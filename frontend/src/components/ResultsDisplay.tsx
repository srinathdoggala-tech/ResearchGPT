import React from 'react'

interface ResultsDisplayProps {
  results: {
    status: string
    topic: string
    plan: any
    findings: any
    verification: any
    report: any
  }
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ results }) => {
  const renderPlan = (plan: any) => (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">📋 Research Plan</h3>
      <div className="space-y-4">
        {plan.research_questions && (
          <div>
            <h4 className="font-semibold text-gray-700 mb-2">Research Questions:</h4>
            <ul className="list-disc list-inside space-y-1">
              {plan.research_questions.map((q: string, i: number) => (
                <li key={i} className="text-gray-600">
                  {q}
                </li>
              ))}
            </ul>
          </div>
        )}
        {plan.research_plan && (
          <div>
            <h4 className="font-semibold text-gray-700 mb-2">Steps:</h4>
            <div className="space-y-2">
              {plan.research_plan.map((step: any, i: number) => (
                <div key={i} className="bg-indigo-50 p-3 rounded">
                  <strong className="text-indigo-700">Step {step.step}:</strong> {step.task}
                  <p className="text-sm text-gray-600 mt-1">Focus: {step.key_focus}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )

  const renderFindings = (findings: any) => (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">🔍 Research Findings</h3>
      <div className="space-y-4">
        <div>
          <p className="text-gray-700 whitespace-pre-wrap">{findings.findings}</p>
        </div>
        {findings.sources && findings.sources.length > 0 && (
          <div>
            <h4 className="font-semibold text-gray-700 mb-2">Sources:</h4>
            <div className="space-y-2">
              {findings.sources.slice(0, 5).map((source: any, i: number) => (
                <div key={i} className="border-l-4 border-indigo-500 pl-3 py-1">
                  <a
                    href={source.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline font-medium"
                  >
                    {source.title}
                  </a>
                  <p className="text-sm text-gray-600">{source.snippet}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )

  const renderVerification = (verification: any) => (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">✓ Verification Results</h3>
      <div className="space-y-4">
        {verification.verification_results && (
          <div className="space-y-3">
            {verification.verification_results.map((result: any, i: number) => (
              <div key={i} className="bg-green-50 border border-green-200 p-4 rounded">
                <p className="font-semibold text-green-900">Claim: {result.claim}</p>
                <p className="text-sm text-gray-700 mt-2">{result.verification}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )

  const renderReport = (report: any) => (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">📄 Research Report</h3>
      <div className="space-y-4">
        <p className="text-sm text-gray-500">Word Count: {report.word_count} words</p>
        <div className="prose prose-sm max-w-none">
          <p className="text-gray-700 whitespace-pre-wrap">{report.report}</p>
        </div>
      </div>
    </div>
  )

  return (
    <div className="space-y-6">
      <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-4">
        <h2 className="text-2xl font-bold text-indigo-900">Research Results for: {results.topic}</h2>
        <p className="text-indigo-700 text-sm mt-1">Status: {results.status}</p>
      </div>

      {results.plan && Object.keys(results.plan).length > 0 && renderPlan(results.plan)}
      {results.findings && renderFindings(results.findings)}
      {results.verification && Object.keys(results.verification).length > 0 && renderVerification(results.verification)}
      {results.report && renderReport(results.report)}
    </div>
  )
}

export default ResultsDisplay
