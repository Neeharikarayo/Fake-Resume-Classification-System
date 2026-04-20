'use client';

import { useState, useEffect, useMemo } from 'react';
import { useUser } from '@clerk/nextjs';
import { Loader2, History, AlertTriangle, CheckCircle2, XCircle, Search, Filter, Eye, Trash2, X } from 'lucide-react';
import axios from 'axios';
import ResultCard from '@/components/ResultCard';

export default function HistoryPage() {
  const { isLoaded, isSignedIn } = useUser();
  const [history, setHistory] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  
  // Table State
  const [searchQuery, setSearchQuery] = useState('');
  const [filter, setFilter] = useState<string>('All');
  const [selectedAnalysis, setSelectedAnalysis] = useState<any>(null);

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

  const deleteRecord = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm('Are you sure you want to delete this analysis record?')) return;
    try {
      await axios.delete(`/api/analysis?id=${id}`);
      setHistory(prev => prev.filter(item => item._id !== id));
      if (selectedAnalysis?._id === id) setSelectedAnalysis(null);
    } catch (err) {
      console.error('Failed to delete abstract:', err);
      alert('Failed to delete record. Please check console.');
    }
  };

  // Filter & Search Logic
  const filteredHistory = useMemo(() => {
    return history.filter(item => {
      // Filter tab map
      if (filter !== 'All' && item.prediction !== filter) return false;
      
      // Search Box text match
      if (searchQuery) {
        const query = searchQuery.toLowerCase();
        const dateStr = new Date(item.createdAt).toLocaleDateString().toLowerCase();
        const textSnippet = (item.resumeText || '').toLowerCase();
        return dateStr.includes(query) || textSnippet.includes(query);
      }
      return true;
    });
  }, [history, filter, searchQuery]);

  // Risk Calc
  const getRiskScore = (prediction: string, confidence: number) => {
    if (prediction === 'Fake') return Math.min(100, Math.round(confidence * 100));
    if (prediction === 'Genuine') return Math.max(0, Math.round((1 - confidence) * 100));
    return Math.round(confidence * 100); 
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
        <h1 className="text-2xl font-bold text-white">Please sign in to view history</h1>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6 md:p-8 pb-12 relative">
      <div className="mb-8 mt-2 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2 flex items-center gap-3">
            <History className="text-purple-400" /> Analysis History
          </h1>
          <p className="text-slate-400">Manage, search, and review your previously analyzed resumes.</p>
        </div>
      </div>

      {/* Controls Bar */}
      <div className="bg-slate-900 border border-slate-800 rounded-t-xl p-4 flex flex-col md:flex-row gap-4 items-center justify-between">
        <div className="flex bg-slate-950 rounded-lg p-1 border border-slate-800 w-full md:w-auto">
          {['All', 'Genuine', 'Fake', 'Suspicious'].map(f => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
                filter === f 
                  ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-md' 
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              {f}
            </button>
          ))}
        </div>

        <div className="relative w-full md:w-72">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search size={18} className="text-slate-500" />
          </div>
          <input
            type="text"
            placeholder="Search keyword or date..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white placeholder-slate-500 focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all outline-none"
          />
        </div>
      </div>

      {/* Data Table */}
      <div className="bg-slate-900 border-x border-b border-slate-800 rounded-b-xl overflow-x-auto shadow-xl">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-950/50 border-b border-slate-800 text-slate-400 text-sm uppercase tracking-wider">
              <th className="px-6 py-4 font-semibold">Date</th>
              <th className="px-6 py-4 font-semibold">Prediction</th>
              <th className="px-6 py-4 font-semibold text-center">Confidence</th>
              <th className="px-6 py-4 font-semibold text-center">Risk Score</th>
              <th className="px-6 py-4 font-semibold text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/80">
            {filteredHistory.length > 0 ? (
              filteredHistory.map((item) => {
                const rs = getRiskScore(item.prediction, item.confidence);
                return (
                  <tr key={item._id} className="hover:bg-slate-800/40 transition-colors group cursor-pointer" onClick={() => setSelectedAnalysis(item)}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-slate-300">
                        {new Date(item.createdAt).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })}
                      </div>
                      <div className="text-xs text-slate-500 mt-1">
                        {new Date(item.createdAt).toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' })}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
                        item.prediction === 'Genuine' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' :
                        item.prediction === 'Fake' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' :
                        'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                      }`}>
                        {item.prediction === 'Genuine' ? <CheckCircle2 size={14} className="mr-1.5" /> :
                         item.prediction === 'Fake' ? <XCircle size={14} className="mr-1.5" /> :
                         <AlertTriangle size={14} className="mr-1.5" />}
                        {item.prediction}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm font-semibold text-slate-300">
                      {(item.confidence * 100).toFixed(1)}%
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center justify-center gap-2">
                        <div className="w-16 h-2 bg-slate-800 rounded-full overflow-hidden">
                          <div 
                            className={`h-full rounded-full ${rs > 65 ? 'bg-rose-500' : rs > 35 ? 'bg-amber-400' : 'bg-emerald-400'}`}
                            style={{ width: `${rs}%` }}
                          />
                        </div>
                        <span className={`text-xs font-bold ${rs > 65 ? 'text-rose-400' : rs > 35 ? 'text-amber-400' : 'text-emerald-400'}`}>{rs}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm">
                      <div className="flex items-center justify-end gap-3 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button 
                          onClick={(e) => { e.stopPropagation(); setSelectedAnalysis(item); }}
                          className="p-2 text-slate-400 hover:text-indigo-400 hover:bg-indigo-500/10 rounded-lg transition-colors"
                          title="View Details"
                        >
                          <Eye size={18} />
                        </button>
                        <button 
                          onClick={(e) => deleteRecord(item._id, e)}
                          className="p-2 text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition-colors"
                          title="Delete Record"
                        >
                          <Trash2 size={18} />
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan={5} className="px-6 py-12 text-center text-slate-500">
                  <div className="flex flex-col items-center justify-center">
                    <Filter className="mb-3 text-slate-600" size={32} />
                    <p>No analysis records found matching your filters.</p>
                  </div>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Modal Overlay for Details */}
      {selectedAnalysis && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm transition-all" onClick={() => setSelectedAnalysis(null)}>
          <div className="relative w-full max-w-4xl max-h-[90vh] overflow-y-auto custom-scrollbar bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl" onClick={e => e.stopPropagation()}>
            <button 
              onClick={() => setSelectedAnalysis(null)}
              className="absolute top-4 right-4 z-10 p-2 bg-slate-950/50 rounded-full text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            >
              <X size={20} />
            </button>
            <div className="p-1 border-b border-slate-800 rounded-t-2xl">
              {/* Inherit the newly built ResultCard visually */}
              <ResultCard data={selectedAnalysis} />
            </div>
            {/* Display raw text context block directly inside the modal */}
            <div className="p-8">
               <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400 mb-4">Raw Resume Text Block</h3>
               <div className="bg-slate-950 p-6 rounded-xl border border-slate-800 text-sm text-slate-300 whitespace-pre-wrap font-mono h-[300px] overflow-y-auto">
                 {selectedAnalysis.resumeText}
               </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
