# Best Practices for Working Smart

**Date:** January 10, 2026, 12:00 PM CST  
**Purpose:** Document the smart workflows, conventions, and strategies that make this project maintainable and efficient across multiple working sessions.

---

## 📅 Date & Time Management

### Always Verify Current Time Before Editing
- **Critical Rule**: NEVER assume the current date/time. Always verify before updating documents.
- **Command** (Windows PowerShell):
  ```powershell
  Get-Date -Format "MMMM d, yyyy, h:mm tt"
  ```
  Then manually add ` CST` suffix.

### Dual Timestamp Updates
Every document should have TWO timestamps that must be updated together:
1. **Header timestamp**: `**Date:** January 10, 2026, 12:00 PM CST`
2. **Footer timestamp**: `**Last Updated:** January 10, 2026, 12:00 PM CST`

### Format Standard
- **Format**: `Month DD, YYYY, H:MM AM/PM CST`
- **Examples**:
  - ✅ `January 10, 2026, 12:00 PM CST`
  - ✅ `December 5, 2025, 9:45 AM CST`
  - ❌ `01/10/2026` (too ambiguous)
  - ❌ `Jan 10, 2026` (abbreviated month)

### When to Update Timestamps
Update BOTH timestamps whenever you:
- Modify content in any document
- Add new sections
- Update status indicators
- Make any meaningful changes (not just typo fixes)

### Why This Matters
- **Session continuity**: Know which version of a document you're reading
- **Change tracking**: Understand when information was last verified
- **Conflict resolution**: Determine which version is most recent when comparing notes

See `DATE_TIME_FORMAT.md` for detailed specifications.

---

## 📂 Working Sessions Organization

### Folder Structure
```
/working_sessions/
├── 2026-01-08/
│   ├── 2026-01-08_1430_agent-charter-notes.md
│   ├── 2026-01-08_1545_database-migration-summary.md
│   └── 2026-01-08_1620_testing-results.md
├── 2026-01-09/
│   ├── 2026-01-09_0900_scoring-agent-development.md
│   └── 2026-01-09_1400_frontend-planning.md
└── relay-handoff.md  # Always at root level
```

### Daily Folder Convention
- **Format**: `YYYY-MM-DD/`
- **Purpose**: Group all working notes from a single day
- **Git status**: Ignored (these are temporary/iterative notes)

### File Naming Convention
- **Format**: `YYYY-MM-DD_HHMM_descriptive-name.md`
- **Components**:
  - Date: ISO format (YYYY-MM-DD)
  - Time: 24-hour format (HHMM)
  - Description: kebab-case, descriptive
- **Examples**:
  - ✅ `2026-01-10_1430_api-endpoint-implementation.md`
  - ✅ `2026-01-10_0900_session-kickoff-notes.md`
  - ❌ `notes.md` (not descriptive)
  - ❌ `jan-10-notes.md` (not following format)

### What Goes in Working Sessions
- Session summaries and notes
- Iteration logs (things we tried)
- Debugging findings
- Quick reference notes
- Brainstorming documents
- Temporary TODO lists

### What DOESN'T Go in Working Sessions
- Official project plans (those go in `/plans`)
- Architecture documents (those go in `/architecture`)
- Source code (those go in `/apps`)
- Final documentation (goes in appropriate locations)

---

## 🏃 Relay Handoff Strategy

### The Concept
Think of it like a relay race: Agent A finishes a session and hands the baton (project state) to Agent B at the start of the next session. The relay document is that baton.

### Single Source of Truth
- **Location**: `/working_sessions/relay-handoff.md` (ALWAYS at root level)
- **Naming**: ALWAYS exactly `relay-handoff.md` (no date prefix)
- **Uniqueness**: ONLY ONE can exist at a time
- **Git status**: SHOULD be committed (force add if needed) so it's available next session

### When to Create
- Only when explicitly requested by user at end of session
- Before major milestone transitions
- Before long breaks (weekend, vacation)
- When context is too complex to rely on memory

### Required Content Sections

