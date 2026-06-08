import { useState } from "react";
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

// Dynamically requests relative paths when sharing the same host domain layout on Vercel
const API_BASE_URL = import.meta.env.VITE_API_URL || "";

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

    try {
      const response = await fetch(`${API_BASE_URL}/api/research`, {
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
        throw new Error(`Research failed: ${response.status}`);
      }

      const data: ResearchResult = await response.json();
      setResults(data);
    } catch (err: unknown) {
      setError(
        err instanceof Error ? err.message : "Unexpected error occurred"
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

            {results && !loading && (
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