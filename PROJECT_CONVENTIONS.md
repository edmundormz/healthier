# CH Health OS — Project Conventions

**Date:** January 10, 2026  
**Purpose:** Core conventions and standards for this project  
**Audience:** All contributors (human and AI)

---

## 🎯 Core Philosophy

This project follows a **teaching-first** approach:
- Code should be readable and self-documenting
- Complex logic must be explained with comments
- Always document the "why", not just the "what"
- Link to official documentation when using frameworks

---

## 📂 Project Structure

```
healthier/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/            # REST endpoints
│   │   ├── services/       # Business logic
│   │   ├── agents/         # LangGraph agents
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── core/           # Config, security, database
│   │   └── main.py         # FastAPI app
│   ├── migrations/         # Database migrations
│   ├── tests/             # Backend tests
│   └── requirements.txt
│
├── frontend/               # Next.js (PWA)
│   ├── app/               # App router pages
│   ├── components/        # React components
│   └── lib/              # Utilities
│
├── database/
│   ├── schema/           # Schema documentation
│   └── migrations/       # SQL migration files
│
├── design_docs/          # Product documentation
├── plans/               # Implementation plans
├── working_sessions/    # Session notes (gitignored)
│   ├── YYYY-MM-DD/     # Daily folders
│   └── relay-handoff.md # Session continuity (committed)
│
├── MASTER_PLAN.md       # Overall strategy
├── GETTING_STARTED.md   # Setup guide
└── PROJECT_CONVENTIONS.md # This file
```

---

## 📅 Timestamp Standards

### Required Format
- **Format:** `Month DD, YYYY, H:MM AM/PM CST`
- **Example:** `January 10, 2026, 12:00 PM CST`
- **Timezone:** Always CST (America/Chicago)

### Dual Timestamps
Every document should have:
1. **Header:** `**Date:** January 10, 2026, 12:00 PM CST`
2. **Footer:** `**Last Updated:** January 10, 2026, 12:00 PM CST`

Update BOTH when modifying documents.

### Get Current Time (Windows)
```powershell
Get-Date -Format "MMMM d, yyyy, h:mm tt"
# Manually add " CST" suffix
```

---

## 🧪 Testing Standards

### Coverage Targets
- **Core logic** (services, agents): 80%+ required
- **API endpoints**: 70%+
- **Utilities**: 90%+

### Test Continuously
```bash
# Run tests after each meaningful change
cd backend
pytest tests/ -v

# Watch mode (recommended)
pytest-watch tests/
```

### Before Every Commit
```bash
# Backend checks
cd backend
ruff check .           # Linter
mypy .                 # Type checker
pytest tests/ --cov   # Tests + coverage

# Frontend checks (later)
cd frontend
npm run lint
npm run type-check
npm run test
```

---

## 🌳 Git Workflow

### Branch Naming
- `feat/feature-name` — New features
- `fix/bug-description` — Bug fixes
- `docs/update-topic` — Documentation
- `refactor/component-name` — Code refactoring

### Commit Message Format
```
<type>: <description>

Examples:
feat: add routine versioning service
fix: handle null expiration dates
docs: update database schema
test: add scoring engine tests
refactor: simplify habit streak logic
```

### What to Commit
- ✅ Source code
- ✅ Tests
- ✅ Documentation (plans, architecture)
- ✅ Lock files
- ✅ `/working_sessions/relay-handoff.md`
- ❌ Working session notes (daily folders)
- ❌ `.env` files
- ❌ `__pycache__`, `node_modules`

---

## 📝 Code Standards

### Python (Backend)

#### Style Guide
- **Formatter:** Black (line length 100)
- **Linter:** Ruff
- **Type checker:** MyPy (strict mode)
- **Import order:** isort

#### Naming Conventions
```python
# Classes: PascalCase
class RoutineService:
    pass

# Functions/methods: snake_case
def get_active_routines(user_id: UUID) -> List[Routine]:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRY_ATTEMPTS = 3

# Private methods: _leading_underscore
def _calculate_score(self) -> float:
    pass
```

#### Type Hints (Required)
```python
# ✅ Good
def create_routine(
    user_id: UUID,
    name: str,
    moment: MomentOfDay
) -> Routine:
    pass

# ❌ Bad (no type hints)
def create_routine(user_id, name, moment):
    pass
```

#### Docstrings
```python
def calculate_daily_score(
    routine_adherence: float,
    habit_completion: float,
    exercise_completion: float
) -> float:
    """Calculate daily health score (0-100).
    
    Args:
        routine_adherence: Percentage of routines completed (0.0-1.0)
        habit_completion: Percentage of habits completed (0.0-1.0)
        exercise_completion: Percentage of exercises completed (0.0-1.0)
        
    Returns:
        Daily score from 0 to 100
        
    Example:
        >>> calculate_daily_score(0.8, 0.9, 1.0)
        90.0
    """
    pass
```

### TypeScript (Frontend - Later)
- **Formatter:** Prettier
- **Linter:** ESLint
- **Style:** Airbnb config
- **Type checker:** TypeScript strict mode

---

## 🔐 Security Standards

### Environment Variables
- Never commit `.env` files
- Use `.env.example` as template
- Validate all env vars at startup

### API Security
- Rate limiting on all endpoints
- Input validation with Pydantic
- JWT validation for protected routes
- CORS restricted to frontend domain

### Database Security
- Use RLS (Row Level Security) policies
- Never use service role key in frontend
- Parameterized queries only (SQLAlchemy handles this)
- Encrypt sensitive fields if needed

---

## 📚 Documentation Standards