#### 1. Executive Summary
```markdown
## 📋 Executive Summary
- **Session Date**: January 10, 2026
- **Current Phase**: Backend Development (Phase 2)
- **Overall Progress**: 45% complete
- **Blockers**: None
- **Next Session Priority**: Complete scoring agent testing
```

#### 2. Progress on Plans
```markdown
## 📊 Progress by Plan Document

### MASTER_PLAN.md
- ✅ Phase 1 (Database): Complete
- 🚧 Phase 2 (Backend): In Progress (60% complete)
- ⏳ Phase 3 (Frontend): Pending
- ⏳ Phase 4 (Agent Development): Pending
- ⏳ Phase 5 (Testing & Deployment): Pending

### 01_database_plan.md
- ✅ All tables created
- ✅ RLS policies implemented
- ✅ Migrations tested
- Status: COMPLETE

### 02_backend_plan.md
- ✅ Charter Agent: Complete
- 🚧 Scoring Agent: In Progress (testing phase)
- ⏳ ICP Agent: Not started
- ⏳ Workflow orchestrator: Not started
```

#### 3. What Was Completed This Session
```markdown
## ✅ Completed This Session
1. Implemented scoring agent core logic
2. Added Pydantic models for input/output
3. Integrated with Claude API
4. Added error handling and retries
5. Created unit tests (70% coverage)
```

#### 4. What's In Progress
```markdown
## 🚧 In Progress
1. Scoring agent testing (need to add edge cases)
2. Integration tests for database persistence
3. Documentation updates
```

#### 5. What's Pending
```markdown
## ⏳ Next Steps (Priority Order)
1. Complete scoring agent testing → Target: 80% coverage
2. Deploy scoring agent to dev environment
3. Begin ICP agent development
4. Update MASTER_PLAN.md with latest progress
```

#### 6. Blockers & Context
```markdown
## 🚨 Blockers & Important Context

### Blockers
- None currently

### Important Context for Next Session
- Scoring rubric schema is in `/schemas/04_artifacts_data_types.md`
- Test fixtures are in `tests/fixtures/scoring_examples.json`
- Remember: scoring must be deterministic (same inputs = same outputs)
- Claude API key is in `.env` (don't commit)
```

#### 7. Environment & Quick Start
```markdown
## 🚀 Quick Start for Next Session

### Environment Status
- Python 3.11 via Poetry
- Supabase MCP connected (`supabase-mpgs`)
- Database has all MPGS tables
- LangSmith tracking enabled

### Commands to Resume Work
\`\`\`bash
# Terminal 1: Start API server
cd apps/api
poetry install
poetry run uvicorn main:app --reload --port 8000

# Terminal 2: Run tests
cd apps/api
poetry run pytest tests/agents/test_scoring_agent.py -v
\`\`\`

### Files to Review First
1. `/apps/api/agents/scoring_agent.py` - Current implementation
2. `/tests/agents/test_scoring_agent.py` - Test suite
3. `/plans/02_backend_plan.md` - Backend plan status
```

#### 8. Success Criteria
```markdown
## 🎯 Success Criteria for Next Session
- [ ] Scoring agent test coverage reaches 80%
- [ ] All edge cases handled (missing data, invalid inputs)
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] Ready to move to ICP agent
```

### Using the Relay Document
**At start of new session:**
1. User says "check the relay document" or "read relay-handoff"
2. AI reads `/working_sessions/relay-handoff.md`
3. AI confirms understanding: "I see we're at X phase, Y is complete, Z is pending"
4. AI asks clarifying questions if needed
5. Work resumes seamlessly

**At end of session:**
1. User says "create relay handoff document"
2. AI reviews all plan documents for current status
3. AI creates NEW `/working_sessions/relay-handoff.md` (deleting old one first)
4. AI commits the relay document (force add if needed)

---

## 📋 Plan Document Maintenance

### The Living Documents Philosophy
Plan documents in `/plans` are LIVING documents—they should always reflect current reality, not just initial plans.

