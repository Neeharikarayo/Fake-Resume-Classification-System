'use client';

import { CheckCircle2, AlertTriangle, XCircle, Info, ShieldAlert } from 'lucide-react';

interface ResultCardProps {
  data: {
    prediction: 'Genuine' | 'Fake' | 'Suspicious';
    confidence: number;
    issues: string[];
    details: {
      skill_count: number;
      word_count: number;
      experience_years: number;
      graduation_year: number;
      skill_experience_ratio: number;
      timeline_issue: boolean;
      too_many_skills: boolean;
    };
  };
}

const ResultCard = ({ data }: ResultCardProps) => {
  const getStatusConfig = () => {
    switch (data.prediction) {
      case 'Genuine':
        return {
          icon: <CheckCircle2 className="text-emerald-400" size={32} />,
          badgeClass: 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30',
          gradient: 'from-emerald-500 to-teal-400',
        };
      case 'Fake':
        return {
          icon: <XCircle className="text-rose-400" size={32} />,
          badgeClass: 'bg-rose-500/20 text-rose-400 border border-rose-500/30',
          gradient: 'from-rose-500 to-pink-500',
        };
      case 'Suspicious':
        return {
          icon: <AlertTriangle className="text-amber-400" size={32} />,
          badgeClass: 'bg-amber-500/20 text-amber-400 border border-amber-500/30',
          gradient: 'from-amber-500 to-yellow-400',
        };
      default:
        return {
          icon: <Info className="text-slate-400" size={32} />,
          badgeClass: 'bg-slate-800 text-slate-300 border border-slate-700',
          gradient: 'from-slate-500 to-slate-400',
        };
    }
  };

  const getRiskScore = () => {
    if (data.prediction === 'Fake') return Math.min(100, Math.round(data.confidence * 100));
    if (data.prediction === 'Genuine') return Math.max(0, Math.round((1 - data.confidence) * 100));
    return Math.round(data.confidence * 100); 
  };

  const config = getStatusConfig();
  const riskScore = getRiskScore();

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl shadow-xl overflow-hidden group">
      {/* Top Gradient Bar */}
      <div className={`h-1.5 w-full bg-gradient-to-r ${config.gradient}`} />

      <div className="p-6 md:p-8">
        <div className="flex flex-col md:flex-row gap-6 items-start md:items-center justify-between mb-8 border-b border-slate-800/50 pb-8">
          <div className="flex items-center gap-4">
            <div className={`p-4 rounded-xl bg-slate-950/50 border border-slate-800 shadow-inner`}>
              {config.icon}
            </div>
            <div>
              <p className="text-sm text-slate-400 font-medium mb-1">AI Classification</p>
              <div className="flex items-center gap-3">
                <span className={`px-4 py-1 rounded-full text-sm font-bold tracking-wide uppercase ${config.badgeClass}`}>
                  {data.prediction}
                </span>
                <span className="text-slate-300 font-medium bg-slate-800/50 px-3 py-1 rounded-full text-sm border border-slate-700/50">
                  {(data.confidence * 100).toFixed(1)}% Confidence
                </span>
              </div>
            </div>
          </div>

          {/* Risk Score Bar */}
          <div className="w-full md:w-64 bg-slate-950/50 p-4 rounded-xl border border-slate-800/60">
            <div className="flex justify-between items-end mb-2">
              <span className="text-sm font-bold text-slate-300 flex items-center gap-2">
                <ShieldAlert size={16} className={riskScore > 65 ? 'text-rose-400' : riskScore > 35 ? 'text-amber-400' : 'text-emerald-400'} /> 
                Risk Score
              </span>
              <span className={`text-xl font-black ${riskScore > 65 ? 'text-rose-400' : riskScore > 35 ? 'text-amber-400' : 'text-emerald-400'}`}>
                {riskScore}/100
              </span>
            </div>
            <div className="h-2.5 w-full bg-slate-800 rounded-full overflow-hidden">
              <div 
                className={`h-full rounded-full bg-gradient-to-r ${
                  riskScore > 65 ? 'from-rose-500 to-red-500' : 
                  riskScore > 35 ? 'from-amber-400 to-yellow-500' : 
                  'from-emerald-400 to-teal-500'
                } transition-all duration-1000 ease-out`}
                style={{ width: `${riskScore}%` }}
              />
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-slate-950/40 border border-slate-800 p-5 rounded-xl flex flex-col items-center justify-center text-center transition-all duration-200 hover:bg-slate-800/40">
            <p className="text-xs text-slate-400 uppercase tracking-widest mb-2 font-semibold">Total Skills</p>
            <p className="text-3xl font-bold text-white bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400">
              {data.details.skill_count}
            </p>
          </div>
          <div className="bg-slate-950/40 border border-slate-800 p-5 rounded-xl flex flex-col items-center justify-center text-center transition-all duration-200 hover:bg-slate-800/40">
            <p className="text-xs text-slate-400 uppercase tracking-widest mb-2 font-semibold">Experience</p>
            <p className="text-3xl font-bold text-white">{data.details.experience_years} <span className="text-base font-medium text-slate-500">yrs</span></p>
          </div>
          <div className="bg-slate-950/40 border border-slate-800 p-5 rounded-xl flex flex-col items-center justify-center text-center transition-all duration-200 hover:bg-slate-800/40">
            <p className="text-xs text-slate-400 uppercase tracking-widest mb-2 font-semibold">Skill Density</p>
            <p className="text-3xl font-bold text-white">{data.details.skill_experience_ratio}</p>
          </div>
          <div className="bg-slate-950/40 border border-slate-800 p-5 rounded-xl flex flex-col items-center justify-center text-center transition-all duration-200 hover:bg-slate-800/40">
            <p className="text-xs text-slate-400 uppercase tracking-widest mb-2 font-semibold">Graduation</p>
            <p className="text-3xl font-bold text-white">{data.details.graduation_year || 'N/A'}</p>
          </div>
        </div>

        {data.issues.length > 0 ? (
          <div className="bg-rose-500/5 border border-rose-500/20 rounded-xl p-6">
            <h3 className="text-sm font-bold uppercase tracking-wider text-rose-400 mb-4 flex items-center">
              <AlertTriangle size={18} className="mr-2" /> Detected Red Flags
            </h3>
            <ul className="space-y-3">
              {data.issues.map((issue, idx) => (
                <li key={idx} className="flex items-start text-sm md:text-base text-slate-300 p-3 rounded-lg bg-slate-950/60 border border-rose-500/10 shadow-sm">
                  <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-rose-500/20 text-rose-400 mr-3 flex-shrink-0 text-xs font-bold mt-0.5">
                    {idx + 1}
                  </span>
                  {issue}
                </li>
              ))}
            </ul>
          </div>
        ) : (
           <div className="bg-emerald-500/5 border border-emerald-500/20 rounded-xl p-6 flex items-center gap-4">
             <div className="p-3 bg-emerald-500/10 rounded-full">
                <CheckCircle2 className="text-emerald-400" size={24} />
             </div>
             <div>
                <h3 className="text-sm font-bold uppercase tracking-wider text-emerald-400 mb-1">No Red Flags Detected</h3>
                <p className="text-sm text-slate-400">The AI model did not identify any logical inconsistencies or keyword stuffing patterns in this resume.</p>
             </div>
           </div>
        )}
      </div>
    </div>
  );
};

export default ResultCard;
