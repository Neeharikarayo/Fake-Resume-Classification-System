'use client';

import { Upload, Cpu, FileCheck } from 'lucide-react';

const steps = [
  {
    icon: Upload,
    number: '01',
    title: 'Upload Resume',
    description: 'Paste or upload the resume text you want to analyze. Our system accepts any format.',
    gradient: 'from-purple-500 to-indigo-500',
  },
  {
    icon: Cpu,
    number: '02',
    title: 'AI Analyzes Content',
    description: 'Our ML models examine skills, experience, text patterns, and consistency in real-time.',
    gradient: 'from-indigo-500 to-blue-500',
  },
  {
    icon: FileCheck,
    number: '03',
    title: 'Fraud Detection Report',
    description: 'Receive a detailed report with fraud score, flagged issues, and actionable recommendations.',
    gradient: 'from-blue-500 to-cyan-500',
  },
];

const HowItWorksSection = () => {
  return (
    <section id="how-it-works" className="relative py-24 sm:py-32">
      {/* Background */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-indigo-600/5 rounded-full blur-[140px]" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-6">
        {/* Section Header */}
        <div className="text-center mb-20">
          <p className="text-sm font-semibold uppercase tracking-widest text-purple-400 mb-3">How It Works</p>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-4">
            Three simple <span className="gradient-text">steps</span>
          </h2>
          <p className="text-gray-400 text-lg max-w-xl mx-auto">
            Get from resume to fraud report in under two seconds.
          </p>
        </div>

        {/* Steps */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
          {/* Connecting Lines (desktop only) */}
          <div className="hidden md:block absolute top-[72px] left-[calc(16.67%+60px)] right-[calc(16.67%+60px)] h-[2px]">
            <div className="w-full h-full bg-gradient-to-r from-purple-500/30 via-indigo-500/30 to-blue-500/30" />
          </div>

          {steps.map((step, index) => {
            const Icon = step.icon;
            return (
              <div key={step.title} className="relative group text-center">
                {/* Step Number + Icon */}
                <div className="relative inline-flex flex-col items-center mb-8">
                  <div className={`relative w-36 h-36 rounded-3xl bg-gradient-to-br ${step.gradient} p-[1px] group-hover:shadow-2xl group-hover:shadow-purple-500/10 transition-all duration-500`}>
                    <div className="w-full h-full rounded-3xl bg-[#0a0a1a] flex flex-col items-center justify-center gap-2 group-hover:bg-[#0d0d20] transition-colors">
                      <Icon className="w-10 h-10 text-white/80 group-hover:text-white transition-colors" />
                      <span className="text-xs font-bold text-purple-400/60 tracking-widest">{step.number}</span>
                    </div>
                  </div>
                </div>

                {/* Content */}
                <h3 className="text-xl font-semibold text-white mb-3">{step.title}</h3>
                <p className="text-gray-400 text-sm leading-relaxed max-w-xs mx-auto">{step.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default HowItWorksSection;
