# Exercise System – MVP

## Goals
- Align workouts to personal objectives
- Encourage consistency over intensity

## User Inputs
- Primary goal (fat loss, recomposition, energy)
- Available equipment
- Training days per week

## Workout Structure
- WorkoutPlan
- WorkoutSession (A / B / C)
- Exercises with:
  - sets
  - reps
  - load
  - RPE target

## Post-Workout Check-in
- Completed (yes/no)
- RPE actual
- Notes (pain, fatigue)

## Adjustment Logic (Rules)
- If RPE consistently high → reduce volume
- If sessions skipped → simplify next week
