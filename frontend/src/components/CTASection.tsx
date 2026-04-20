import Link from 'next/link';
import { ArrowRight } from 'lucide-react';

const CTASection = () => {
  return (
    <section className="relative py-24 px-6 bg-slate-950 overflow-hidden">
      <div className="relative z-10 max-w-5xl mx-auto text-center">
        {/* Glowing gradient background blur behind the section */}
        <div className="absolute inset-0 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 blur-3xl opacity-30 -z-10 rounded-[3rem]" />

        <div className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 rounded-2xl shadow-xl p-10 md:p-16 relative overflow-hidden">
          <div className="relative z-10">
            <h2 className="text-3xl md:text-5xl font-bold text-white">
              Start Detecting Fake Resumes Today
            </h2>
            <p className="text-lg text-indigo-100 mt-4 max-w-2xl mx-auto mb-10">
              Use AI to instantly analyze resumes and detect fraudulent claims, skill inconsistencies, and suspicious timelines.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link
                href="/dashboard"
                className="inline-flex items-center justify-center bg-white text-indigo-600 px-6 py-3 rounded-lg font-semibold shadow-lg hover:bg-gray-200 transition-colors"
              >
                Get Started
                <ArrowRight className="w-5 h-5 ml-2" />
              </Link>
              <Link
                href="#how-it-works"
                className="inline-flex items-center justify-center border border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-indigo-600 transition-colors"
              >
                Try Demo
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CTASection;
