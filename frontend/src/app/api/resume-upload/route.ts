import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@clerk/nextjs/server';
import dbConnect from '@/lib/mongodb';
import Analysis from '@/models/Analysis';
import { predictResume } from '@/lib/api';

export const dynamic = 'force-dynamic';

export async function POST(req: NextRequest) {
  try {
    // Polyfill DOMMatrix for pdf-parse (pdfjs-dist dependency in Node environments)
    // @ts-ignore
    if (typeof global.DOMMatrix === 'undefined') {
      // @ts-ignore
      global.DOMMatrix = class DOMMatrix { };
    }
    // @ts-ignore
    const pdfParse = require('pdf-parse/lib/pdf-parse.js');

    // @ts-ignore
    const mammothModule = await import('mammoth');
    // @ts-ignore
    const mammoth = mammothModule.default || mammothModule;

    const { userId } = await auth();

    if (!userId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const formData = await req.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return NextResponse.json({ error: 'No file uploaded' }, { status: 400 });
    }

    // Check file size (e.g., limit to 5MB)
    if (file.size > 5 * 1024 * 1024) {
      return NextResponse.json({ error: 'File size exceeds 5MB limit' }, { status: 400 });
    }

    const buffer = Buffer.from(await file.arrayBuffer());
    const fileName = file.name.toLowerCase();
    let extractedText = '';

    try {
      if (fileName.endsWith('.pdf')) {
        let pdfData = await pdfParse(buffer);
        extractedText = pdfData.text;
      } else if (fileName.endsWith('.docx')) {
        const result = await mammoth.extractRawText({ buffer });
        extractedText = result.value;
      } else {
        return NextResponse.json({ error: 'Unsupported file format. Please upload PDF or DOCX.' }, { status: 400 });
      }
    } catch (parseError) {
      console.error('Text extraction error:', parseError);
      return NextResponse.json({ error: 'Failed to extract text from file' }, { status: 422 });
    }

    if (!extractedText || !extractedText.trim()) {
      return NextResponse.json({ error: 'No readable text found in the file' }, { status: 422 });
    }

    // Call FastAPI backend for prediction
    let predictionResult;
    try {
      predictionResult = await predictResume(extractedText);
    } catch (apiError) {
      console.error('FastAPI error:', apiError);
      return NextResponse.json({
        error: 'Prediction service is currently unavailable. Please make sure the backend is running.'
      }, { status: 503 });
    }

    // Save to MongoDB
    await dbConnect();

    const analysis = await Analysis.create({
      userId,
      resumeText: extractedText,
      prediction: predictionResult.prediction,
      confidence: predictionResult.confidence,
      issues: predictionResult.issues,
      details: predictionResult.details,
    });

    return NextResponse.json(analysis);
  } catch (error: any) {
    console.error('Resume upload route error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
