import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@clerk/nextjs/server';
import dbConnect from '@/lib/mongodb';
import Analysis from '@/models/Analysis';
import { predictResume } from '@/lib/api';

export async function POST(req: NextRequest) {
  try {
    const { userId } = await auth();
    
    if (!userId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { resume_text } = await req.json();

    if (!resume_text) {
      return NextResponse.json({ error: 'Resume text is required' }, { status: 400 });
    }

    // Call FastAPI backend for prediction
    // Note: handle the case where FastAPI might be down
    let predictionResult;
    try {
      predictionResult = await predictResume(resume_text);
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
      resumeText: resume_text,
      prediction: predictionResult.prediction,
      confidence: predictionResult.confidence,
      issues: predictionResult.issues,
      details: predictionResult.details,
    });

    return NextResponse.json(analysis);
  } catch (error: any) {
    console.error('Analysis route error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

export async function GET(req: NextRequest) {
  try {
    const { userId } = await auth();
    
    if (!userId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    await dbConnect();
    
    const analyses = await Analysis.find({ userId }).sort({ createdAt: -1 }).limit(10);
    
    return NextResponse.json(analyses);
  } catch (error: any) {
    console.error('Analyses history error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
