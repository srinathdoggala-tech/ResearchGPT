import React from 'react'

interface LoadingSpinnerProps {
  currentTopic: string
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ currentTopic }) => {
  const steps = [
    { name: 'Planning', emoji: '📋' },
    { name: 'Researching', emoji: '🔍' },
    { name: 'Verifying', emoji: '✓' },
    { name: 'Writing', emoji: '✍️' },
  ]

  return (
    <div className="bg-white rounded-lg shadow-lg p-8">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Researching: {currentTopic}</h2>
        <p className="text-gray-600">AI agents are working on your research...</p>
      </div>

      <div className="space-y-4 mb-8">
        {steps.map((step, index) => (
          <div key={index} className="flex items-center">
            <div className="w-8 h-8 bg-indigo-600 text-white rounded-full flex items-center justify-center mr-4">
              <span className="text-lg">{step.emoji}</span>
            </div>
            <span className="text-gray-700 font-medium">{step.name}</span>
            <div className="flex-1 ml-4">
              <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-indigo-600 animate-pulse"
                  style={{
                    animation: 'pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                    width: '100%',
                  }}
                />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="flex justify-center">
        <div className="animate-spin">
          <div className="w-12 h-12 border-4 border-indigo-200 border-t-indigo-600 rounded-full" />
        </div>
      </div>
    </div>
  )
}

export default LoadingSpinner
