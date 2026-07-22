import React, { useState } from "react";

interface SearchFormProps {
  onSearch: (topic: string, style: string, includeVerification: boolean) => void;
  onQuickSearch: (topic: string) => void;
  loading: boolean;
}

const SearchForm: React.FC<SearchFormProps> = ({
  onSearch,
  onQuickSearch,
  loading,
}) => {
  const [topic, setTopic] = useState("");
  const [style, setStyle] = useState("academic");
  const [includeVerification, setIncludeVerification] = useState(true);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (topic.trim()) {
      onSearch(topic, style, includeVerification);
    }
  };

  const handleQuickSubmit = () => {
    if (topic.trim()) {
      onQuickSearch(topic);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {/* Topic Input */}
      <div>
        <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
          Research Query / Topic
        </label>
        <div className="relative">
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g. Impact of AI on Semiconductor Supply Chains"
            className="w-full px-4 py-3 rounded-xl bg-slate-900/60 border border-slate-700/70 text-slate-100 placeholder-slate-500 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition duration-200 text-sm shadow-inner"
            disabled={loading}
          />
          {topic && (
            <button
              type="button"
              onClick={() => setTopic("")}
              className="absolute right-3 top-3 text-slate-500 hover:text-slate-300 text-xs bg-slate-800 rounded-full w-5 h-5 flex items-center justify-center"
            >
              ✕
            </button>
          )}
        </div>
      </div>

      {/* Writing Style */}
      <div>
        <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
          Report Output Style
        </label>
        <select
          value={style}
          onChange={(e) => setStyle(e.target.value)}
          className="w-full px-4 py-2.5 rounded-xl bg-slate-900/60 border border-slate-700/70 text-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition duration-200 text-sm cursor-pointer"
          disabled={loading}
        >
          <option value="academic" className="bg-slate-900 text-slate-200">
            🎓 Academic & Detailed
          </option>
          <option value="journalistic" className="bg-slate-900 text-slate-200">
            📰 Journalistic & Concise
          </option>
          <option value="summary" className="bg-slate-900 text-slate-200">
            ⚡ Executive Summary
          </option>
        </select>
      </div>

      {/* Verification Toggle */}
      <div className="flex items-center space-x-3 p-3 rounded-xl bg-slate-900/40 border border-slate-800/60">
        <input
          type="checkbox"
          id="verification"
          checked={includeVerification}
          onChange={(e) => setIncludeVerification(e.target.checked)}
          className="w-4 h-4 text-indigo-600 bg-slate-900 border-slate-700 rounded focus:ring-indigo-500 focus:ring-offset-slate-900 cursor-pointer"
          disabled={loading}
        />
        <label
          htmlFor="verification"
          className="text-xs text-slate-300 font-medium cursor-pointer select-none"
        >
          Enable Cross-Source Fact Verification
        </label>
      </div>

      {/* Action Buttons */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
        <button
          type="submit"
          disabled={loading || !topic.trim()}
          className="w-full bg-gradient-to-r from-indigo-600 via-indigo-500 to-purple-600 hover:from-indigo-500 hover:to-purple-500 disabled:opacity-50 text-white font-semibold py-3 px-4 rounded-xl transition duration-300 shadow-lg shadow-indigo-600/30 flex items-center justify-center space-x-2 text-sm active:scale-95"
        >
          <span>{loading ? "⚙️ Processing..." : "🧠 Full Research"}</span>
        </button>

        <button
          type="button"
          onClick={handleQuickSubmit}
          disabled={loading || !topic.trim()}
          className="w-full bg-slate-800 hover:bg-slate-700 border border-slate-700 disabled:opacity-50 text-slate-200 font-semibold py-3 px-4 rounded-xl transition duration-300 flex items-center justify-center space-x-2 text-sm active:scale-95"
        >
          <span>⚡ Quick Search</span>
        </button>
      </div>
    </form>
  );
};

export default SearchForm;
