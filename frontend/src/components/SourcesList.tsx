import React from 'react'

interface SourcesListProps {
  sources: Array<{
    title: string
    url: string
    snippet: string
  }>
}

const SourcesList: React.FC<SourcesListProps> = ({ sources }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">Sources</h3>
      <div className="space-y-3">
        {sources.map((source, index) => (
          <div key={index} className="border-l-4 border-blue-500 pl-4 py-2">
            <a
              href={source.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline font-semibold"
            >
              {source.title}
            </a>
            <p className="text-sm text-gray-600 mt-1">{source.snippet}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default SourcesList
