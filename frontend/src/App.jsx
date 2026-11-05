
import './App.css'

function App() {
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
          />

          <div className="input-footer">
            <span>Powered by AI</span>
            <button type="button">Generate SQL</button>
          </div>
        </div>

        <div className="example">
          <h3>Try asking</h3>
          <div className="examples">
            <div>Show customers from Pune</div>
            <div>How many customers are there?</div>
            <div>Show all orders</div>
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
