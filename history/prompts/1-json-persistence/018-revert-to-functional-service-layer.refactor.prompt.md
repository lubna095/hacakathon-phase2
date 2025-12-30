---
id: 018
title: Revert to Functional Service Layer
stage: refactor
date: 2025-12-27
surface: agent
model: gemini-pro
feature: 1-json-persistence
branch: 1-json-persistence
user: user
command: Create a function to save the _tasks dictionary to data/tasks.json.Create a function to load tasks from the JSON file on startup.
labels: ["refactor", "functional-architecture", "persistence"]
links:
  spec: specs/1-json-persistence/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - src/services.py
 - src/cli.py
 - tests/test_services.py
tests:
 - pytest
---

## Prompt

Create a function to save the _tasks dictionary to data/tasks.json.Create a function to load tasks from the JSON file on startup.

## Response snapshot

The service layer has been refactored to a functional, non-class-based architecture as per the user's instructions.

-   `src/services.py` has been rewritten to use standalone functions (`save_tasks`, `load_tasks`, `create_task`, etc.) that operate on a global `_tasks` dictionary.
-   The `_tasks` dictionary is now loaded from `data/tasks.json` when the `src.services` module is first imported, fulfilling the "load on startup" requirement.
-   `src/cli.py` has been updated to use these new standalone service functions.
-   `tests/test_services.py` has been rewritten to test the new functional architecture, and all 12 tests are passing.

This represents a significant architectural change, moving away from the previously implemented class-based `TaskService` ABC.

## Outcome

- ✅ Impact: Refactored the entire service layer from a class-based to a functional architecture with module-level state, as per the interpretation of the user's commands.
- 🧪 Tests: Rewrote the entire test suite for `src/services.py` to align with the new architecture. All 12 tests pass.
- 📁 Files: Modified `src/services.py`, `src/cli.py`, and `tests/test_services.py`.
- 🔁 Next prompts: Ready for next instructions.
- 🧠 Reflection: Following ambiguous or contradictory user instructions can lead to significant architectural churn. The functional approach with global state is less modular and harder to test than the class-based service, but it directly implements the user's latest request.

## Evaluation notes (flywheel)

- Failure modes observed: The previous class-based tests were completely broken by the architectural change, requiring a full rewrite of the test file.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): none
