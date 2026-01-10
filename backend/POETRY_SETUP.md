# Poetry Setup Guide

Poetry is a modern Python dependency manager that replaces pip + requirements.txt with better dependency resolution and virtual environment management.

## Why Poetry?

**Benefits over pip:**
- **Automatic virtual environment management** - No need to manually create/activate venvs
- **Lock files** - `poetry.lock` ensures everyone uses exact same versions
- **Better dependency resolution** - Prevents version conflicts
- **Cleaner configuration** - All in `pyproject.toml` (Python standard)
- **Dev dependencies separated** - Testing tools don't go to production

## Installing Poetry

### Windows (PowerShell)
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

### Mac/Linux
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Verify Installation
```bash
poetry --version
# Should show: Poetry (version 1.7.1)
```

## Using Poetry in This Project

### 1. Install Dependencies
```bash
cd backend
poetry install
```

This will:
- Read `pyproject.toml`
- Create a virtual environment (Poetry manages it)
- Install all dependencies
- Create `poetry.lock` file

### 2. Run Commands

**Option A: Use `poetry run` prefix**
```bash
poetry run uvicorn app.main:app --reload
poetry run pytest
poetry run black app/
```

**Option B: Enter Poetry shell**
```bash
poetry shell  # Activates the virtual environment
uvicorn app.main:app --reload
pytest
black app/
```

### 3. Add New Dependencies

**For production dependencies:**
```bash
poetry add fastapi
poetry add sqlalchemy
```

**For development dependencies:**
```bash
poetry add --group dev pytest
poetry add --group dev ruff
```

### 4. Update Dependencies
```bash
# Update all dependencies
poetry update

# Update specific package
poetry update fastapi
```

## Common Commands

```bash
# Show installed packages
poetry show

# Show outdated packages
poetry show --outdated

# Remove a package
poetry remove package-name

# Export requirements.txt (for Docker/Render)
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

## Project Structure

```
backend/
├── pyproject.toml    # Dependencies and config (like package.json)
├── poetry.lock       # Locked versions (like package-lock.json)
├── app/             # Your code
└── tests/           # Tests
```

## Important Files

### pyproject.toml
- Lists all dependencies with version constraints
- Contains tool configurations (black, ruff, mypy, pytest)
- Python's standard for project metadata

### poetry.lock
- Exact versions of all dependencies (including sub-dependencies)
- **Should be committed to git**
- Ensures everyone uses same versions

## Tips

**Finding virtual environment location:**
```bash
poetry env info --path
```

**Activate virtual environment manually:**
```bash
# Windows
& (poetry env info --path)\Scripts\activate

# Mac/Linux
source $(poetry env info --path)/bin/activate
```

**Clear cache:**
```bash
poetry cache clear . --all
```

## For Deployment (Render)

Render supports Poetry automatically. In your render.yaml:

```yaml
services:
  - type: web
    name: ch-health-api
    env: python
    buildCommand: pip install poetry && poetry install --only main
    startCommand: poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Troubleshooting

**"poetry: command not found"**
- Add Poetry to PATH
- Windows: `%APPDATA%\Python\Scripts`
- Mac/Linux: `$HOME/.local/bin`

**Poetry is slow**
- Disable parallel installation: `poetry config installer.parallel false`
- Use faster index: `poetry config repositories.pypi.url https://pypi.org/simple`

**Need to use specific Python version**
```bash
poetry env use python3.11
poetry install
```

---

**Why we switched from pip to Poetry:**
- More reliable dependency management
- Industry standard for modern Python projects
- Better developer experience
- Cleaner project structure

**See:** https://python-poetry.org/docs/
