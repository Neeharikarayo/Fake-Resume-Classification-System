'use client';

import Link from 'next/link';
import { Sparkles, ArrowRight } from 'lucide-react';
import { useEffect, useRef } from 'react';
import Image from 'next/image';

const HeroSection = () => {
  const imageRef = useRef(null);

  useEffect(() => {
    const imageElement = imageRef.current;

    if (!imageElement) return;

    let ticking = false;
    const scrollThreshold = 100;

    const handleScroll = () => {
      const scrollPosition = window.scrollY || window.pageYOffset;

      if (!ticking) {
        window.requestAnimationFrame(() => {
          if (scrollPosition > scrollThreshold) {
            imageElement.classList.add("scrolled");
          } else {
            imageElement.classList.remove("scrolled");
          }
          ticking = false;
        });
        ticking = true;
      }
    };

    window.addEventListener("scroll", handleScroll, { passive: true });

    handleScroll();

    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  return (
    <section className="relative min-h-[90vh] flex flex-col items-center justify-center overflow-hidden">

      {/* Content */}
      <div className="relative z-10 max-w-7xl mx-auto px-6 text-center mt-24">
        {/* Badge */}
        {/* <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-slate-700 bg-slate-800/50 backdrop-blur-sm mb-8 animate-slide-up">
          <Sparkles className="w-4 h-4 text-indigo-400" />
          <span className="text-sm text-slate-300 font-medium">Powered by Advanced Machine Learning</span>
        </div> */}

        {/* Title */}
        <h1 className="text-5xl md:text-6xl font-bold text-white tracking-tight leading-[1.1] mb-6 animate-slide-up delay-100">
          Detect{' '}
          <span className="bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            Fake Resumes
          </span>
          <br />
          with AI
        </h1>

        {/* Subtitle */}
        <p className="text-lg sm:text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed animate-slide-up delay-200">
          Use machine learning to instantly analyze resumes and identify fraudulent claims,
          skill inconsistencies, and suspicious career timelines.
        </p>

        {/* Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-slide-up delay-300">
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 px-8 py-4 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-xl shadow-lg hover:shadow-indigo-500/25 transition-all duration-300 hover:-translate-y-0.5 group"
          >
            Get Started
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </Link>
          <Link
            href="#how-it-works"
            className="inline-flex items-center gap-2 px-8 py-4 bg-slate-900 border border-slate-800 rounded-xl text-slate-300 font-semibold hover:bg-slate-800 transition-all duration-300"
          >
            Try Demo
          </Link>
        </div>

        {/* Stats Bar */}


        {/* Animated Hero Image */}
        <div className="hero-image-wrapper mt-5 md:mt-0 flex justify-center">
          <div ref={imageRef} className="hero-image">
            <Image
              src="/banner.jpeg"
              height={720}
              width={1000}
              alt="Banner Fake Resume Detection"
              className="rounded-lg shadow-2xl border mx-auto"
              priority
            />
          </div>
        </div>

        <div className="mt-16 grid grid-cols-3 gap-8 max-w-lg mx-auto animate-slide-up delay-400">
          <div>
            <p className="text-2xl sm:text-3xl font-bold text-white">12K+</p>
            <p className="text-sm text-slate-400 mt-1">Resumes Analyzed</p>
          </div>
          <div>
            <p className="text-2xl sm:text-3xl font-bold text-white">95%</p>
            <p className="text-sm text-slate-400 mt-1">Detection Accuracy</p>
          </div>
          <div>
            <p className="text-2xl sm:text-3xl font-bold text-white">&lt;2s</p>
            <p className="text-sm text-slate-400 mt-1">Analysis Time</p>
          </div>
        </div>
      </div>

      {/* Bottom fade */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-slate-950 to-transparent" />
    </section>
  );
};

export default HeroSection;
