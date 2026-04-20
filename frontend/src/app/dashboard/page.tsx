'use client';

import { useState, useEffect, useMemo } from 'react';
import { useUser } from '@clerk/nextjs';
import StatsCards from '@/components/dashboard/StatsCards';
import AnalysisHistory from '@/components/dashboard/AnalysisHistory';
import { Loader2 } from 'lucide-react';
import axios from 'axios';
import { useRouter } from 'next/navigation';

export default function DashboardOverviewPage() {
  const { isLoaded, isSignedIn, user } = useUser();
  const [history, setHistory] = useState<any[]>([]);
  const [isLoadingHistory, setIsLoadingHistory] = useState(true);
  const router = useRouter();

  useEffect(() => {
    if (isLoaded && isSignedIn) {
      syncUser();
      fetchHistory();
    }
  }, [isLoaded, isSignedIn]);

  const syncUser = async () => {
    try {
      await axios.post('/api/users');
    } catch (err) {
      console.error('Failed to sync user:', err);
    }
  };

  const fetchHistory = async () => {
    try {
      const response = await axios.get('/api/analysis');
      setHistory(response.data);
    } catch (err) {
      console.error('Failed to fetch history:', err);
    } finally {
      setIsLoadingHistory(false);
    }
  };

  const stats = useMemo(() => {
    const total = history.length;
    const fake = history.filter(h => h.prediction === 'Fake').length;
    const suspicious = history.filter(h => h.prediction === 'Suspicious').length;
    const totalConfidence = history.reduce((sum, item) => sum + (item.confidence || 0), 0);
    const avgConfidence = total > 0 ? totalConfidence / total : 0;
    
    return { total, fake, suspicious, avgConfidence };
  }, [history]);

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
        <h1 className="text-2xl font-bold text-white">Please sign in to access the dashboard</h1>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6 md:p-8 pb-12">
      <div className="mb-10 mt-2">
        <h1 className="text-3xl font-bold text-white mb-2">Welcome back, {user.firstName || 'User'} 👋</h1>
        <p className="text-slate-400">Here's an overview of your AI resume analysis activity.</p>
      </div>

      <StatsCards 
        total={stats.total} 
        fake={stats.fake} 
        suspicious={stats.suspicious} 
        avgConfidence={stats.avgConfidence} 
      />

      <div className="grid grid-cols-1 gap-8 items-start mt-8">
        <div className="border-slate-800">
          <AnalysisHistory 
            history={history.slice(0, 5)} 
            isLoading={isLoadingHistory} 
            onSelectResult={() => router.push('/dashboard/history')} 
          />
        </div>
      </div>
    </div>
  );
}
