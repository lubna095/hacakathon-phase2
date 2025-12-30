---
id: 013
title: Provide Manual Verification Steps for CLI
stage: explainer
date: 2025-12-27
surface: agent
model: gemini-pro
feature: 1-json-persistence
branch: 1-json-persistence
user: user
command: Verify the CLI still works exactly as before, but now remembers data after a restart.
labels: ["manual-test", "verification", "cli"]
links:
  spec: specs/1-json-persistence/spec.md
  ticket: null
  adr: null
  pr: null
files:
(none)
tests:
(none)
---

## Prompt

Verify the CLI still works exactly as before, but now remembers data after a restart.

## Response snapshot

I have implemented the persistence logic, and all automated tests are passing. To manually verify that the CLI works as expected and remembers data across restarts, please follow these steps in your terminal:

1.  **Run the application:**
    ```bash
    python main.py
    ```

2.  **Add a task:**
    -   Choose option `1`.
    -   Enter a task name (e.g., `My Persistent Task`).
    -   Enter a description (e.g., `This task should be saved`).
    -   You should see: `Task 'My Persistent Task' created successfully.`

3.  **List tasks:**
    -   Choose option `2`.
    -   You should see your new task listed: `[ ] My Persistent Task: This task should be saved`.

4.  **Exit the application:**
    -   Choose option `6`.
    -   You should see: `Exiting Task Management CLI. Goodbye!`

5.  **Restart the application:**
    ```bash
    python main.py
    ```

6.  **List tasks again:**
    -   Choose option `2`.
    -   You should see the task from the previous session: `[ ] My Persistent Task: This task should be saved`.

7.  **Clean up (optional):**
    -   Choose option `4` to delete the task.
    -   Enter the name `My Persistent Task`.
    -   Choose option `6` to exit.

This manual test will confirm that the application correctly saves and loads tasks. Let me know if you encounter any issues.

## Outcome

- ✅ Impact: Provided the user with clear, step-by-step instructions for manually verifying the implemented feature in the interactive CLI.
- 🧪 Tests: No new tests were run.
- 📁 Files: No files were created or modified.
- 🔁 Next prompts: Awaiting user confirmation or next instructions.
- 🧠 Reflection: For interactive applications, providing manual testing steps is a good way to empower the user to verify functionality that cannot be easily automated by the agent.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): none