### When to Update Plans
Update plans:
- ✅ After completing any task in a plan checklist
- ✅ When approach changes from original plan
- ✅ When discovering new requirements
- ✅ At end of each working session
- ✅ Before creating relay handoff documents
- ❌ Don't wait until "everything is done"

### How to Update Plans

#### 1. Update Checklists
```markdown
Before:
- [ ] Implement scoring agent
- [ ] Add tests

After:
- [x] Implement scoring agent
- [x] Add tests (80% coverage achieved)
```

#### 2. Update Status Indicators
```markdown
Before:
## Phase 2: Backend Development - ⏳ Pending

After:
## Phase 2: Backend Development - 🚧 In Progress (60% complete)
```

#### 3. Add Completion Notes
```markdown
## Charter Agent - ✅ Complete

**Completion Notes:**
- Implemented using Claude 3.5 Sonnet (changed from GPT-4 as planned)
- Added additional validation for product requirements
- Test coverage: 85% (exceeded 80% target)
- Deployed to dev: January 8, 2026
```

#### 4. Update Timestamps
Always update the footer timestamp when modifying a plan:
```markdown
**Last Updated:** January 10, 2026, 12:00 PM CST
```

### Status Indicator Standards
- ✅ **Complete**: Fully done, tested, documented
- 🚧 **In Progress**: Actively working on it
- ⏳ **Pending**: Not started yet
- ⚠️ **Blocked**: Can't proceed (explain why)
- ❌ **Cancelled**: No longer needed (explain why)

### Plan Documents to Maintain
1. `/plans/MASTER_PLAN.md` - Overall project status (update most frequently)
2. `/plans/01_database_plan.md` - Database phase
3. `/plans/02_backend_plan.md` - Backend phase
4. `/plans/03_frontend_plan.md` - Frontend phase
5. `/plans/04_agent_development_plan.md` - Agent development details
6. `/plans/05_testing_deployment_plan.md` - Testing & deployment

---

## 🎓 Teaching Mode Best Practices

### Always Explain WHY
```markdown
❌ Bad:
"Adding LangGraph checkpointer."

✅ Good:
"Adding LangGraph checkpointer so the workflow can resume from interruptions.
This is critical for HITL (Human-In-The-Loop) points where we need user decisions.
See: https://langchain-ai.github.io/langgraph/how-tos/persistence/"
```

### Comment Complex Logic
```python
# ❌ Bad: No explanation
state["version"] = f"{major}.{minor}.{patch}"

# ✅ Good: Explain the reasoning
# Semantic versioning: MAJOR.MINOR.PATCH
# - MAJOR: Breaking changes to artifact structure
# - MINOR: New fields or significant updates
# - PATCH: Typo fixes, clarifications
# This ensures downstream consumers know when to update their code.
state["version"] = f"{major}.{minor}.{patch}"
```

### Link to Official Docs
```markdown
✅ Good practice:
"We're using LangGraph's StateGraph for orchestration (see: https://...)
instead of custom state management because it provides built-in:
- Checkpointing (resume from interruptions)
- Visualization (debug workflow graphs)
- Type safety (TypedDict for state)"
```

### Explain Trade-offs
```markdown
✅ Good practice:
"We could use Redis for caching, but we're using Supabase because:
- Already our database (one less service)
- Built-in realtime subscriptions (needed for frontend updates)
- RLS policies (security without custom middleware)

Trade-off: Supabase is slower than Redis, but for our use case
(human-in-the-loop workflows), latency isn't critical."
```

### Don't Assume Knowledge
```markdown
❌ Bad:
"Using RLS policies."

✅ Good:
"Using RLS (Row Level Security) policies—a Supabase feature that
enforces database-level security rules. This means users can only
access their own data, even if the API is compromised.
See: https://supabase.com/docs/guides/auth/row-level-security"
```

---

## 🧪 Testing Best Practices

### Test Continuously, Not Just Before Commits
```bash
# ❌ Bad workflow:
# Write 500 lines of code → Run tests → Fix 50 bugs

# ✅ Good workflow:
# Write 50 lines → Run tests → Fix 2 bugs → Repeat
```