### Document as You Build
```markdown
❌ Bad: Build entire feature → Write docs at end
✅ Good: Plan (create doc) → Build → Update doc continuously
```

### Link Between Documents
Always use relative paths:
```markdown
See `/plans/02_backend_plan.md` for details.
Architecture in `/database/schema/DATABASE_SCHEMA.md`
```

### Keep Plans Updated
Update plan documents:
- ✅ After completing tasks
- ✅ When approach changes
- ✅ At end of each session
- ❌ Don't wait until "everything is done"

---

## 🏃 Working Sessions

### Daily Folders
- **Location:** `/working_sessions/YYYY-MM-DD/`
- **Purpose:** Session notes, debugging logs, brainstorming
- **Git status:** Ignored (temporary)

### File Naming
```
YYYY-MM-DD_HHMM_descriptive-name.md

Examples:
2026-01-10_1430_api-endpoint-implementation.md
2026-01-10_0900_session-kickoff-notes.md
```

### Relay Handoff
- **Location:** `/working_sessions/relay-handoff.md` (root level)
- **Purpose:** Session continuity document
- **Git status:** Committed (force add if needed)
- **When to create:** End of session when requested

---

## 🎯 Status Indicators

Use these consistently across all documents:

- ✅ **Complete** — Fully done, tested, documented
- 🚧 **In Progress** — Actively working on it
- ⏳ **Pending** — Not started yet
- ⚠️ **Blocked** — Can't proceed (explain why)
- ❌ **Cancelled** — No longer needed (explain why)

---

## 🔄 Session Workflow

### Starting a Session
1. Read `/working_sessions/relay-handoff.md` (if exists)
2. Check plan document timestamps
3. Review yesterday's session notes
4. Verify environment (API, database)
5. Clarify priorities with user

### During a Session
1. Update plans frequently
2. Take notes in daily folder
3. Test continuously
4. Ask for clarification when unsure
5. Update timestamps on modified docs

### Ending a Session
1. Update all relevant plans
2. Run final test suite
3. Create relay handoff (if requested)
4. Commit working code
5. Document any blockers

---

## 🚀 Performance Standards

### API Response Times
- Simple queries: < 100ms
- Complex queries: < 500ms
- LangGraph workflows: < 5s (acceptable for AI)

### Database
- Index all foreign keys
- Index frequently queried columns
- Use database views for complex joins
- Monitor slow query log

### Frontend (Later)
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3s
- Lighthouse score: > 90

---

## 🎓 Teaching Mode

Since this is a learning project:

### Always Explain Why
```python
# ❌ Bad: No explanation
state["version"] = f"{major}.{minor}.{patch}"

# ✅ Good: Explain the reasoning
# Semantic versioning: MAJOR.MINOR.PATCH
# This ensures consumers know when updates may break their code
state["version"] = f"{major}.{minor}.{patch}"
```

### Link to Official Docs
```python
# Using LangGraph StateGraph for orchestration
# See: https://langchain-ai.github.io/langgraph/concepts/#stategraph
# Provides checkpointing, visualization, and type safety
```

### Explain Trade-offs
Document why you chose one approach over another:
```markdown
## Decision: SQLAlchemy (ORM)

Considered: Raw SQL vs SQLAlchemy

Chose: SQLAlchemy because:
- Type safety helps prevent bugs
- Easier for beginners
- Built-in SQL injection protection
- Can optimize specific queries later if needed

Trade-off: Slight performance overhead, but negligible for our use case
```

---

## 🔧 Tool Preferences

### Backend
- **Package manager:** pip + venv (Poetry optional later)
- **HTTP client:** httpx
- **Testing:** pytest + pytest-asyncio
- **ORM:** SQLAlchemy 2.0+
- **Validation:** Pydantic v2
- **API docs:** FastAPI auto-docs

### Frontend (Later)
- **Package manager:** npm or pnpm
- **Framework:** Next.js 14+ (App Router)
- **UI library:** Shadcn UI
- **State:** React Context (Zustand if needed)
- **Forms:** React Hook Form + Zod

### Database
- **Migrations:** Raw SQL files (numbered)
- **Queries:** SQLAlchemy ORM
- **MCP:** Use for quick queries and testing

---

## 📊 Success Metrics

### Code Quality
- [ ] All tests passing
- [ ] Coverage targets met
- [ ] No linter errors
- [ ] Type checker passing
- [ ] Documentation complete

### Performance
- [ ] API endpoints within response time targets
- [ ] No N+1 query issues
- [ ] Database indexes optimized

### User Experience
- [ ] Telegram bot responsive (< 2s)
- [ ] Dashboard loads fast (< 3s)
- [ ] No breaking errors in production

---

## 🤝 When to Ask for Help

**Block and ask when:**
- User input required (HITL decisions)
- Multiple valid approaches (architectural impact)
- Security or data integrity concerns
- Unclear requirements

**Assume and document when:**
- Standard industry practice
- Default configuration reasonable
- Choice easily reversible
- User gave general guidance

Always document assumptions:
```markdown
<!-- ASSUMPTION: Using port 8000 for API
     Override in .env with API_PORT=XXXX -->
```

---

## 📖 Required Reading

Before starting development, review:
1. `MASTER_PLAN.md` — Overall strategy
2. `GETTING_STARTED.md` — Setup instructions
3. `database/schema/DATABASE_SCHEMA.md` — Data model
4. `design_docs/README.md` — Product context

---

**Last Updated:** January 10, 2026, 12:00 PM CST

**Note:** This document is a living standard. Update it when discovering better approaches or new patterns.
