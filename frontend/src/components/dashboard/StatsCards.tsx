import { Files, AlertTriangle, Activity, ShieldAlert } from 'lucide-react';

interface StatsCardsProps {
  total: number;
  fake: number;
  suspicious: number;
  avgConfidence: number;
}

const StatsCards = ({ total, fake, suspicious, avgConfidence }: StatsCardsProps) => {
  const stats = [
    {
      name: 'Total Resumes Analyzed',
      value: total.toString(),
      icon: Files,
      gradient: 'from-indigo-500/20 to-purple-500/20',
      iconColor: 'text-indigo-400',
    },
    {
      name: 'Fake Resumes Detected',
      value: fake.toString(),
      icon: AlertTriangle,
      gradient: 'from-rose-500/20 to-pink-500/20',
      iconColor: 'text-rose-400',
    },
    {
      name: 'Suspicious Resumes',
      value: suspicious.toString(),
      icon: ShieldAlert,
      gradient: 'from-amber-500/20 to-yellow-500/20',
      iconColor: 'text-amber-400',
    },
    {
      name: 'Average AI Confidence',
      value: total > 0 ? `${(avgConfidence * 100).toFixed(1)}%` : '0%',
      icon: Activity,
      gradient: 'from-emerald-500/20 to-teal-500/20',
      iconColor: 'text-emerald-400',
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
      {stats.map((stat) => {
        const Icon = stat.icon;
        return (
          <div key={stat.name} className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex items-center shadow-lg transition-all duration-300 hover:shadow-indigo-500/10 hover:border-slate-700 hover:-translate-y-1">
            <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${stat.gradient} flex items-center justify-center mr-4 flex-shrink-0`}>
              <Icon className={stat.iconColor} size={24} />
            </div>
            <div>
              <p className="text-sm font-medium text-slate-400">{stat.name}</p>
              <h3 className="text-2xl font-bold text-white mt-1">{stat.value}</h3>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default StatsCards;
