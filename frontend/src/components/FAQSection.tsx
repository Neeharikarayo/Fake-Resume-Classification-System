'use client';

import { useState } from 'react';
import { ChevronDown } from 'lucide-react';

const faqs = [
  {
    question: 'What is AI Fake Resume Detection?',
    answer: 'Our AI system uses machine learning models trained on thousands of real and synthetic resumes to identify patterns commonly found in fake or exaggerated applications. It analyzes skills, experience timelines, text patterns, and consistency to generate a fraud risk score.',
  },
  {
    question: 'How accurate is the AI model?',
    answer: 'Our model achieves over 95% accuracy in detecting fake resumes across our test datasets. It was trained on 12,000+ samples and uses multiple classification techniques including natural language processing, feature extraction, and pattern recognition.',
  },
  {
    question: 'Is my resume data secure?',
    answer: 'Absolutely. All data is encrypted in transit and at rest. We use enterprise-grade authentication with Clerk, and your resume data is stored securely in encrypted MongoDB databases. We never share your data with third parties.',
  },
  {
    question: 'Can recruiters use this tool for hiring?',
    answer: 'Yes! Our platform is designed for recruiters, HR managers, and hiring teams of all sizes. You can analyze individual resumes or batch-process multiple applications. Our API also supports integration with existing ATS systems.',
  },
  {
    question: 'How does the fraud detection system work?',
    answer: 'The system works in three stages: First, it extracts features from the resume text (skills count, experience years, word patterns). Then, the ML model evaluates these features against known patterns of genuine and fake resumes. Finally, it generates a comprehensive report with a fraud probability score and flagged issues.',
  },
];

const FAQSection = () => {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const toggle = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <section id="faq" className="relative py-24 sm:py-32 bg-slate-950">
      <div className="relative z-10 max-w-3xl mx-auto px-6">
        {/* Section Header */}
        <div className="text-center mb-16">
          <p className="text-sm font-semibold uppercase tracking-widest text-indigo-400 mb-3">FAQ</p>
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Frequently asked questions
          </h2>
          <p className="text-slate-400 text-lg max-w-xl mx-auto">
            Everything you need to know about our AI resume detection platform.
          </p>
        </div>

        {/* Accordion */}
        <div className="space-y-4">
          {faqs.map((faq, index) => (
            <div
              key={index}
              className={`bg-slate-900 border ${openIndex === index ? 'border-indigo-500/50' : 'border-slate-800'
                } rounded-xl overflow-hidden transition-all duration-300 shadow-lg`}
            >
              <button
                onClick={() => toggle(index)}
                className="w-full flex items-center justify-between p-6 text-left hover:bg-slate-800 transition-colors"
              >
                <span className="text-white font-semibold pr-4">{faq.question}</span>
                <ChevronDown
                  className={`w-5 h-5 text-indigo-400 flex-shrink-0 transition-transform duration-300 ${openIndex === index ? 'rotate-180' : ''
                    }`}
                />
              </button>
              <div
                className={`overflow-hidden transition-all duration-300 ${openIndex === index ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'
                  }`}
              >
                <p className="px-6 pb-6 text-slate-400 leading-relaxed text-sm">
                  {faq.answer}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FAQSection;
