# CH Health OS Backend

FastAPI backend for CH Health OS.

## Tech Stack

- **Framework:** FastAPI (async Python web framework)
- **Database:** Supabase (Postgres) via SQLAlchemy ORM
- **AI:** LangGraph + OpenAI (for Vita agent)
- **Bot:** Telegram Bot API
- **Deployment:** Render

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── core/                # Core functionality
│   │   ├── config.py        # Settings and environment variables
│   │   ├── database.py      # Database connection
│   │   └── security.py      # Auth and security (coming soon)
│   ├── api/
│   │   └── routes/          # API endpoints
│   ├── models/              # SQLAlchemy models (database tables)
│   ├── schemas/             # Pydantic models (API validation)
│   ├── services/            # Business logic
│   └── agents/              # LangGraph agents (Vita)
├── tests/                   # Test suite
├── migrations/              # Database migrations
└── requirements.txt         # Python dependencies
```

## Setup

### 1. Create Virtual Environment

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Required environment variables:
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_ANON_KEY` - Supabase anon/public key
- `SUPABASE_SERVICE_KEY` - Supabase service role key (⚠️ keep secret!)
- `TELEGRAM_BOT_TOKEN` - Telegram bot token from @BotFather
- `OPENAI_API_KEY` - OpenAI API key for LangGraph

### 4. Run the API

```bash
# Development mode (auto-reload on code changes)
uvicorn app.main:app --reload

# Or using Python
python -m app.main
```

API will be available at:
- **API:** http://localhost:8000
- **Docs (Swagger):** http://localhost:8000/docs
- **Docs (ReDoc):** http://localhost:8000/redoc

## Development

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run only unit tests
pytest -m unit

# Run specific test file
pytest tests/test_example.py
```

### Code Quality

```bash
# Format code (Black)
black app/ tests/

# Lint code (Ruff)
ruff check app/ tests/

# Type check (MyPy)
mypy app/
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Add users table"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## API Endpoints

### Health Check
- `GET /` - Basic service info
- `GET /health` - Health check for monitoring

### Coming Soon
- `POST /api/telegram/webhook` - Telegram webhook
- `GET /api/routines` - Get user routines
- `POST /api/routines` - Create routine
- `GET /api/habits` - Get user habits
- `POST /api/habits/log` - Log habit completion

## Environment Variables

See `.env.example` for all available configuration options.

**Important for production:**
- Set `ENVIRONMENT=production`
- Set `DEBUG=false`
- Generate strong `SECRET_KEY` (use: `openssl rand -hex 32`)
- Restrict `CORS_ORIGINS` to your frontend domain

## Deployment

### Render

1. Connect your GitHub repository
2. Create new Web Service
3. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables from `.env`
5. Deploy!

## Documentation

- [Master Plan](../plans/00_MASTER_PLAN.md)
- [Database Schema](../database/schema/DATABASE_SCHEMA.md)
- [Project Conventions](../PROJECT_CONVENTIONS.md)

## Testing

We follow these coverage targets:
- **Core logic (services, agents):** 80%+
- **API endpoints:** 70%+
- **Utilities:** 90%+

Run tests after each meaningful change:
```bash
pytest --cov=app
```

## Contributing

See [PROJECT_CONVENTIONS.md](../PROJECT_CONVENTIONS.md) for coding standards.

---

**Last Updated:** January 10, 2026, 4:15 PM CST
