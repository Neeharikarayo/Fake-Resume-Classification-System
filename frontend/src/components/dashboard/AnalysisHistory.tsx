'use client';

import { History, Loader2, ChevronRight, CheckCircle2, XCircle, AlertTriangle } from 'lucide-react';

interface AnalysisHistoryProps {
  history: any[];
  isLoading: boolean;
  onSelectResult: (data: any) => void;
}

const AnalysisHistory = ({ history, isLoading, onSelectResult }: AnalysisHistoryProps) => {
  const getRiskScore = (prediction: string, confidence: number) => {
    if (prediction === 'Fake') return Math.min(100, Math.round(confidence * 100));
    if (prediction === 'Genuine') return Math.max(0, Math.round((1 - confidence) * 100));
    return Math.round(confidence * 100); 
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl h-full flex flex-col">
      <div className="p-6 border-b border-slate-800/80 flex items-center justify-between bg-slate-900/50">
        <div className="flex items-center space-x-3 text-white">
          <div className="p-2 bg-purple-500/10 rounded-lg border border-purple-500/20">
            <History size={20} className="text-purple-400" />
          </div>
          <h2 className="text-lg font-bold">Recent Analysis History</h2>
        </div>
      </div>

      <div className="flex-1 overflow-hidden">
        {isLoading ? (
          <div className="flex justify-center flex-col items-center p-12 h-full gap-4 text-slate-500">
            <Loader2 className="animate-spin text-purple-500" size={32} />
            <span className="text-sm font-medium">Loading history...</span>
          </div>
        ) : history.length > 0 ? (
          <div className="divide-y divide-slate-800/50">
            {history.map((item) => {
              const rs = getRiskScore(item.prediction, item.confidence);
              return (
                <div 
                  key={item._id} 
                  className="group px-6 py-4 cursor-pointer hover:bg-slate-800/40 transition-all duration-300 flex flex-col sm:flex-row sm:items-center justify-between gap-4"
                  onClick={() => onSelectResult(item)}
                >
                  <div className="flex items-center gap-4 flex-1">
                    <div className="flex-shrink-0 p-2 bg-slate-950 rounded-xl border border-slate-800 group-hover:border-slate-700 transition-colors">
                       {item.prediction === 'Genuine' ? <CheckCircle2 className="text-emerald-400" size={24} /> :
                        item.prediction === 'Fake' ? <XCircle className="text-rose-400" size={24} /> :
                        <AlertTriangle className="text-amber-400" size={24} />}
                    </div>
                    <div>
                      <div className="flex items-center gap-3 mb-1.5">
                        <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider border ${
                          item.prediction === 'Genuine' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
                          item.prediction === 'Fake' ? 'bg-rose-500/10 text-rose-400 border-rose-500/20' :
                          'bg-amber-500/10 text-amber-400 border-amber-500/20'
                        }`}>
                          {item.prediction}
                        </span>
                        <span className="text-xs text-slate-500 font-medium whitespace-nowrap">
                          {new Date(item.createdAt).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}
                        </span>
                      </div>
                      <div className="text-sm text-slate-300 font-medium">
                        AI Match Confidence: <span className="text-white font-bold ml-1">{(item.confidence * 100).toFixed(1)}%</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-6 sm:justify-end mt-2 sm:mt-0">
                    <div className="flex flex-col items-start sm:items-end w-32">
                      <span className="text-[10px] text-slate-500 uppercase tracking-widest font-semibold mb-1.5">Risk Score</span>
                      <div className="flex items-center gap-2 w-full">
                        <div className="h-1.5 flex-1 bg-slate-800 flex rounded-full overflow-hidden shrink-0">
                          <div 
                            className={`h-full rounded-full ${rs > 65 ? 'bg-gradient-to-r from-rose-500 to-red-500' : rs > 35 ? 'bg-gradient-to-r from-amber-400 to-yellow-500' : 'bg-gradient-to-r from-emerald-400 to-teal-500'}`}
                            style={{ width: `${rs}%` }}
                          />
                        </div>
                        <span className={`text-xs font-bold w-6 text-right shrink-0 ${rs > 65 ? 'text-rose-400' : rs > 35 ? 'text-amber-400' : 'text-emerald-400'}`}>{rs}</span>
                      </div>
                    </div>
                    
                    <div className="w-8 h-8 rounded-full bg-slate-800/50 flex items-center justify-center text-slate-400 group-hover:bg-purple-500/20 group-hover:text-purple-400 transition-colors flex-shrink-0">
                      <ChevronRight size={16} />
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-16 px-6 text-center">
            <div className="w-16 h-16 bg-slate-800/50 rounded-full flex items-center justify-center mb-4 border border-slate-700/50">
              <History className="text-slate-600" size={28} />
            </div>
            <h3 className="text-lg font-medium text-white mb-2">No History Yet</h3>
            <p className="text-slate-500 text-sm max-w-sm">Analyze some resumes to see your recent history appear here.</p>
          </div>
        )}
      </div>
      
      {!isLoading && history.length > 0 && (
         <div className="p-4 border-t border-slate-800/80 bg-slate-900/30 text-center">
            <button 
              onClick={(e) => {
                e.stopPropagation();
                onSelectResult({}); // Handled by parent to route to full history
              }} 
              className="text-sm font-medium text-purple-400 hover:text-purple-300 transition-colors py-2 px-4 rounded-lg hover:bg-purple-500/10 inline-flex items-center"
            >
              View Full History <ChevronRight size={14} className="ml-1" />
            </button>
         </div>
      )}
    </div>
  );
};

export default AnalysisHistory;
