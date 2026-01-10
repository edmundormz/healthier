# Routine System Design (with Expiration)

## Core Concept
Routines are time-bound protocols, not static checklists.

## Entities

### Routine
- id
- user_id
- active_version_id

### RoutineVersion
- id
- routine_id
- start_date
- end_date (nullable)
- created_by
- notes

### RoutineCard
- id
- routine_version_id
- moment_of_day (AM | MIDDAY | PM | NIGHT)

### RoutineItem
- id
- routine_card_id
- type (medication | supplement | skincare | habit)
- name
- dosage / instructions
- frequency
- expires_at (nullable)
- duration_days (nullable)
- next_item_id (optional)

## Expiration Rules
- An item is active if:
  - current_date >= start_date
  - AND (expires_at IS NULL OR current_date <= expires_at)

## Example
Medication:
- Drug A – 20mg – Days 1–14
- Drug A – 10mg – Days 15–28

Implemented as:
- Item A (expires_at = day 14, next_item_id = Item B)
- Item B (start_date = day 15)

## Benefits
- Medical traceability
- Clean transitions
- Historical adherence preserved
