# Telegram Integration & Vita Agent

## Components

### Message Operator
- Receives Telegram webhooks
- Normalizes messages
- Maps telegram_user_id → user_id
- Stores raw events

### Vita (Conversation Agent)
- Handles dialogue and tone
- Interprets intent
- Calls system tools
- Maintains short-term conversational state

### Health Orchestrator
- Owns health logic
- Executes rules
- Generates briefs, scores, nudges

## Flow
Telegram → Message Operator → Vita → Orchestrator → Vita → Telegram

## Example Commands
- /today
- /done
- /status
- /help