### Run Tests in Watch Mode
```bash
# Python (using pytest-watch)
cd apps/api
poetry run ptw tests/

# TypeScript (using Vitest)
cd apps/web
pnpm run test --watch
```

### Test Coverage Targets
- **Core logic** (agents, gates, orchestrator): 80%+ required
- **UI components**: 70%+ (less critical for presentational components)
- **Utilities**: 90%+ (pure functions should be easy to test)

### Before Every Commit Checklist
```bash
# Backend
cd apps/api
poetry run ruff check .           # Linter
poetry run mypy .                  # Type checker
poetry run pytest tests/ -v --cov # Tests + coverage

# Frontend
cd apps/web
pnpm run lint                      # ESLint
pnpm run type-check               # TypeScript
pnpm run test                      # Vitest
```

---

## 🌳 Git Workflow Best Practices

### Branch Naming
- **Feature**: `feat/agent-charter`
- **Bug fix**: `fix/scoring-validation`
- **Documentation**: `docs/update-readme`
- **Refactor**: `refactor/scoring-logic`

### Commit Message Format
```bash
# Format: <type>: <description>

# Examples:
✅ "feat: add scoring agent with rubric validation"
✅ "fix: handle missing ICP data in scoring"
✅ "docs: update relay handoff strategy"
✅ "test: add edge cases for charter agent"

# Types:
# feat: New feature
# fix: Bug fix
# docs: Documentation only
# test: Adding or updating tests
# refactor: Code change that neither fixes a bug nor adds a feature
# chore: Updating dependencies, tooling, etc.
```

### What to Commit
- ✅ Source code
- ✅ Tests
- ✅ Documentation (plans, architecture)
- ✅ Lock files (`poetry.lock`, `pnpm-lock.yaml`)
- ✅ Relay handoff document
- ❌ Working session notes (those are gitignored)
- ❌ Environment files (`.env`, `.env.local`)
- ❌ Temporary files

### When to Commit
- After completing a logical unit of work
- Before switching context (end of day, switching branches)
- Before creating relay handoff document
- When tests pass

---

## 📝 Documentation Best Practices

### Document as You Build
```markdown
❌ Bad workflow:
Build entire feature → Write docs at the end

✅ Good workflow:
Plan (create doc) → Build incrementally → Update doc as you go
```

### Use Consistent Headers
```markdown
# Every major document should have:
**Date:** January 10, 2026, 12:00 PM CST
**Purpose:** [What this document is for]
**Status:** [Complete | In Progress | Pending]
**Last Updated:** January 10, 2026, 12:00 PM CST
```

### Link Between Documents
```markdown
✅ Good practice:
"See `/plans/02_backend_plan.md` for implementation details."
"Artifact schemas defined in `/schemas/04_artifacts_data_types.md`"
"Architecture overview in `/architecture/04_workflow_orchestration.md`"
```

### Keep TODOs Actionable
```markdown
❌ Bad:
<!-- TODO: Fix this -->

✅ Good:
<!-- TODO: Add validation for empty product_name (see issue #42) -->
<!-- TODO: Refactor to use Pydantic BaseModel instead of dict -->
```

---

## 🔄 Session Continuity Best Practices

### Starting a New Session
1. **Read relay handoff** (if exists): `/working_sessions/relay-handoff.md`
2. **Review recent plan updates**: Check `**Last Updated:**` timestamps
3. **Check working session notes**: Review yesterday's folder in `/working_sessions`
4. **Verify environment**: Run quick health checks (API, database, tests)
5. **Clarify priorities**: Ask user what to focus on if unclear

### During a Session
1. **Update plans frequently**: Don't wait until end
2. **Take notes in daily folder**: Create session-specific notes
3. **Test continuously**: Run tests after each meaningful change
4. **Ask for clarification**: Don't guess—block if unsure
5. **Update timestamps**: Every time you edit a document

### Ending a Session
1. **Update all relevant plans**: Reflect current reality
2. **Run final test suite**: Ensure nothing broken
3. **Create relay handoff** (if requested): Comprehensive handoff document
4. **Commit working code**: Don't leave broken state
5. **Note any blockers**: Document anything that needs attention

