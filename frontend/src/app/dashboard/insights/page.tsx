'use client';

import { useState, useEffect } from 'react';
import { useUser } from '@clerk/nextjs';
import { Loader2, BrainCircuit, Code, BookOpen, Clock, AlertTriangle, CheckCircle2 } from 'lucide-react';
import axios from 'axios';

export default function InsightsPage() {
  const { isLoaded, isSignedIn } = useUser();
  const [history, setHistory] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (isLoaded && isSignedIn) {
      fetchHistory();
    }
  }, [isLoaded, isSignedIn]);

  const fetchHistory = async () => {
    try {
      const response = await axios.get('/api/analysis');
      setHistory(response.data);
    } catch (err) {
      console.error('Failed to fetch history:', err);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isLoaded || isLoading) {
    return (
      <div className="flex h-[80vh] items-center justify-center">
        <Loader2 className="animate-spin text-purple-500" size={48} />
      </div>
    );
  }

  if (!isSignedIn) {
    return (
      <div className="flex h-[80vh] flex-col items-center justify-center space-y-4">
        <h1 className="text-2xl font-bold text-white">Please sign in to view AI Insights</h1>
      </div>
    );
  }

  // Calculate insights
  const totalAnalyzed = history.length;
  let totalSkillsExtracted = 0;
  let totalExperience = 0;
  let fakeCount = 0;
  let genuineCount = 0;

  history.forEach((h) => {
    totalSkillsExtracted += (h.details?.skill_count || 0);
    totalExperience += (h.details?.experience_years || 0);
    if (h.prediction === 'Fake') fakeCount++;
    if (h.prediction === 'Genuine') genuineCount++;
  });

  const avgSkills = totalAnalyzed ? Math.round(totalSkillsExtracted / totalAnalyzed) : 0;
  const avgExperience = totalAnalyzed ? Math.round(totalExperience / totalAnalyzed) : 0;
  const fakePercentage = totalAnalyzed ? Math.round((fakeCount / totalAnalyzed) * 100) : 0;

  // Find most recent extreme Fake
  const topFake = history.filter(h => h.prediction === 'Fake').sort((a, b) => b.confidence - a.confidence)[0];

  return (
    <div className="max-w-7xl mx-auto p-6 md:p-8 pb-12">
      <div className="mb-10 mt-2">
        <h1 className="text-3xl font-bold text-white mb-2 flex items-center gap-3">
          <BrainCircuit className="text-purple-400" /> AI Resume Insights
        </h1>
        <p className="text-slate-400">Deep-dive intelligence extracted across all your analyzed resumes.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-10">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl relative overflow-hidden group">
          <div className="absolute -right-4 -top-4 opacity-5 bg-gradient-to-bl from-indigo-500 rounded-full w-32 h-32" />
          <div className="flex items-center gap-4 mb-4">
            <div className="w-12 h-12 rounded-xl bg-indigo-500/20 flex items-center justify-center text-indigo-400">
              <Code size={24} />
            </div>
            <div>
              <p className="text-sm text-slate-400 font-medium">Avg Skills per Resume</p>
              <h3 className="text-3xl font-bold text-white">{avgSkills}</h3>
            </div>
          </div>
          <p className="text-sm text-slate-500">The average number of technologies and skills mapped by the AI extraction engine.</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl relative overflow-hidden group">
          <div className="absolute -right-4 -top-4 opacity-5 bg-gradient-to-bl from-emerald-500 rounded-full w-32 h-32" />
          <div className="flex items-center gap-4 mb-4">
            <div className="w-12 h-12 rounded-xl bg-emerald-500/20 flex items-center justify-center text-emerald-400">
              <Clock size={24} />
            </div>
            <div>
              <p className="text-sm text-slate-400 font-medium">Avg Claimed Experience</p>
              <h3 className="text-3xl font-bold text-white">{avgExperience} yrs</h3>
            </div>
          </div>
          <p className="text-sm text-slate-500">Average tenure claimed across all collected documentation.</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl relative overflow-hidden group">
          <div className="absolute -right-4 -top-4 opacity-5 bg-gradient-to-bl from-rose-500 rounded-full w-32 h-32" />
          <div className="flex items-center gap-4 mb-4">
            <div className="w-12 h-12 rounded-xl bg-rose-500/20 flex items-center justify-center text-rose-400">
              <AlertTriangle size={24} />
            </div>
            <div>
              <p className="text-sm text-slate-400 font-medium">Fake Rate</p>
              <h3 className="text-3xl font-bold text-white">{fakePercentage}%</h3>
            </div>
          </div>
          <p className="text-sm text-slate-500">Percentage of documents flagged with critical timeline or credential issues.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-xl">
           <h3 className="text-xl font-bold text-white mb-6">Engine Activity</h3>
           <div className="space-y-6">
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-slate-400">Genuine Profiles</span>
                  <span className="text-emerald-400 font-bold">{genuineCount}</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2">
                  <div className="bg-emerald-400 h-2 rounded-full" style={{ width: `${totalAnalyzed ? (genuineCount/totalAnalyzed)*100 : 0}%` }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-slate-400">Suspicious Profiles</span>
                  <span className="text-amber-400 font-bold">{totalAnalyzed - fakeCount - genuineCount}</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2">
                  <div className="bg-amber-400 h-2 rounded-full" style={{ width: `${totalAnalyzed ? ((totalAnalyzed - fakeCount - genuineCount)/totalAnalyzed)*100 : 0}%` }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-slate-400">Fake Profiles</span>
                  <span className="text-rose-400 font-bold">{fakeCount}</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2">
                  <div className="bg-rose-400 h-2 rounded-full" style={{ width: `${totalAnalyzed ? (fakeCount/totalAnalyzed)*100 : 0}%` }}></div>
                </div>
              </div>
           </div>
        </div>

        {topFake && (
          <div className="bg-gradient-to-br from-rose-500/10 to-transparent border border-rose-500/20 rounded-2xl p-8 shadow-xl">
            <h3 className="text-xl font-bold text-rose-400 mb-6 flex items-center">
              <AlertTriangle className="mr-2" /> Top Flagged Candidate
            </h3>
            <div className="bg-slate-950/60 rounded-xl p-6 border border-slate-800/50">
              <div className="flex justify-between items-center mb-4">
                <span className="text-sm text-slate-400">Date Logged</span>
                <span className="text-sm text-slate-300 bg-slate-800 px-3 py-1 rounded-full">{new Date(topFake.createdAt).toLocaleDateString()}</span>
              </div>
              <div className="mb-4">
                <p className="text-slate-400 text-sm mb-1">AI Match Confidence</p>
                <p className="text-2xl font-black text-white">{(topFake.confidence * 100).toFixed(1)}%</p>
              </div>
              {topFake.issues && topFake.issues.length > 0 && (
                 <div>
                   <p className="text-slate-400 text-sm mb-2">Detected Anomalies</p>
                   <ul className="space-y-2">
                     {topFake.issues.map((i: string, idx: number) => (
                       <li key={idx} className="text-sm text-slate-300 flex items-start">
                         <span className="w-1.5 h-1.5 bg-rose-500 rounded-full mt-1.5 mr-2 flex-shrink-0" /> {i}
                       </li>
                     ))}
                   </ul>
                 </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
