'use client';

import { CheckCircle2, Circle, Loader2 } from 'lucide-react';

interface ResumeAnalysisProgressProps {
  currentStep: number;
}

export const ANALYSIS_STEPS = [
  { id: 1, label: 'Uploading Resume' },
  { id: 2, label: 'Extracting Resume Text' },
  { id: 3, label: 'Parsing Resume Data' },
  { id: 4, label: 'Running AI Model Analysis' },
  { id: 5, label: 'Detecting Fraud Patterns' },
  { id: 6, label: 'Generating Final Report' }
];

const ResumeAnalysisProgress = ({ currentStep }: ResumeAnalysisProgressProps) => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 shadow-xl mt-6">
      <h3 className="text-xl font-bold text-white mb-6 flex items-center">
        <Loader2 className="animate-spin mr-3 text-purple-400" size={24} /> 
        Analyzing resume with AI...
      </h3>
      
      <div className="space-y-4">
        {ANALYSIS_STEPS.map((step) => {
          const isCompleted = currentStep > step.id;
          const isActive = currentStep === step.id;
          const isPending = currentStep < step.id;

          return (
            <div 
              key={step.id} 
              className={`flex items-center p-3 rounded-lg transition-all duration-300 ${
                isActive ? 'bg-slate-800/80 border border-slate-700/50 shadow-inner translate-x-1' 
                : 'border border-transparent'
              }`}
            >
              <div className="mr-4 flex-shrink-0">
                {isCompleted && (
                  <CheckCircle2 className="text-emerald-400" size={20} />
                )}
                {isActive && (
                  <Loader2 className="text-purple-400 animate-spin" size={20} />
                )}
                {isPending && (
                  <Circle className="text-slate-600" size={20} />
                )}
              </div>
              
              <span className={`text-sm md:text-base font-semibold transition-colors duration-300 ${
                isCompleted ? 'text-emerald-400' 
                : isActive ? 'text-purple-400 animate-pulse' 
                : 'text-slate-500'
              }`}>
                {step.label}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ResumeAnalysisProgress;
