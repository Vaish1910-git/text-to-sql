\# Text2SQL AI



An AI-powered Text-to-SQL application that converts natural language questions into PostgreSQL queries using Google's Gemini API.



Users can ask questions in plain English, clarify ambiguous requests, preview generated SQL, validate queries, and view database results through a React interface.



\## Features



\- Natural language to SQL generation using Gemini.

\- PostgreSQL database integration.

\- SQL validation using SQLGlot.

\- Automatic SQL correction.

\- Read-only SELECT query enforcement.

\- Ambiguity detection and clarification options.

\- Custom clarification support.

\- Multi-table JOIN and aggregation support.

\- FastAPI backend.

\- React frontend.

\- SQL preview and query results.

\- Query history with browser storage.

\- Backend error handling.



\## Technology Stack



\### Backend

\- Python

\- FastAPI

\- Google Gemini API

\- SQLGlot

\- Pydantic



\### Frontend

\- React.js

\- Vite

\- JavaScript

\- CSS



\### Database

\- PostgreSQL



\## Project Structure



```text

text-to-sql-ai/

│

├── app/

│   ├── api/

│   │   └── main.py

│   ├── database/

│   │   ├── connection.py

│   │   └── schema.py

│   ├── engine/

│   │   ├── gemini\\\_client.py

│   │   ├── text\\\_to\\\_sql.py

│   │   ├── clarification.py

│   │   ├── sql\\\_validator.py

│   │   └── sql\\\_corrector.py

│   └── main.py

│

├── frontend/

│   └── src/

│       ├── App.jsx

│       ├── App.css

│       ├── index.css

│       └── main.jsx

│

├── .env

├── .gitignore

└── README.md

```



\## Prerequisites



\- Python 3.10+

\- Node.js and npm

\- PostgreSQL

\- Google Gemini API key



\## Installation and Setup



\### 1. Clone the repository



```bash

git clone YOUR\\\_GITHUB\\\_REPOSITORY\\\_URL

cd text-to-sql-ai

```



\### 2. Create and activate Python virtual environment



```powershell

python -m venv .venv

.\\\\.venv\\\\Scripts\\\\Activate.ps1

```



\### 3. Install Python dependencies



```bash

pip install -r requirements.txt

```



\### 4. Configure environment variables



Create a `.env` file in the project root:



```env

GEMINI\\\_API\\\_KEY=your\\\_gemini\\\_api\\\_key

DB\\\_HOST=localhost

DB\\\_PORT=5432

DB\\\_NAME=text\\\_to\\\_sql\\\_db

DB\\\_USER=your\\\_postgres\\\_username

DB\\\_PASSWORD=your\\\_postgres\\\_password

```



Use the actual database variable names expected by `app/database/connection.py`.



Never commit your `.env` file or expose API keys.



\### 5. Set up PostgreSQL



Create the database:



```sql

CREATE DATABASE text\\\_to\\\_sql\\\_db;

```



Run the project's database schema and sample-data setup.



\### 6. Start the backend



From the project root:



```powershell

python -m uvicorn app.api.main:app --reload

```



Backend URL:



```text

http://127.0.0.1:8000

```



API documentation:



```text

http://127.0.0.1:8000/docs

```



\### 7. Start the frontend



Open another terminal:



```powershell

cd frontend

npm install

npm run dev

```



Frontend URL:



```text

http://localhost:5173

```



\## Example Questions



\- Show all customers from Pune.

\- How many customers are there?

\- Show all orders.

\- Find customers who spent more than 50000.

\- Who are my best customers?



For ambiguous questions, the application asks the user to select or describe the intended meaning before generating SQL.



\## Security



\- Only read-only SELECT queries are supported.

\- SQL validation checks generated queries.

\- Multiple SQL statements are restricted.

\- Unsupported write operations are rejected.

\- Database and API errors are handled gracefully.



\## Future Improvements



\- More comprehensive query evaluation.

\- Improved handling of complex natural language questions.

\- Deployment and production configuration.

\- Expanded database schema support.



\## Author



Vaishnavi Deshmukh

