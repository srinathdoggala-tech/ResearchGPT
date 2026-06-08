import React, { useState } from "react";
import SearchForm from "./components/SearchForm";
import ResultsDisplay from "./components/ResultsDisplay";
import LoadingSpinner from "./components/LoadingSpinner";

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

const API_BASE_URL = (import.meta as any).env?.VITE_API_URL || "";

function App() {
  const [results, setResults] = useState<ResearchResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentTopic, setCurrentTopic] = useState("");

  const handleSearch = async (
    topic: string,
    style: string,
    includeVerification: boolean
  ) => {
    setLoading(true);
    setError(null);
    setCurrentTopic(topic);
    
    // Initialize a clean default result structure to append streamed results safely
    const runningResult: ResearchResult = {
      status: "processing",
      topic,
      plan: { research_questions: [] },
      findings: { findings: "GATHERING FINDINGS...", sources: [] },
      verification: null,
      report: { report: "", word_count: 0 }
    };

    try {
      // Connect directly to the streaming endpoint to bypass Vercel serverless timeouts
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
        throw new Error(`Research stream initialization failed: ${response.status}`);
      }

      if (!response.body) {
        throw new Error("ReadableStream not supported by the hosting gateway.");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let finished = false;
      let buffer = "";

      while (!finished) {
        const { value, done } = await reader.read();
        finished = done;
        if (value) {
          buffer += decoder.decode(value, { stream: !done });
          const lines = buffer.split("\n");
          
          // Save the last incomplete line back to the chunk buffer
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

              // Append streamed output data blocks securely into the interface display wrapper
              if (parsed.content) {
                runningResult.report.report += parsed.content;
                runningResult.report.word_count = runningResult.report.report.split(/\s+/).filter(Boolean).length;
                
                // Keep status text moving during step checkpoints
                if (parsed.content.includes("📋")) runningResult.status = "Planning...";
                if (parsed.content.includes("🔍")) runningResult.status = "Searching Web...";
                if (parsed.content.includes("✓")) runningResult.status = "Fact Checking...";
                if (parsed.content.includes("✍️")) runningResult.status = "Writing Final Report...";

                setResults({ ...runningResult });
              }
            } catch (e) {
              // Ignore partial chunk syntax errors during transit
            }
          }
        }
      }
      
      // Mark workflow as successfully finalized once stream returns closed state
      runningResult.status = "success";
      setResults({ ...runningResult });

    } catch (err: unknown) {
      setError(
        err instanceof Error ? err.message : "Unexpected stream network error occurred"
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
        plan: { research_questions: [] },
        findings: {
          findings: data?.findings ?? "",
          sources: data?.sources ?? []
        },
        verification: null,
        report: {
          report: data?.findings ?? "",
          word_count: data?.findings ? String(data.findings).split(/\s+/).filter(Boolean).length : 0
        },
      });
    } catch (err: unknown) {
      setError(
        err instanceof Error ? err.message : "Unexpected error occurred"
      );
      setResults(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-4xl font-bold text-indigo-600">
            ResearchGPT
          </h1>
          <p className="text-gray-600 mt-2">
            Multi-Agent AI Research Assistant
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-lg p-6 sticky top-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">
                Research
              </h2>

              <SearchForm
                onSearch={handleSearch}
                onQuickSearch={handleQuickSearch}
                loading={loading}
              />
            </div>
          </div>

          <div className="lg:col-span-2">
            {loading && (
              <LoadingSpinner currentTopic={currentTopic} />
            )}

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">
                <h3 className="font-bold mb-2">Error</h3>
                <p>{error}</p>
              </div>
            )}

            {results && (
              <ResultsDisplay results={results} />
            )}

            {!loading && !error && !results && (
              <div className="bg-white rounded-lg shadow-lg p-8 text-center">
                <p className="text-gray-500 text-lg">
                  Enter a topic and start researching to see results here.
                </p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;