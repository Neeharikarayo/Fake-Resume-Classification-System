'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, FileSearch, History, User, Settings, BrainCircuit } from 'lucide-react';

const Sidebar = () => {
  const pathname = usePathname();

  const menuItems = [
    { name: 'Dashboard Overview', icon: LayoutDashboard, href: '/dashboard' },
    { name: 'Analyze Resume', icon: FileSearch, href: '/dashboard/analyze' },
    { name: 'Resume Insights', icon: BrainCircuit, href: '/dashboard/insights' },
    { name: 'Analysis History', icon: History, href: '/dashboard/history' },
    { name: 'Settings', icon: Settings, href: '/dashboard/settings' },
  ];

  return (
    <div className="w-64 bg-slate-950 border-r border-slate-800 h-screen flex-col hidden md:flex sticky top-0">
      <div className="p-6 flex-1">
        <Link href="/" className="text-xl font-bold tracking-tight text-white mb-10 block">
          ResumeScan.ai
        </Link>
        <nav className="space-y-2">
          {menuItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                  isActive 
                    ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-lg shadow-indigo-500/20' 
                    : 'text-slate-400 hover:bg-slate-900 hover:text-white'
                }`}
              >
                <item.icon size={20} />
                <span className="font-medium">{item.name}</span>
              </Link>
            );
          })}
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;
