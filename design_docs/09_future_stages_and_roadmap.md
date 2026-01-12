# CH Health OS — Future Stages & Feature Roadmap

**Last Updated:** January 12, 2026, 7:45 PM CST

## Philosophy
CH Health OS grows in layers.
Each stage adds depth without breaking daily simplicity.

No feature is added unless it:
- Reduces friction
- Improves adherence
- Respects explainability
- Aligns with real life

---

## Stage v0 — MVP (Current)
Focus: Daily adherence

- Routine Builder (time-based, expiring)
- Habits
- Exercise aligned to goals
- Weekly body composition input
- Daily AM Brief & PM Recap
- Telegram-first interaction (Vita)
- Gamification & family rewards
- Dashboard (basic)

---

## Stage v1 — Biometric Context
Focus: Context-aware adjustments

- Oura API integration
  - Sleep
  - Readiness
  - Activity
  - Stress
- Rule-based adjustments:
  - Training intensity
  - Recovery days
  - Sleep nudges
- Trend analysis (weekly/monthly)

AI Role:
- Explain patterns
- Suggest micro-adjustments
- Never override rules

---

## Stage v2 — Preventive Health & Medical Memory
Focus: Long-term health continuity

- Preventive Health Vault
  - Upload labs, reports, prescriptions
  - Structured extraction
- Lab tracking & retest planner
- Protocol adherence monitoring
- Clinical guardrails & escalation logic

---

## Stage v3 — Predictive & Preventive Intelligence
Focus: Anticipation, not reaction

- Pattern detection:
  - Adherence decay
  - Overtraining risk
  - Sleep debt accumulation
- Scenario simulation:
  - "If you skip X → Y impact"
- Gentle forecasting (non-alarmist)

---

## Stage v4 — Extended Ecosystem (Optional)
Focus: Integration, not expansion

- Wearables beyond Oura (only if justified)
- Nutrition integrations (see detailed section below)
- Optional clinician-facing exports (PDF summaries)

Out of Scope:
- Social networks
- Public sharing
- Gamified leaderboards

---

## Future Feature: Nutrition & Meal Planning System

### Overview
Help users align nutrition with their health objectives through intelligent meal planning and food inventory management.

### Core Features

#### 1. Food Inventory Management
**Purpose:** Reduce waste, simplify grocery shopping, know what you have

- Digital fridge/pantry tracker
  - Photo-based item entry (optional)
  - Manual entry with quantities
  - Expiration date tracking
  - Category organization (proteins, vegetables, grains, etc.)
- Inventory awareness
  - "What can I make with what I have?"
  - Expiring soon notifications
  - Running low alerts

#### 2. Smart Grocery Lists
**Purpose:** Shop with intention, aligned to objectives

- Auto-generated shopping lists based on:
  - Meal plans
  - Current inventory gaps
  - User's health objectives
  - Household size
- List organization
  - Grouped by store section
  - Quantities calculated automatically
  - Shared lists (family collaboration)
- Integration points:
  - Export to notes/Instacart/etc.
  - Voice add: "Vita, add chicken to grocery list"

#### 3. Meal Planning Engine
**Purpose:** Nutrition that fits life, not disrupts it

**Objective-Aware Planning:**
- Aligns with user's goals in system:
  - Weight loss → calorie targets, macro balance
  - Muscle gain → protein prioritization
  - Energy/performance → carb timing
  - General health → balanced variety
- Respects dietary preferences:
  - Restrictions (allergies, vegetarian, etc.)
  - Dislikes (configurable)
  - Cooking skill level
  - Time constraints

**Intelligent Suggestions:**
- Week-view meal planner (breakfast, lunch, dinner, snacks)
- Recipe recommendations based on:
  - Current inventory (reduce waste)
  - Upcoming grocery trips
  - Family schedule (quick meals vs. leisurely)
  - Seasonality
- Batch cooking suggestions
- Leftover integration

**Flexibility:**
- Drag-and-drop meal swapping
- Quick substitutions
- "I ate out" logging (no guilt, just data)
- Recipe scaling (family size)

#### 4. Nutrition Tracking (Light Touch)
**Purpose:** Awareness without obsession

- Meal logging
  - Quick entry from meal plan
  - Photo + AI recognition (optional)
  - Voice: "Vita, I had salmon and broccoli"
- Nutrient summary (not daily nagging)
  - Weekly trends vs. objectives
  - Macro balance visualization
  - Key nutrients (protein, fiber, etc.)
- Integration with exercise
  - Fueling for training days
  - Recovery meal suggestions

### Vita's Role
- **Conversational Meal Planning**
  - "What should I make for dinner tonight?"
  - "I have chicken, rice, and spinach. Ideas?"
  - "Plan my meals this week, focus on quick dinners"
  
- **Gentle Nudges (Not Nagging)**
  - "Your chicken expires tomorrow. Want a recipe?"
  - "You're low on vegetables. Add to grocery list?"
  - "This week's meals are protein-light. Adjust?"

- **Explainable Recommendations**
  - "I suggested this because: [objective alignment + inventory]"
  - "This meal supports your [goal] with [nutrients]"

### Design Principles
1. **Reduce Friction:** Planning should be easier than not planning
2. **Respect Real Life:** Eating out, leftovers, chaos are normal
3. **Objective-Aligned:** Meals serve health goals, not arbitrary rules
4. **Family-Centered:** Plan for household, not just individual
5. **No Food Guilt:** Track for awareness, not judgment
6. **Explainable:** Why this meal? Why this timing?

### Technical Considerations
- **Rules-First Approach**
  - Macro targets calculated from user objectives
  - Recipe matching uses logic, not black-box AI
  - Inventory management is deterministic
  
- **Data Privacy**
  - Food preferences are sensitive (medical, cultural, personal)
  - No selling data to food companies
  - Optional photo storage (user-controlled)

- **Integration Points**
  - Recipe APIs (Spoonacular, Edamam, etc.)
  - Nutrition databases (USDA, etc.)
  - Potential grocery store APIs
  - Calendar integration (plan around events)

### Implementation Phases
**Phase 1: Foundation**
- Food inventory database
- Basic grocery list
- Manual meal planning

**Phase 2: Intelligence**
- Objective-aware meal suggestions
- Recipe recommendations from inventory
- Automated grocery list generation

**Phase 3: Conversational**
- Vita meal planning dialogue
- Voice-based inventory management
- Proactive nudges (expiration, shopping)

**Phase 4: Advanced**
- Photo-based inventory entry
- AI meal recognition
- Batch cooking optimization
- Family preference learning

### Success Metrics
- Reduction in "What's for dinner?" stress
- Decreased food waste
- Improved objective adherence (nutrition aligned to goals)
- Grocery shopping efficiency
- Meal prep time reduction

### Notes
- This feature is complex and should only be built after v0 is stable
- Start simple: inventory + lists before AI suggestions
- Family testing critical: nutrition is personal and cultural
- Never prescriptive: suggest, don't dictate
