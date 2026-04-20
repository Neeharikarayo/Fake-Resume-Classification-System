'use client';

import { useState, useRef } from 'react';
import { Search, Loader2, UploadCloud, FileText } from 'lucide-react';
import axios from 'axios';
import ResumeAnalysisProgress, { ANALYSIS_STEPS } from './ResumeAnalysisProgress';
interface ResumeUploaderProps {
  onAnalysisComplete: (data: any) => void;
}

const ResumeUploader = ({ onAnalysisComplete }: ResumeUploaderProps) => {
  const [text, setText] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisStep, setAnalysisStep] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const progressRef = useRef<HTMLDivElement>(null);

  const handleAnalyzeText = async () => {
    if (!text.trim()) {
      setError('Please enter some resume text');
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setAnalysisStep(3); // Skip straight to parsing if text is manually pasted

    setTimeout(() => {
      progressRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);

    try {
      const response = await axios.post('/api/analysis', { resume_text: text });
      
      // Simulate the remaining AI steps visually for the UI effect
      setAnalysisStep(4);
      await new Promise(r => setTimeout(r, 600));
      setAnalysisStep(5);
      await new Promise(r => setTimeout(r, 600));
      setAnalysisStep(6);
      await new Promise(r => setTimeout(r, 400));

      onAnalysisComplete(response.data);
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.error || 'Failed to analyze resume. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleFileUpload = async (file: File) => {
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    if (!validTypes.includes(file.type) && !file.name.endsWith('.pdf') && !file.name.endsWith('.docx')) {
      setError('Please upload a valid PDF or DOCX file.');
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setAnalysisStep(1);

    setTimeout(() => {
      progressRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Simulate file extraction step
      setAnalysisStep(2);
      
      const response = await axios.post('/api/resume-upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setText(response.data.resumeText);
      setAnalysisStep(3);
      await new Promise(r => setTimeout(r, 500));
      setAnalysisStep(4);
      await new Promise(r => setTimeout(r, 700));
      setAnalysisStep(5);
      await new Promise(r => setTimeout(r, 600));
      setAnalysisStep(6);
      await new Promise(r => setTimeout(r, 400));
      
      onAnalysisComplete(response.data);
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.error || 'Failed to extract and analyze file. Please try again.');
    } finally {
      setIsAnalyzing(false);
      setAnalysisStep(0);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const onDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const onDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFileUpload(file);
  };

  return (
    <div className="space-y-6">
      {/* Upload Card */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 shadow-xl transition-all duration-200">
        <h2 className="text-xl font-bold text-white mb-6 flex items-center">
          <UploadCloud className="mr-2 text-indigo-400" /> Upload Document
        </h2>
        
        <div 
          onDragOver={onDragOver}
          onDragLeave={onDragLeave}
          onDrop={onDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-colors duration-200 flex flex-col items-center justify-center ${
            isDragging ? 'border-indigo-500 bg-indigo-500/10' : 'border-slate-600 hover:border-slate-500 hover:bg-slate-800/50'
          }`}
        >
          <input 
            type="file" 
            ref={fileInputRef}
            className="hidden" 
            accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) handleFileUpload(file);
            }}
          />
          <FileText className={`w-12 h-12 mb-4 ${isDragging ? 'text-indigo-400' : 'text-slate-500'}`} />
          <p className="text-lg font-medium text-white mb-2">Drag & drop your resume here, or click to upload</p>
          <p className="text-sm text-slate-400">Supported formats: PDF, DOCX (Max 5MB)</p>
          
          {isAnalyzing && analysisStep <= 2 && (
            <div className="mt-6 flex items-center text-purple-400 bg-purple-500/10 px-4 py-2 rounded-full font-medium">
              <Loader2 className="animate-spin mr-2" size={18} /> Uploading & Extracting Text...
            </div>
          )}
        </div>
      </div>

      <div className="relative flex items-center py-2">
        <div className="flex-grow border-t border-slate-800"></div>
        <span className="flex-shrink-0 mx-4 text-slate-500 text-sm font-medium">OR</span>
        <div className="flex-grow border-t border-slate-800"></div>
      </div>

      {/* Text Analyzer Card */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 shadow-xl transition-all duration-200">
        <div className="flex flex-col space-y-4">
          <label htmlFor="resume_text" className="text-xl font-bold text-white flex items-center">
            Manual Text Input
          </label>
          <p className="text-sm text-slate-400 mb-2">
            Paste raw resume text below to analyze it, or edit text extracted from your uploaded file before re-analyzing.
          </p>
          <textarea
            id="resume_text"
            className="w-full h-64 p-4 text-slate-300 bg-slate-950 border border-slate-800 rounded-xl focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/30 outline-none transition-all resize-none placeholder-slate-600 shadow-inner"
            placeholder="Paste resume text here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          
          {error && (
            <div className="p-4 bg-red-500/10 border border-red-500/20 text-red-400 rounded-lg text-sm transition-all flex items-center">
              <span className="font-semibold mr-2">Error:</span> {error}
            </div>
          )}

          <button
            onClick={handleAnalyzeText}
            disabled={isAnalyzing || !text.trim()}
            className={`flex items-center justify-center space-x-2 px-6 py-3 rounded-lg font-bold text-white transition-all duration-200 w-full md:w-auto self-end mt-2 ${
              isAnalyzing || !text.trim()
                ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
                : 'bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 hover:opacity-90 shadow-lg shadow-purple-500/25'
            }`}
          >
            {isAnalyzing ? (
              <>
                <Loader2 className="animate-spin" size={20} />
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <Search size={20} />
                <span>Analyze Text</span>
              </>
            )}
          </button>
        </div>
      </div>
      {/* AI Processing Simulation */}
      <div ref={progressRef}>
        {isAnalyzing && analysisStep > 0 && (
          <ResumeAnalysisProgress currentStep={analysisStep} />
        )}
      </div>
    </div>
  );
};

export default ResumeUploader;
