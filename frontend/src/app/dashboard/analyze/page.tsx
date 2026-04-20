'use client';

import { useState, useRef, useEffect } from 'react';
import { useUser } from '@clerk/nextjs';
import ResumeUploader from '@/components/ResumeUploader';
import ResultCard from '@/components/ResultCard';
import { Loader2 } from 'lucide-react';
import axios from 'axios';

export default function AnalyzePage() {
  const { isLoaded, isSignedIn, user } = useUser();
  const [currentAnalysis, setCurrentAnalysis] = useState<any>(null);

  const handleAnalysisComplete = async (data: any) => {
    setCurrentAnalysis(data);
  };

  if (!isLoaded) {
    return (
      <div className="flex h-[80vh] items-center justify-center">
        <Loader2 className="animate-spin text-purple-500" size={48} />
      </div>
    );
  }

  if (!isSignedIn) {
    return (
      <div className="flex h-[80vh] flex-col items-center justify-center space-y-4">
        <h1 className="text-2xl font-bold text-white">Please sign in to access the analyzer</h1>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-8 pb-12">
      <div className="mb-10 mt-2">
        <h1 className="text-3xl font-bold text-white mb-2">Analyze Resume</h1>
        <p className="text-slate-400">Paste resume text below to detect fake claims and inconsistencies.</p>
      </div>

      <div className="space-y-8">
        <ResumeUploader onAnalysisComplete={handleAnalysisComplete} />
        
        {currentAnalysis && (
          <div 
            className="space-y-4 mt-16 transition-all duration-500 ease-in-out transform translate-y-0 opacity-100 animate-in fade-in slide-in-from-bottom-8"
          >
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-bold text-white">Analysis Result</h3>
              <button 
                onClick={() => setCurrentAnalysis(null)}
                className="text-sm font-medium text-slate-400 hover:text-white transition-colors px-3 py-1.5 rounded-md hover:bg-slate-800"
              >
                Clear Result
              </button>
            </div>
            <ResultCard data={currentAnalysis} />
          </div>
        )}
      </div>
    </div>
  );
}
