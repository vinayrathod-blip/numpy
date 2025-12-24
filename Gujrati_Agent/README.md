# Gujarati Voice-Based Native Language Service Agent

A voice-first, agentic AI that helps users identify and apply for government/public welfare schemes in Gujarati. It implements an agentic Planner–Executor–Evaluator loop, uses three tools, maintains conversation memory, and handles failures.

## Features
- Gujarati-only interaction: STT → Agent → TTS
- Agentic state machine with Planner/Executor/Evaluator
- Tools:
  - Scheme retrieval (corpus search)
  - Eligibility engine (rule-based)
  - Application submission (mock API with failure simulation)
- Memory across turns (short-term + user profile)
- Failure handling (missing info, contradictions, API failure)



Install:
```bash
pip install -r requirements.txt
