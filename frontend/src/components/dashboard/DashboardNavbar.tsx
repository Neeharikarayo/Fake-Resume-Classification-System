'use client';

import { UserButton } from '@clerk/nextjs';
import { Menu } from 'lucide-react';

const DashboardNavbar = () => {
  return (
    <header className="bg-slate-950 border-b border-slate-800 text-white h-16 flex items-center justify-between px-6 lg:px-10 sticky top-0 z-20 w-full backdrop-blur-xl bg-slate-950/80">
      <div className="flex items-center space-x-4">
        <button className="md:hidden text-slate-400 hover:text-white transition-colors">
          <Menu size={24} />
        </button>
        <h1 className="text-lg font-semibold md:hidden bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400">ResumeScan.ai</h1>
        <h1 className="text-lg font-semibold hidden md:block text-slate-300">Overview</h1>
      </div>
      <div>
        <UserButton 
          appearance={{
            elements: {
              avatarBox: "w-8 h-8 rounded-full border border-slate-700 hover:border-indigo-500 transition-colors"
            }
          }}
        />
      </div>
    </header>
  );
};

export default DashboardNavbar;
