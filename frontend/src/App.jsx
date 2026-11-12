import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [response, setResponse] = useState(null)
  const [error, setError] = useState('')
  const [customMeaning, setCustomMeaning] = useState('')
  const [history, setHistory] = useState(() => {
  try {
    const savedHistory = localStorage.getItem('queryHistory')
    return savedHistory ? JSON.parse(savedHistory) : []
  } catch {
    return []
  }
})
useEffect(() => {
  localStorage.setItem('queryHistory', JSON.stringify(history))
}, [history])

  const handleSubmit = async () => {
    if (!question.trim()) {
      setError('Please enter a question.')
      return
    }

    setLoading(true)
    setResponse(null)
    setError('')

    try {
      const res = await fetch('http://127.0.0.1:8000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      })

      const data = await res.json()

      if (!res.ok) {
        throw new Error(data.detail || 'Something went wrong.')
      }

      setResponse(data)

if (data.status === 'success') {
  setHistory((prev) => [
    {
      question: data.question,
      generated_sql: data.generated_sql,
      results: data.results,
    },
    ...prev,
  ])
}
    } catch (err) {
      setError(err.message || 'Unable to connect to backend.')
    } finally {
      setLoading(false)
    }
  }


const handleClarification = async (selectedOption = null) => {
  const meaning = selectedOption || customMeaning.trim()

  if (!meaning) {
    setError('Please select an option or describe your meaning.')
    return
  }

  setLoading(true)
  setError('')

  try {
    const res = await fetch('http://127.0.0.1:8000/clarify', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        original_question: response.original_question,
        ...(selectedOption
          ? { selected_option: selectedOption }
          : { custom_meaning: meaning }),
      }),
    })

    const data = await res.json()

    if (!res.ok) {
      throw new Error(data.detail || 'Clarification failed.')
    }

    setResponse(data)
    setCustomMeaning('')

    if (data.status === 'success') {
      setHistory((prev) => [
        {
          question: response.original_question,
          generated_sql: data.generated_sql,
          results: data.results,
        },
        ...prev,
      ])
    }
  } catch (err) {
    setError(err.message || 'Unable to process clarification.')
  } finally {
    setLoading(false)
  }
}



  return (
    <div className="app">
      <header className="header">
        <h2>Text<span>2</span>SQL AI</h2>
        <p>Ask questions. Get SQL. Understand your data.</p>
      </header>

      <main className="main">
        <div className="welcome">
          <h1>Talk to your database</h1>
          <p>
            Convert your natural language questions into SQL queries
            and get instant results.
          </p>
        </div>

        <div className="chat-box">
          <textarea
            placeholder="Ask something like: Show customers from Pune..."
            rows="4"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />

          <div className="input-footer">
            <span>Powered by AI</span>
            <button
              type="button"
              onClick={handleSubmit}
              disabled={loading}
            >
              {loading ? 'Generating...' : 'Generate SQL'}
            </button>
          </div>
        </div>

        {error && <p className="error">{error}</p>}

        

{response && response.status === 'clarification_required' && (
  <div className="result-box">
    <h3>{response.clarification_question}</h3>

    <div className="clarification-options">
      {response.options.map((option, index) => (
        <button
          key={index}
          type="button"
          disabled={loading}
          onClick={() => handleClarification(option)}
        >
          {option}
        </button>
      ))}
    </div>

    <div className="custom-clarification">
      <h4>Something else?</h4>

      <textarea
        rows="3"
        placeholder="Describe what you mean by best customers..."
        value={customMeaning}
        onChange={(e) => setCustomMeaning(e.target.value)}
        disabled={loading}
      />

      <button
        type="button"
        disabled={loading || !customMeaning.trim()}
        onClick={() => handleClarification()}
      >
        {loading ? 'Processing...' : 'Submit Custom Meaning'}
      </button>
    </div>
  </div>
)}


{response && response.status === 'success' && (
  <div className="result-box">
    <h3>Generated SQL</h3>
    <pre>{response.generated_sql}</pre>

    <p>{response.validation_message}</p>

    <h3>Query Results</h3>

    {response.results.length > 0 ? (
      <table>
        <thead>
          <tr>
            {Object.keys(response.results[0]).map((column) => (
              <th key={column}>{column}</th>
            ))}
          </tr>
        </thead>

        <tbody>
          {response.results.map((row, index) => (
            <tr key={index}>
              {Object.values(row).map((value, i) => (
                <td key={i}>{value}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    ) : (
      <p>No results found.</p>
    )}
  </div>
)}
{history.length > 0 && (
  <div className="history-section">
    <h3>Recent Queries</h3>

    <div className="history-list">
      {history.map((item, index) => (
        <button
          key={index}
          type="button"
          onClick={() => {
            setQuestion(item.question)
            setResponse({
              status: 'success',
              question: item.question,
              generated_sql: item.generated_sql,
              validation_message: 'SQL query is valid.',
              results: item.results,
            })
          }}
        >
          {item.question}
        </button>
      ))}
    </div>
  </div>
)}

        <div className="example">
          <h3>Try asking</h3>
          <div className="examples">
            <div onClick={() => setQuestion('Show customers from Pune')}>
              Show customers from Pune
            </div>
            <div onClick={() => setQuestion('How many customers are there?')}>
              How many customers are there?
            </div>
            <div onClick={() => setQuestion('Show all orders')}>
              Show all orders
            </div>
          </div>
        </div>
      </main>

      <footer>
        Built with React, FastAPI, PostgreSQL and Gemini AI
      </footer>
    </div>
  )
}

export default App
