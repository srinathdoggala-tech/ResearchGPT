import { useState } from "react";
import SearchForm from "./components/SearchForm";
import ResultsDisplay from "./components/ResultsDisplay";
import LoadingSpinner from "./components/LoadingSpinner";
import InteractiveBackground from "./components/InteractiveBackground";

interface ResearchPlan {
  research_questions: string[];
  research_plan?: Array<{
    step: number;
    task: string;
    key_focus: string;
  }>;
  estimated_duration?: string;
}

interface ResearchFindings {
  findings: string;
  sources: Array<{
    title: string;
    url: string;
    snippet: string;
  }>;
}

interface ResearchReport {
  report: string;
  word_count: number;
  topic?: string;
  style?: string;
}

interface ResearchResult {
  status: string;
  topic: string;
  plan: ResearchPlan;
  findings: ResearchFindings;
  verification: any;
  report: ResearchReport;
}

const API_BASE_URL =
  import.meta.env.VITE_API_URL ||
  "http://localhost:8001";

function App() {
  const [results, setResults] = useState<ResearchResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentTopic, setCurrentTopic] = useState("");
  const [theme, setTheme] = useState<"dark" | "light">("dark");

  const handleSearch = async (
    topic: string,
    style: string,
    includeVerification: boolean
  ) => {
    setLoading(true);
    setError(null);
    setCurrentTopic(topic);

    const runningResult: ResearchResult = {
      status: "processing",
      topic,
      plan: { research_questions: [] },
      findings: {
        findings: "GATHERING FINDINGS...",
        sources: [],
      },
      verification: null,
      report: {
        report: "",
        word_count: 0,
      },
    };

    try {
      const response = await fetch(`${API_BASE_URL}/api/research/stream`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          topic,
          style,
          include_verification: includeVerification,
        }),
      });

      if (!response.ok) {
        throw new Error(
          `Research stream initialization failed: ${response.status}`
        );
      }

      if (!response.body) {
        throw new Error(
          "ReadableStream not supported by the hosting gateway."
        );
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let finished = false;
      let buffer = "";

      while (!finished) {
        const { value, done } = await reader.read();

        finished = done;

        if (value) {
          buffer += decoder.decode(value, {
            stream: !done,
          });

          const lines = buffer.split("\n");

          buffer = lines.pop() || "";

          for (const line of lines) {
            const cleanLine = line.trim();

            if (!cleanLine.startsWith("data: ")) continue;

            try {
              const rawJson = cleanLine.replace("data: ", "");
              const parsed = JSON.parse(rawJson);

              if (parsed.error) {
                throw new Error(parsed.error);
              }

              if (parsed.type === "status") {
                runningResult.status = parsed.status || parsed.content;
              } else if (parsed.type === "plan") {
                runningResult.plan = parsed.plan;
              } else if (parsed.type === "findings") {
                runningResult.findings = parsed.findings;
              } else if (parsed.type === "verification") {
                runningResult.verification = parsed.verification;
              } else if (parsed.type === "report" || parsed.content) {
                const textChunk = parsed.content || "";
                if (
                  textChunk.includes("📋") ||
                  textChunk.includes("🔍") ||
                  textChunk.includes("✓") ||
                  textChunk.includes("✍️")
                ) {
                  if (textChunk.includes("📋")) runningResult.status = "Planning...";
                  if (textChunk.includes("🔍")) runningResult.status = "Searching Web...";
                  if (textChunk.includes("✓")) runningResult.status = "Fact Checking...";
                  if (textChunk.includes("✍️")) runningResult.status = "Writing Final Report...";
                } else {
                  runningResult.report.report += textChunk;
                  runningResult.report.word_count =
                    runningResult.report.report
                      .split(/\s+/)
                      .filter(Boolean).length;
                }
              }

              setResults({ ...runningResult });
            } catch {
              // Ignore partial stream chunks
            }
          }
        }
      }

      runningResult.status = "success";
      setResults({ ...runningResult });
    } catch (err: unknown) {
      setError(
        err instanceof Error
          ? err.message
          : "Unexpected stream network error occurred"
      );

      setResults(null);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickSearch = async (topic: string) => {
    setLoading(true);
    setError(null);
    setCurrentTopic(topic);

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/research/quick?topic=${encodeURIComponent(
          topic
        )}&max_results=5`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        throw new Error(`Quick research failed: ${response.status}`);
      }

      const data = await response.json();

      setResults({
        status: "success",
        topic,
        plan: {
          research_questions: [],
        },
        findings: {
          findings: data?.findings ?? "",
          sources: data?.sources ?? [],
        },
        verification: null,
        report: {
          report: data?.findings ?? "",
          word_count: data?.findings
            ? String(data.findings).split(/\s+/).filter(Boolean).length
            : 0,
        },
      });
    } catch (err: unknown) {
      setError(
        err instanceof Error
          ? err.message
          : "Unexpected error occurred"
      );

      setResults(null);
    } finally {
      setLoading(false);
    }
  };

  const isDark = theme === "dark";

  return (
    <div
      className={`min-h-screen relative transition-colors duration-500 selection:bg-indigo-500 selection:text-white ${
        isDark
          ? "bg-slate-950 text-slate-100"
          : "bg-slate-50 text-slate-800"
      }`}
    >
      {/* Interactive Background Canvas */}
      <InteractiveBackground isSearching={loading} theme={theme} />

      {/* Main Header */}
      <header
        className={`sticky top-0 z-40 backdrop-blur-xl border-b transition-colors duration-500 ${
          isDark
            ? "bg-slate-950/70 border-slate-800/80 shadow-2xl shadow-indigo-950/20"
            : "bg-white/70 border-slate-200 shadow-md shadow-slate-200/50"
        }`}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-500 p-0.5 shadow-lg shadow-indigo-500/30 animate-gradient">
              <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
                <span className="text-xl">⚡</span>
              </div>
            </div>

            <div>
              <div className="flex items-center space-x-2">
                <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 via-purple-300 to-pink-400">
                  ResearchGPT
                </h1>
                <span className="px-2.5 py-0.5 text-xs font-semibold rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                  v1.0 Multi-Agent
                </span>
              </div>
              <p className="text-xs sm:text-sm text-slate-400 font-medium">
                Autonomous Deep-Research & Fact Verification Engine
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            {/* Live Agent Status Indicator */}
            <div className="hidden md:flex items-center space-x-2 px-3 py-1.5 rounded-full bg-slate-900/60 border border-slate-800 text-xs">
              <span className="relative flex h-2.5 w-2.5">
                <span
                  className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
                    loading ? "bg-amber-400" : "bg-emerald-400"
                  }`}
                ></span>
                <span
                  className={`relative inline-flex rounded-full h-2.5 w-2.5 ${
                    loading ? "bg-amber-500" : "bg-emerald-500"
                  }`}
                ></span>
              </span>
              <span className="text-slate-300 font-mono text-[11px]">
                {loading ? "Agent Active..." : "Agents Ready"}
              </span>
            </div>

            {/* Theme Toggle Button */}
            <button
              onClick={() => setTheme(isDark ? "light" : "dark")}
              className={`p-2.5 rounded-xl border transition-all duration-300 hover:scale-105 active:scale-95 ${
                isDark
                  ? "bg-slate-900 border-slate-800 text-amber-400 hover:bg-slate-800 hover:border-slate-700"
                  : "bg-white border-slate-200 text-slate-700 hover:bg-slate-100 hover:border-slate-300 shadow-sm"
              }`}
              title="Toggle theme mode"
            >
              {isDark ? "☀️ Light Mode" : "🌙 Dark Mode"}
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Layout */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8 relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left Column: Form Controls */}
          <div className="lg:col-span-4">
            <div
              className={`rounded-2xl p-6 sticky top-24 transition-all duration-500 ${
                isDark
                  ? "glass-panel"
                  : "glass-panel-light shadow-xl shadow-indigo-100"
              }`}
            >
              <div className="flex items-center justify-between mb-6 pb-4 border-b border-slate-800/50">
                <h2 className="text-xl font-bold tracking-wide flex items-center gap-2">
                  <span>🚀</span> Launch Research
                </h2>
                <span className="text-xs text-indigo-400 bg-indigo-500/10 px-2.5 py-1 rounded-md border border-indigo-500/20 font-mono">
                  Gemini Flash 2.5
                </span>
              </div>

              <SearchForm
                onSearch={handleSearch}
                onQuickSearch={handleQuickSearch}
                loading={loading}
              />
            </div>
          </div>

          {/* Right Column: Display Panel */}
          <div className="lg:col-span-8">
            {loading && (
              <div className="transition-all duration-300">
                <LoadingSpinner currentTopic={currentTopic} />
              </div>
            )}

            {error && (
              <div className="rounded-2xl p-6 bg-red-950/60 border border-red-800/60 text-red-200 backdrop-blur-md shadow-2xl mb-8 animate-shake">
                <div className="flex items-center space-x-3 mb-2">
                  <span className="text-2xl">⚠️</span>
                  <h3 className="font-bold text-lg text-red-300">
                    Execution Error
                  </h3>
                </div>
                <p className="text-sm opacity-90 font-mono bg-red-900/40 p-3 rounded-lg border border-red-800/40">
                  {error}
                </p>
              </div>
            )}

            {results && (
              <div className="transition-all duration-500">
                <ResultsDisplay results={results} />
              </div>
            )}

            {!loading && !error && !results && (
              <div
                className={`rounded-2xl p-12 text-center transition-all duration-500 ${
                  isDark
                    ? "glass-panel border-dashed border-slate-800/80"
                    : "glass-panel-light border-dashed border-slate-300"
                }`}
              >
                <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-tr from-indigo-500/20 to-purple-500/20 flex items-center justify-center border border-indigo-500/30">
                  <span className="text-3xl animate-bounce">💡</span>
                </div>
                <h3 className="text-xl font-bold mb-2">
                  Ready to Start Deep Research
                </h3>
                <p className="text-slate-400 text-sm max-w-md mx-auto">
                  Enter any complex query or topic on the left panel. Our
                  Planner, Researcher, Verifier, and Technical Writer agents
                  will generate a comprehensive structured report in real time.
                </p>

                <div className="mt-8 flex flex-wrap justify-center gap-2">
                  {[
                    "Quantum Computing Trends 2026",
                    "AGI Safety Alignment Models",
                    "Fusion Energy Commercialization",
                  ].map((presetTopic) => (
                    <button
                      key={presetTopic}
                      onClick={() => handleSearch(presetTopic, "academic", true)}
                      className={`text-xs px-3.5 py-2 rounded-xl transition-all duration-200 border ${
                        isDark
                          ? "bg-slate-900/80 hover:bg-indigo-950/80 border-slate-800 hover:border-indigo-600 text-slate-300 hover:text-indigo-200"
                          : "bg-white hover:bg-indigo-50 border-slate-200 hover:border-indigo-300 text-slate-700 hover:text-indigo-700 shadow-sm"
                      }`}
                    >
                      ✨ {presetTopic}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;