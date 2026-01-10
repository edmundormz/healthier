# LangGraph – Agent Architecture

## Nodes
- MessageOperator
- VitaAgent
- Orchestrator
- RulesEngine
- ScoringEngine
- SummaryGenerator

## Edges
MessageOperator → Vita  
Vita → Orchestrator  
Orchestrator → RulesEngine  
RulesEngine → ScoringEngine  
ScoringEngine → SummaryGenerator  
SummaryGenerator → Vita