---

## 🎯 Decision-Making Best Practices

### When to Block vs. Assume
```markdown
✅ BLOCK when:
- User input is required (HITL-Decision point)
- Data is missing and can't be reasonably inferred
- Multiple valid approaches and choice impacts architecture
- Security or data integrity at stake

✅ ASSUME (with documentation) when:
- Standard industry practice applies
- Default configuration is reasonable
- Choice is easily reversible
- User has given general guidance

Always document assumptions clearly:
<!-- ASSUMPTION: Using standard port 8000 for API.
     User can override in .env with API_PORT=XXXX -->
```

### Explain Trade-offs
When making architectural decisions, always explain:
1. **What options were considered**
2. **Which option was chosen**
3. **Why it was chosen**
4. **What trade-offs were accepted**

Example:
```markdown
## Decision: Use LangGraph for Orchestration

### Options Considered:
1. Custom state machine (full control)
2. Apache Airflow (enterprise-grade)
3. LangGraph (LangChain ecosystem)

### Choice: LangGraph

### Reasoning:
- Built for LLM workflows (HITL, interrupts, retries)
- TypedDict state = type safety
- Built-in checkpointing = persistence
- Visual debugging tools

### Trade-offs Accepted:
- Newer framework (less mature than Airflow)
- Tied to LangChain ecosystem
- Learning curve for state management patterns
```

---

## 🚀 Efficiency Best Practices

### Use MCP for Database Operations
```bash
# ❌ Slow: Manual Supabase dashboard navigation

# ✅ Fast: AI assistant uses MCP to query directly
# "Show me all products in the database"
# → AI runs query via mcp_supabase-mpgs_execute_sql
```

### Parallelize Independent Tasks
```bash
# ❌ Sequential:
# Create database tables → Test
# Create API endpoints → Test
# Create frontend components → Test

# ✅ Parallel (where possible):
# Create database tables + Start API endpoints (in parallel)
# → Integration test (requires both)
```

### Automate Repetitive Tasks
- Use pre-commit hooks (Husky)
- Use watch mode for tests and linters
- Use scripts for common operations
- Use MCP for database queries

### Batch Related Changes
```bash
# ❌ Many small commits:
# "Add function"
# "Add test"
# "Fix typo"
# "Update docs"

# ✅ Logical units:
# "feat: add scoring agent with tests and docs"
```

---

## 🎓 Learning & Improvement

### Reflect on What Works
- Keep notes on what strategies work well
- Update this document when discovering better approaches
- Share learnings across projects

### Iterate on Processes
- If a process feels clunky, revisit it
- Propose improvements to this document
- Balance rigor with pragmatism

### Stay Consistent
- Consistency > perfection
- Follow established patterns even if not "ideal"
- Refactor patterns later if needed (document why)

---

## 📚 Quick Reference

### File Locations
- **Plans**: `/plans/*.md`
- **Architecture**: `/architecture/*.md`
- **Schemas**: `/schemas/*.md`
- **Working notes**: `/working_sessions/YYYY-MM-DD/*.md`
- **Relay handoff**: `/working_sessions/relay-handoff.md`
- **Backend**: `/apps/api/`
- **Frontend**: `/apps/web/`

### Key Commands
```bash
# Get current timestamp (Windows)
Get-Date -Format "MMMM d, yyyy, h:mm tt"  # Add " CST" manually

# Backend tests
cd apps/api && poetry run pytest tests/ -v

# Frontend tests
cd apps/web && pnpm run test

# Start API server
cd apps/api && poetry run uvicorn main:app --reload

# Start frontend
cd apps/web && pnpm run dev
```

### Status Indicators
- ✅ Complete
- 🚧 In Progress
- ⏳ Pending
- ⚠️ Blocked
- ❌ Cancelled

---

**Last Updated:** January 10, 2026, 12:00 PM CST

**Note**: This document itself should follow these practices—update timestamps when modified, commit changes, and reference it in relay handoff documents when relevant.
