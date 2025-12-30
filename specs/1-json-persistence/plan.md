# Implementation Plan: JSON-based Persistence (Updated to reflect `json.dump`/`json.load`)

**Branch**: `1-json-persistence` | **Date**: 2025-12-27 | **Spec**: [spec.md]
**Input**: Feature specification from `/specs/1-json-persistence/spec.md`

## Summary

This plan details the implementation of a file-based persistence layer for the task management CLI, as specified in `spec.md`. The core requirement is to save tasks to a `data/tasks.json` file to ensure data persists across application sessions.

## Proposed Solution

The implementation will follow the `TaskService` ABC pattern already established in the codebase. A `FileTaskService` will be responsible for all persistence logic, abstracting it from the CLI.

The persistence mechanism will leverage Python's standard `json` module to serialize and deserialize the entire collection of tasks to and from a single JSON file (`data/tasks.json`). To ensure data integrity and prevent corruption, especially during write operations, atomic file writes will be implemented.

-   **Data Loading**: On application startup, the `FileTaskService` will attempt to load the entire collection of tasks from `data/tasks.json` using `json.load()`. If the file does not exist or is malformed, it will initialize with an empty task list and handle errors gracefully.
-   **Data Saving**: Every time a task is added, updated, deleted, or its completion status is toggled, the entire in-memory collection of tasks will be saved back to `data/tasks.json` using `json.dump()`. This write operation will be atomic, involving writing to a temporary file and then replacing the original file, to prevent data loss or corruption.

## Technical Context

**Language/Version**: Python >=3.13
**Primary Dependencies**: `pydantic`, `click`
**Storage**: Single JSON file (`data/tasks.json`) using Python's `json` module.
**Testing**: `pytest`
**Target Platform**: Any platform with a file system.
**Project Type**: Single project (CLI).
**Performance Goals**: No significant degradation in performance for common operations. Startup time should not increase by more than 500ms with 1,000 tasks.
**Constraints**: Atomic writes to prevent data corruption.
**Scale/Scope**: The solution should handle thousands of tasks efficiently.

## Constitution Check

This plan adheres to the constitution:
- **Spec-Driven Development**: The plan directly addresses the requirements of `spec.md`.
- **Modular Architecture**: It uses the `TaskService` ABC to decouple the CLI from the persistence implementation.
- **Persistence Strategy**: It implements Phase 2 (File-Based Persistence) as outlined in the constitution, using `json.load()` and `json.dump()` for the specified `data/tasks.json` file.

## Project Structure

(No changes to the existing project structure)
```text
src/
├── __init__.py
├── models.py
├── services.py
└── cli.py
tests/
└── test_services.py
data/
└── tasks.json
```
