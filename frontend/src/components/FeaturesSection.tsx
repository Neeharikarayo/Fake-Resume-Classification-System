'use client';

import { Brain, ShieldCheck, Clock, BarChart3, Lock, History } from 'lucide-react';

const features = [
  {
    icon: Brain,
    title: 'AI Resume Analysis',
    description: 'Analyze resumes using advanced machine learning models trained on thousands of real and synthetic data points.',
    gradient: 'from-indigo-500 to-purple-500',
  },
  {
    icon: ShieldCheck,
    title: 'Skill Consistency Detection',
    description: 'Detect mismatched skills and experience levels that indicate fabricated or exaggerated qualifications.',
    gradient: 'from-purple-500 to-pink-500',
  },
  {
    icon: Clock,
    title: 'Timeline Validation',
    description: 'Identify unrealistic job histories, overlapping positions, and suspicious career progression patterns.',
    gradient: 'from-pink-500 to-rose-500',
  },
  {
    icon: BarChart3,
    title: 'Fraud Risk Score',
    description: 'Get an AI-generated fraud probability score with detailed confidence metrics and breakdown.',
    gradient: 'from-indigo-400 to-cyan-400',
  },
  {
    icon: Lock,
    title: 'Secure Authentication',
    description: 'Enterprise-grade security with protected user accounts, encrypted data, and role-based access.',
    gradient: 'from-purple-400 to-indigo-400',
  },
  {
    icon: History,
    title: 'History Tracking',
    description: 'View and compare previous resume analysis results with full audit trail and exportable reports.',
    gradient: 'from-blue-400 to-indigo-400',
  },
];

const FeaturesSection = () => {
  return (
    <section id="features" className="relative py-24 sm:py-32 bg-slate-950">
      <div className="relative z-10 max-w-7xl mx-auto px-6">
        {/* Section Header */}
        <div className="text-center mb-16">
          <p className="text-sm font-semibold uppercase tracking-widest text-indigo-400 mb-3">Features</p>
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Everything you need to verify candidates
          </h2>
          <p className="text-slate-400 text-lg max-w-2xl mx-auto">
            Our AI platform combines multiple detection methods to deliver comprehensive resume analysis at scale.
          </p>
        </div>

        {/* Feature Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div
                key={feature.title}
                className="group relative bg-slate-900 border border-slate-800 rounded-xl p-6 hover:-translate-y-1 shadow-lg transition-all duration-300 hover:border-indigo-500/50"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                {/* Icon */}
                <div className={`inline-flex items-center justify-center w-12 h-12 rounded-xl bg-gradient-to-br ${feature.gradient} mb-6 shadow-md`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>

                {/* Content */}
                <h3 className="text-xl font-semibold text-white mb-3">
                  {feature.title}
                </h3>
                <p className="text-slate-400 leading-relaxed text-sm">
                  {feature.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;
