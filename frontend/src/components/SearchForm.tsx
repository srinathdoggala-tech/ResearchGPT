import React, { useState } from 'react'

interface SearchFormProps {
  onSearch: (topic: string, style: string, includeVerification: boolean) => void
  onQuickSearch: (topic: string) => void
  loading: boolean
}

const SearchForm: React.FC<SearchFormProps> = ({ onSearch, onQuickSearch, loading }) => {
  const [topic, setTopic] = useState('')
  const [style, setStyle] = useState('academic')
  const [includeVerification, setIncludeVerification] = useState(true)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (topic.trim()) {
      onSearch(topic, style, includeVerification)
    }
  }

  const handleQuickSubmit = () => {
    if (topic.trim()) {
      onQuickSearch(topic)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Topic Input */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Research Topic</label>
        <input
          type="text"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="Enter your research topic..."
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
          disabled={loading}
        />
      </div>

      {/* Writing Style */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Writing Style</label>
        <select
          value={style}
          onChange={(e) => setStyle(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
          disabled={loading}
        >
          <option value="academic">Academic</option>
          <option value="journalistic">Journalistic</option>
          <option value="summary">Summary</option>
        </select>
      </div>

      {/* Verification Toggle */}
      <div className="flex items-center">
        <input
          type="checkbox"
          id="verification"
          checked={includeVerification}
          onChange={(e) => setIncludeVerification(e.target.checked)}
          className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
          disabled={loading}
        />
        <label htmlFor="verification" className="ml-2 text-sm text-gray-700">
          Include Verification
        </label>
      </div>

      {/* Buttons */}
      <div className="grid grid-cols-2 gap-3">
        <button
          type="submit"
          disabled={loading || !topic.trim()}
          className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-bold py-2 px-4 rounded-lg transition"
        >
          {loading ? 'Researching...' : 'Full Research'}
        </button>
        <button
          type="button"
          onClick={handleQuickSubmit}
          disabled={loading || !topic.trim()}
          className="w-full bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white font-bold py-2 px-4 rounded-lg transition"
        >
          {loading ? 'Searching...' : 'Quick Search'}
        </button>
      </div>
    </form>
  )
}

export default SearchForm
