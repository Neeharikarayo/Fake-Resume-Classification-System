'use client';

import { Star } from 'lucide-react';

const testimonials = [
  {
    name: 'Sarah Mitchell',
    role: 'Senior Recruiter',
    company: 'TechCorp Inc.',
    initials: 'SM',
    rating: 5,
    quote: 'This tool helped us detect multiple fraudulent resumes during hiring. We caught several candidates with fabricated work histories that would have slipped through.',
    gradient: 'from-indigo-500 to-purple-500',
  },
  {
    name: 'James Rodriguez',
    role: 'HR Manager',
    company: 'GlobalHire Solutions',
    initials: 'JR',
    rating: 5,
    quote: 'The AI analysis saved our recruitment team hours of manual verification. What used to take days now takes seconds with incredible accuracy.',
    gradient: 'from-purple-500 to-pink-500',
  },
  {
    name: 'Priya Sharma',
    role: 'Startup Founder',
    company: 'InnovateTech',
    initials: 'PS',
    rating: 5,
    quote: 'A powerful AI tool for verifying candidate claims. As a startup, we can\'t afford bad hires — this tool gives us enterprise-level screening capabilities.',
    gradient: 'from-pink-500 to-rose-500',
  },
];

const TestimonialsSection = () => {
  return (
    <section id="testimonials" className="relative py-24 sm:py-32 bg-slate-950">
      <div className="relative z-10 max-w-7xl mx-auto px-6">
        {/* Section Header */}
        <div className="text-center mb-16">
          <p className="text-sm font-semibold uppercase tracking-widest text-indigo-400 mb-3">Testimonials</p>
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Trusted by industry leaders
          </h2>
          <p className="text-slate-400 text-lg max-w-xl mx-auto">
            See what HR professionals and recruiters have to say about our platform.
          </p>
        </div>

        {/* Testimonial Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {testimonials.map((testimonial) => (
            <div
              key={testimonial.name}
              className="group bg-slate-900/80 backdrop-blur-md border border-slate-800 rounded-xl p-6 shadow-lg hover:-translate-y-1 hover:border-indigo-500/50 transition-all duration-300"
            >
              {/* Stars */}
              <div className="flex items-center gap-1 mb-6">
                {Array.from({ length: testimonial.rating }).map((_, i) => (
                  <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                ))}
              </div>

              {/* Quote */}
              <p className="text-slate-300 leading-relaxed mb-8 text-sm italic">
                &ldquo;{testimonial.quote}&rdquo;
              </p>

              {/* Author */}
              <div className="flex items-center gap-4">
                <div className={`w-12 h-12 rounded-full bg-gradient-to-br ${testimonial.gradient} flex items-center justify-center text-white font-bold text-sm shadow-md`}>
                  {testimonial.initials}
                </div>
                <div>
                  <p className="text-white font-semibold text-sm">{testimonial.name}</p>
                  <p className="text-slate-400 text-xs">{testimonial.role}, {testimonial.company}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default TestimonialsSection;
