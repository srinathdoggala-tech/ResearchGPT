import React from "react";

interface LoadingSpinnerProps {
  currentTopic: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ currentTopic }) => {
  const steps = [
    { name: "Planner Agent", action: "Structuring questions & scope", emoji: "📋" },
    { name: "Researcher Agent", action: "Querying Tavily Web Index", emoji: "🔍" },
    { name: "Verifier Agent", action: "Fact-checking claims & evidence", emoji: "✓" },
    { name: "Writer Agent", action: "Synthesizing report text", emoji: "✍️" },
  ];

  return (
    <div className="rounded-2xl p-8 glass-panel border border-indigo-500/30 shadow-2xl backdrop-blur-xl mb-8 relative overflow-hidden">
      {/* Background glow orb */}
      <div className="absolute -right-20 -top-20 w-64 h-64 bg-indigo-600/20 rounded-full blur-3xl pointer-events-none animate-pulse"></div>

      <div className="text-center mb-8 relative z-10">
        <span className="px-3 py-1 rounded-full text-xs font-mono bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 mb-3 inline-block animate-pulse">
          ⚡ Multi-Agent Pipeline Active
        </span>
        <h2 className="text-xl sm:text-2xl font-bold text-slate-100 mb-2">
          Researching: <span className="text-indigo-400">"{currentTopic}"</span>
        </h2>
        <p className="text-xs text-slate-400">
          Autonomous agents are executing research, fact checking, and report synthesis...
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8 relative z-10">
        {steps.map((step, index) => (
          <div
            key={index}
            className="flex items-center p-3.5 rounded-xl bg-slate-900/60 border border-slate-800/80 hover:border-indigo-500/40 transition-all duration-300"
          >
            <div className="w-10 h-10 rounded-xl bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 flex items-center justify-center mr-3 shrink-0 shadow-lg shadow-indigo-500/10">
              <span className="text-lg">{step.emoji}</span>
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-200 truncate">
                  {step.name}
                </span>
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span>
                </span>
              </div>
              <p className="text-[11px] text-slate-400 truncate mt-0.5">
                {step.action}
              </p>
            </div>
          </div>
        ))}
      </div>

      <div className="flex flex-col items-center justify-center relative z-10 pt-2">
        <div className="w-12 h-12 rounded-full border-2 border-indigo-500/20 border-t-indigo-500 animate-spin flex items-center justify-center">
          <div className="w-6 h-6 rounded-full border-2 border-purple-500/20 border-b-purple-400 animate-spin"></div>
        </div>
        <span className="text-xs font-mono text-slate-400 mt-3 animate-pulse">
          Streaming output...
        </span>
      </div>
    </div>
  );
};

export default LoadingSpinner;
