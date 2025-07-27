reply4u is an app for managing LLM-based Telegram chatbots that allows you to configure model behavior with any user. It supports both JSON and SQL data storage options, and Ollama or any third-party API compatible with the openai-python as LLM API

# Installation
For installation and proper working, **Python 3.12.2**, **Node.js 20.11.1**, and **PostgreSQL 16.2** (if using PostgreSQL storage) are required.

1. Clone GitHub repository: 
   ```bash
   git clone https://github.com/xtens1on/reply4u.git
   ```
2. Go to `backend` directory, create virtual environment and install required dependencies:   
   For **Linux/macOS**:
   ```bash
   cd reply4u/backend
   python -m venv venv
   source venv/bin/activate
   python -m pip install -r requirements.txt
   ```
   For **Windows**:
   ```powershell
   cd reply4u/backend
   python -m venv venv
   venv\scripts\activate
   python -m pip install -r requirements.txt
   ```
3. If you are going to use PostgreSQL as user store, install PostgreSQL 16.2 and create a database.
4. Create Telegram Application following <a href="https://core.telegram.org/api/obtaining_api_id#obtaining-api-id">**this**</a> guide
5. Install <a href="https://github.com/ollama/ollama">**Ollama**</a> or use any API, compatible with `openai-python`
6. Configure environment variables in `.env`:
   ```ini
   USER_STORAGE_TYPE=json  # User storage type. `json` for JSON-store and `sql` for PostgreSQL-store 

   # Database credentials (required only if you are using PostgreSQL-store)
   DB_DRIVER=postgresql+asyncpg
   DB_USERNAME=
   DB_PASSWORD=
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=reply4u

   # Telegram Application credentials
   TELEGRAM_API_ID=
   TELEGRAM_API_HASH=
   
   # LLM API provider (currently has 2 options: ollama, openai).
   LLM_PROVIDER=openai

   # OpenAI API credentials (required, if you use OpenAI as LLM_PROVIDER) 
   OPENAI_BASE_URL=
   OPENAI_API_KEY=

   # Delay between message processing during which both messages will be processed together (in seconds)
   RESPONSE_DELAY=5

   # Frontend-client hosts for correct CORS working (format: host1,host2,host3)
   FRONTEND_HOSTS=http://localhost:8281,http://127.0.0.1:8281
   ```
7. Go to frontend directory and install required dependencies:  
   ```bash
   cd ../frontend
   npm install
   ```
8. Run the application (all terminals should be opened in `reply4u` directory):
   ### Terminal 1: 
   For **Linux/macOS**: 
   ```bash
   cd backend
   source venv/bin/activate 
   python -m core.run  # start telegram worker
   ```
   For **Windows**:
   ```powershell
   cd backend
   venv\scripts\activate
   python -m core.run  # start telegram worker
   ```

   ### Terminal 2:  
   For **Linux/macOS**: 
   ```bash
   cd backend
   source venv/bin/activate
   python -m fastapi run api/run.py  # start admin api
   ```
   For **Windows**:
   ```powershell
   cd backend
   venv\scripts\activate
   python -m fastapi run api/run.py  # start admin api
   ```
   ### Terminal 3:
   ```bash
   cd frontend  
   npx http-server -p 8281  # you can replace 8281 with port you want to use here (you need to also change port in .env FRONTEND_HOST variable). Hosts an admin page. 
   ```
