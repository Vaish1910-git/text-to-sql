
import { useState } from 'react'
import './App.css'

function App() {
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [response, setResponse] = useState(null)
  const [error, setError] = useState('')
  const [history, setHistory] = useState([])
  const [pendingQuestion, setPendingQuestion] = useState('')

  const API_URL = 'http://127.0.0.1:8000'

  // Send question to FastAPI
  const handleGenerate = async () => {
    if (!question.trim()) {
      setError('Please enter a question.')
      return
    }

    setLoading(true)
    setResponse(null)
    setError('')

    try {
      const res = await fetch(`${API_URL}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          question: question
        })
      })

      const data = await res.json()

      if (!res.ok) {
        throw new Error(data.detail || 'Something went wrong.')
      }

      // Save question if clarification is required
      if (data.status === 'clarification_required') {
        setPendingQuestion(question)
      }

      // Save successful normal questions
      if (data.status === 'success') {
        setHistory(prev => [
          {
            question: question,
            response: data
          },
          ...prev
        ])
        setPendingQuestion('')
      }

      setResponse(data)

    } catch (err) {
      setError(err.message || 'Unable to connect to backend.')
    } finally {
      setLoading(false)
    }
  }

  // Handle clarification selection
  const handleClarification = async (option) => {
    setLoading(true)
    setError('')

    try {
      const res = await fetch(`${API_URL}/clarify`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          original_question: response.original_question,
          selected_option: option
        })
      })

      const data = await res.json()

      if (!res.ok) {
        throw new Error(data.detail || 'Something went wrong.')
      }

      // Save clarified question and its result
      if (data.status === 'success') {
        setHistory(prev => [
          {
            question: pendingQuestion,
            response: data
          },
          ...prev
        ])

        setPendingQuestion('')
      }

      setResponse(data)

    } catch (err) {
      setError(err.message || 'Unable to connect to backend.')
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

        {/* Question Input */}
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
              onClick={handleGenerate}
              disabled={loading}
            >
              {loading ? 'Generating...' : 'Generate SQL'}
            </button>
          </div>

        </div>

        {/* Example Questions */}
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

        {/* Error Message */}
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {/* Loading Message */}
        {loading && (
          <p className="loading">
            Processing your question...
          </p>
        )}

        {/* Clarification Section */}
        {response?.status === 'clarification_required' && (
          <div className="result-section">

            <h2>Need some clarification</h2>

            <p>{response.clarification_question}</p>

            <div className="clarification-options">
              {response.options.map((option, index) => (
                <button
                  key={index}
                  type="button"
                  onClick={() => handleClarification(option)}
                  disabled={loading}
                >
                  {option}
                </button>
              ))}
            </div>

          </div>
        )}

        {/* SQL Result Section */}
        {response?.status === 'success' && (
          <div className="result-section">

            <h2>Generated SQL</h2>

            <pre className="sql-output">
              {response.generated_sql}
            </pre>

            <p className="validation-message">
              {response.validation_message}
            </p>

            <h2>Query Results</h2>

            {response.results?.length > 0 ? (
              <div className="table-container">
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
                        {Object.values(row).map((value, colIndex) => (
                          <td key={colIndex}>
                            {value === null ? 'NULL' : String(value)}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p>No records found.</p>
            )}

          </div>
        )}

        {/* Conversation History */}
        {history.length > 0 && (
          <div className="history-section">

            <h2>Conversation History</h2>

            {history.map((item, index) => (
              <div className="history-item" key={index}>

                <h3>Question {history.length - index}</h3>

                <p>{item.question}</p>
                <button
  type="button"
  className="view-history-btn"
  onClick={() => {
    setResponse(item.response)
    setQuestion(item.question)
    setError('')
  }}
>
  View Result
</button>

                <h4>Generated SQL</h4>

                <pre className="sql-output">
                  {item.response.generated_sql}
                </pre>

                <h4>Query Results</h4>

                {item.response.results?.length > 0 ? (
                  <div className="table-container">
                    <table>
                      <thead>
                        <tr>
                          {Object.keys(item.response.results[0]).map(column => (
                            <th key={column}>{column}</th>
                          ))}
                        </tr>
                      </thead>

                      <tbody>
                        {item.response.results.map((row, rowIndex) => (
                          <tr key={rowIndex}>
                            {Object.values(row).map((value, colIndex) => (
                              <td key={colIndex}>
                                {value === null ? 'NULL' : String(value)}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <p>No records found.</p>
                )}

              </div>
            ))}

          </div>
        )}

        {/* Backend Error Response */}
        {response?.status === 'error' && (
          <div className="error-message">
            {response.message}

            {response.generated_sql && (
              <pre className="sql-output">
                {response.generated_sql}
              </pre>
            )}
          </div>
        )}

      </main>

      <footer>
        Built with React, FastAPI, PostgreSQL and Gemini AI
      </footer>

    </div>
  )
}

export default App
