# Tasks: JSON-based Persistence

**Feature Branch**: `1-json-persistence` | **Date**: 2025-12-27 | **Spec**: [spec.md] | **Plan**: [plan.md]

**Organization**: Tasks are grouped by phase, reflecting the refactoring and implementation process.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare the project structure for persistence.

- [x] T001 Create `data/` directory for storing data files.

---

## Phase 2: Foundational (Refactoring for Modularity)

**Purpose**: Refactor the service layer to support multiple persistence implementations.

- [x] T002 Create a `TaskService` Abstract Base Class in `src/services.py` to define the service contract.
- [x] T003 Refactor existing functions into an `InMemoryTaskService` class in `src/services.py` that implements `TaskService`.
- [x] T004 Create `src/__init__.py` to ensure the `src` directory is treated as a Python package, resolving import issues.

---

## Phase 3: User Story 1 - Persist Tasks Across Sessions (Priority: P1)

**Goal**: Implement file-based persistence so tasks are saved and loaded between application sessions.
**Independent Test**: Add a task, exit, restart, and verify the task is still present.

### Implementation for User Story 1

- [x] T005 [US1] Implement `FileTaskService` in `src/services.py` to handle reading from and writing to `data/tasks.json`.
- [x] T006 [US1] Implement atomic writes in `FileTaskService` using a temporary file and rename strategy to prevent data corruption.
- [x] T007 [US1] Update `src/cli.py` to instantiate and use `FileTaskService` instead of the in-memory implementation.

### Tests for User Story 1

> **NOTE: These tests were created to verify the implementation.**

- [x] T008 [P] [US1] Update `tests/test_services.py` to test the `InMemoryTaskService` against the `TaskService` ABC.
- [x] T009 [P] [US1] Add tests to `tests/test_services.py` for `FileTaskService`, covering file creation, data persistence, atomic writes, and error handling for corrupted files.

---

## Phase N: Polish & Cross-Cutting Concerns

- [x] T010 Run all tests via `pytest` to ensure all changes are working correctly and no regressions were introduced.
