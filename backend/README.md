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

### 1. Install Poetry

Poetry is a modern Python dependency manager (better than pip).

```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# Mac/Linux
curl -sSL https://install.python-poetry.org | python3 -

# Verify installation
poetry --version
```

### 2. Install Dependencies

```bash
# Install all dependencies
poetry install

# This creates a virtual environment automatically
# Poetry manages it for you!
```

### 3. Configure Environment

Your `.env` file should have these values:

Required environment variables (new Supabase key system):
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_PUBLISHABLE_KEY` - New publishable key (replaces anon key)
- `SUPABASE_SECRET_KEY` - Secret key (replaces service_role key, ⚠️ keep secret!)
- `TELEGRAM_BOT_TOKEN` - Telegram bot token from @BotFather
- `OPENAI_API_KEY` - OpenAI API key for LangGraph

### 4. Run the API

```bash
# With Poetry (recommended)
poetry run uvicorn app.main:app --reload

# Or enter Poetry shell first
poetry shell
uvicorn app.main:app --reload
```

API will be available at:
- **API:** http://localhost:8000
- **Docs (Swagger):** http://localhost:8000/docs
- **Docs (ReDoc):** http://localhost:8000/redoc

## Development

### Run Tests

```bash
# Run all tests (with Poetry)
poetry run pytest

# Run with coverage report
poetry run pytest --cov=app --cov-report=html

# Run only unit tests
poetry run pytest -m unit

# Run specific test file
poetry run pytest tests/test_example.py
```

### Code Quality

```bash
# Format code (Black)
poetry run black app/ tests/

# Lint code (Ruff)
poetry run ruff check app/ tests/

# Type check (MyPy)
poetry run mypy app/

# Auto-fix linting issues
poetry run ruff check --fix app/ tests/
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
