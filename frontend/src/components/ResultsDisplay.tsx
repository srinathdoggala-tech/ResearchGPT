import React, { useState } from "react";

interface ResultsDisplayProps {
  results: {
    status: string;
    topic: string;
    plan: any;
    findings: any;
    verification: any;
    report: any;
  };
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ results }) => {
  const [copied, setCopied] = useState(false);

  const handleCopyReport = () => {
    if (results?.report?.report) {
      navigator.clipboard.writeText(results.report.report);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const renderPlan = (plan: any) => (
    <div className="rounded-2xl p-6 glass-panel border border-slate-800/80 mb-6 transition-all duration-300">
      <div className="flex items-center space-x-3 mb-4 pb-3 border-b border-slate-800/60">
        <span className="text-xl">📋</span>
        <h3 className="text-lg font-bold text-slate-100">Research Plan</h3>
      </div>
      <div className="space-y-4 text-sm">
        {plan.research_questions && plan.research_questions.length > 0 && (
          <div>
            <h4 className="font-semibold text-indigo-300 mb-2 text-xs uppercase tracking-wider">
              Core Questions:
            </h4>
            <ul className="space-y-2">
              {plan.research_questions.map((q: string, i: number) => (
                <li key={i} className="flex items-start space-x-2 text-slate-300">
                  <span className="text-indigo-400 font-bold">•</span>
                  <span>{q}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
        {plan.research_plan && plan.research_plan.length > 0 && (
          <div>
            <h4 className="font-semibold text-indigo-300 mb-2 text-xs uppercase tracking-wider">
              Execution Sequence:
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {plan.research_plan.map((step: any, i: number) => (
                <div
                  key={i}
                  className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800/80"
                >
                  <span className="text-xs font-mono px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                    Step {step.step}
                  </span>
                  <p className="font-semibold text-slate-200 mt-2 text-xs">
                    {step.task}
                  </p>
                  <p className="text-[11px] text-slate-400 mt-1">
                    Focus: {step.key_focus}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );

  const renderFindings = (findings: any) => (
    <div className="rounded-2xl p-6 glass-panel border border-slate-800/80 mb-6 transition-all duration-300">
      <div className="flex items-center space-x-3 mb-4 pb-3 border-b border-slate-800/60">
        <span className="text-xl">🔍</span>
        <h3 className="text-lg font-bold text-slate-100">Synthesized Findings</h3>
      </div>
      <div className="space-y-4 text-sm text-slate-300">
        <p className="whitespace-pre-wrap leading-relaxed">{findings.findings}</p>

        {findings.sources && findings.sources.length > 0 && (
          <div className="mt-6 pt-4 border-t border-slate-800/60">
            <h4 className="font-semibold text-indigo-300 mb-3 text-xs uppercase tracking-wider flex items-center gap-2">
              <span>🌐</span> Verified Web Sources ({findings.sources.length})
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {findings.sources.slice(0, 6).map((source: any, i: number) => (
                <div
                  key={i}
                  className="p-3 rounded-xl bg-slate-900/50 border border-slate-800 hover:border-indigo-500/40 transition-all duration-200 group"
                >
                  <a
                    href={source.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xs font-semibold text-indigo-300 group-hover:text-indigo-200 line-clamp-1 flex items-center justify-between"
                  >
                    <span>{source.title || "Web Reference"}</span>
                    <span className="text-[10px] text-slate-500">↗</span>
                  </a>
                  <p className="text-[11px] text-slate-400 mt-1 line-clamp-2">
                    {source.snippet}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );

  const renderVerification = (verification: any) => (
    <div className="rounded-2xl p-6 glass-panel border border-emerald-900/50 bg-emerald-950/20 mb-6 transition-all duration-300">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-emerald-900/40">
        <div className="flex items-center space-x-3">
          <span className="text-xl text-emerald-400">✓</span>
          <h3 className="text-lg font-bold text-emerald-200">Fact Verification</h3>
        </div>
        {verification.overall_reliability && (
          <span className="px-3 py-1 rounded-full text-xs font-mono bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
            Reliability: {verification.overall_reliability}
          </span>
        )}
      </div>
      <div className="space-y-3">
        {verification.verification_results &&
          verification.verification_results.map((result: any, i: number) => (
            <div
              key={i}
              className="bg-emerald-950/40 border border-emerald-800/40 p-4 rounded-xl text-xs space-y-1.5"
            >
              <p className="font-semibold text-emerald-300">
                Claim: "{result.claim}"
              </p>
              <p className="text-slate-300">{result.verification}</p>
            </div>
          ))}
      </div>
    </div>
  );

  const renderReport = (report: any) => (
    <div className="rounded-2xl p-6 glass-panel border border-slate-800/80 mb-6 shadow-2xl transition-all duration-300">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800/60">
        <div className="flex items-center space-x-3">
          <span className="text-xl">📄</span>
          <h3 className="text-lg font-bold text-slate-100">Final Research Report</h3>
        </div>
        <div className="flex items-center space-x-3">
          <span className="text-xs text-slate-400 font-mono">
            {report.word_count || 0} words
          </span>
          <button
            onClick={handleCopyReport}
            className="px-3 py-1.5 rounded-lg text-xs font-medium bg-indigo-600/30 hover:bg-indigo-600/50 border border-indigo-500/40 text-indigo-200 transition active:scale-95"
          >
            {copied ? "✓ Copied!" : "📋 Copy Report"}
          </button>
        </div>
      </div>
      <div className="prose prose-invert prose-sm max-w-none">
        <div className="text-slate-200 whitespace-pre-wrap leading-relaxed font-sans text-sm bg-slate-950/40 p-5 rounded-xl border border-slate-900">
          {report.report}
        </div>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="rounded-2xl p-5 bg-gradient-to-r from-indigo-950/80 via-purple-950/60 to-slate-950/80 border border-indigo-800/50 backdrop-blur-md shadow-xl flex items-center justify-between">
        <div>
          <h2 className="text-xl sm:text-2xl font-extrabold text-slate-100 flex items-center gap-2">
            <span>🎯</span> {results.topic}
          </h2>
          <div className="flex items-center space-x-2 mt-1 text-xs text-indigo-300">
            <span className="font-mono">Status: {results.status}</span>
          </div>
        </div>
      </div>

      {results.plan && Object.keys(results.plan).length > 0 && renderPlan(results.plan)}
      {results.findings && renderFindings(results.findings)}
      {results.verification &&
        Object.keys(results.verification).length > 0 &&
        renderVerification(results.verification)}
      {results.report && renderReport(results.report)}
    </div>
  );
};

export default ResultsDisplay;
