# Phase 2: Frontend with Next.js and FastAPI Backend - Tasks

This document outlines the granular, testable tasks required to implement the `phase2-frontend-nextjs` feature, covering both the FastAPI backend and the Next.js frontend.

## 1. Backend Tasks (FastAPI)

These tasks focus on creating the FastAPI application and exposing the task management logic via a RESTful API.

### 1.1. Setup FastAPI Application

- **Task:** Create `src/api.py` to initialize the FastAPI app.
    - **Description:** Create a new file `src/api.py`. Initialize `app = FastAPI()`.
    - **Acceptance Criteria:** `src/api.py` exists and contains basic FastAPI app initialization.
    - **Test:** Run `python -c "from src.api import app"` without errors.
- **Task:** Configure CORS middleware in `src/api.py`.
    - **Description:** Add `CORSMiddleware` to the FastAPI app to allow `http://localhost:3000` as an origin.
    - **Acceptance Criteria:** CORS middleware is correctly configured in `src/api.py`.
    - **Test:** Verify middleware configuration in code.
- **Task:** Define `get_task_service_dep` dependency in `src/api.py`.
    - **Description:** Create a function that returns an instance of `FileTaskService` for dependency injection.
    - **Acceptance Criteria:** `get_task_service_dep` is defined and returns `TaskService`.
    - **Test:** Call the dependency function and assert its return type.

### 1.2. Pydantic Models for API (in `src/models.py`)

- **Task:** Add `TaskCreate` Pydantic model.
    - **Description:** Define `TaskCreate(BaseModel)` with `name: str` and `description: str`.
    - **Acceptance Criteria:** `TaskCreate` model is defined in `src/models.py`.
    - **Test:** Instantiate `TaskCreate` and assert its attributes.
- **Task:** Add `TaskUpdate` Pydantic model.
    - **Description:** Define `TaskUpdate(BaseModel)` with `name: str`, `description: str`, and `completed: bool`.
    - **Acceptance Criteria:** `TaskUpdate` model is defined in `src/models.py`.
    - **Test:** Instantiate `TaskUpdate` and assert its attributes.

### 1.3. Implement API Endpoints (in `src/api.py`)

- **Task:** Implement `GET /tasks` endpoint.
    - **Description:** Create a path operation to list all tasks using `task_service.list_tasks()`.
    - **Acceptance Criteria:** Endpoint returns `List[Task]`.
    - **Test:** Make an HTTP GET request to `/tasks` and verify the response structure and status code (200).
- **Task:** Implement `POST /tasks` endpoint.
    - **Description:** Create a path operation to create a new task using `TaskCreate` model. Handle `ValueError` for existing tasks.
    - **Acceptance Criteria:** Endpoint creates a task and returns `Task` with status 201. Handles conflicts (400).
    - **Test:** Make an HTTP POST request to `/tasks` with valid and invalid data, verify responses (201, 400).
- **Task:** Implement `GET /tasks/{task_name}` endpoint.
    - **Description:** Create a path operation to retrieve a specific task.
    - **Acceptance Criteria:** Endpoint returns `Task` or 404 if not found.
    - **Test:** Make HTTP GET requests to `/tasks/existing_task` and `/tasks/non_existing_task`, verify responses (200, 404).
- **Task:** Implement `PUT /tasks/{task_name}` endpoint.
    - **Description:** Create a path operation to update an existing task using `TaskUpdate` model.
    - **Acceptance Criteria:** Endpoint updates task and returns `Task` or 404 if not found.
    - **Test:** Make HTTP PUT requests to `/tasks/existing_task` with valid data, verify responses (200, 404).
- **Task:** Implement `DELETE /tasks/{task_name}` endpoint.
    - **Description:** Create a path operation to delete a task.
    - **Acceptance Criteria:** Endpoint deletes task and returns 204 or 404 if not found.
    - **Test:** Make HTTP DELETE requests to `/tasks/existing_task` and `/tasks/non_existing_task`, verify responses (204, 404).
- **Task:** Implement `PATCH /tasks/{task_name}/toggle` endpoint.
    - **Description:** Create a path operation to toggle task completion status.
    - **Acceptance Criteria:** Endpoint toggles completion and returns `Task` or 404 if not found.
    - **Test:** Make HTTP PATCH requests to `/tasks/existing_task/toggle`, verify responses (200, 404).

### 1.4. Backend Testing Infrastructure

- **Task:** Create `tests/test_api.py`.
    - **Description:** Create a new file `tests/test_api.py` for API endpoint unit/integration tests using `pytest` and `httpx.TestClient`.
    - **Acceptance Criteria:** `tests/test_api.py` exists and contains basic test setup.
    - **Test:** Run `pytest tests/test_api.py` and ensure it executes without errors.

### 1.5. Backend Running Instructions

- **Task:** Document backend startup command.
    - **Description:** Add instructions on how to run the FastAPI server (e.g., `uvicorn src.api:app --reload`).
    - **Acceptance Criteria:** Startup command is clearly documented.

## 2. Frontend Tasks (Next.js)

These tasks focus on setting up the Next.js project and building the user interface.

### 2.1. Project Setup

- **Task:** Scaffold Next.js 15 project in `frontend/`.
    - **Description:** Navigate to the project root and run `npx create-next-app@latest frontend --ts --eslint --app --tailwind --src-dir --use-npm`.
    - **Acceptance Criteria:** `frontend/` directory is created and contains a working Next.js project with App Router, TypeScript, ESLint, and Tailwind CSS configured.
    - **Test:** Navigate into `frontend/` and run `npm run dev`. Ensure the Next.js development server starts without errors and the default page loads in the browser.

### 2.2. Basic UI Components and Pages

- **Task:** Modify `frontend/app/page.tsx` to fetch and display tasks.
    - **Description:** Implement logic to fetch tasks from the FastAPI backend (`GET /tasks`) and display them in a basic unordered list.
    - **Acceptance Criteria:** The main page successfully fetches and renders a list of tasks.
    - **Test:** Run both backend and frontend, navigate to `http://localhost:3000`, and verify tasks are displayed.
- **Task:** Create `frontend/components/TaskList.tsx`.
    - **Description:** Develop a reusable component to render a list of `TaskItem` components.
    - **Acceptance Criteria:** `TaskList.tsx` exists and correctly receives and maps task data to `TaskItem` components.
- **Task:** Create `frontend/components/TaskItem.tsx`.
    - **Description:** Develop a component for an individual task, displaying name, description, and completion status.
    - **Acceptance Criteria:** `TaskItem.tsx` exists and correctly displays task details.
- **Task:** Create `frontend/components/TaskForm.tsx`.
    - **Description:** Develop a form component for adding new tasks (name, description) that calls the `POST /tasks` API.
    - **Acceptance Criteria:** `TaskForm.tsx` exists and successfully adds new tasks via the API.
    - **Test:** Use the form to add a new task and verify it appears in the task list.

### 2.3. API Client

- **Task:** Create `frontend/lib/api.ts` for backend API interaction.
    - **Description:** Implement functions (`getAllTasks`, `addTask`, `getTask`, `updateTask`, `deleteTask`, `toggleTask`) that encapsulate `fetch` calls to the FastAPI backend.
    - **Acceptance Criteria:** `api.ts` exists and provides functions for all required API operations.

### 2.4. Implement Task Actions

- **Task:** Integrate task toggling functionality.
    - **Description:** Update `TaskItem.tsx` to include a checkbox/button that calls `PATCH /tasks/{task_name}/toggle` to update task completion status.
    - **Acceptance Criteria:** Toggling a task's completion status via the UI updates the backend and reflects in the UI.
- **Task:** Integrate task editing functionality.
    - **Description:** Update `TaskItem.tsx` and potentially `TaskForm.tsx` to allow editing of task name and description, calling `PUT /tasks/{task_name}`.
    - **Acceptance Criteria:** Editing a task via the UI updates the backend and reflects in the UI.
- **Task:** Integrate task deletion functionality.
    - **Description:** Update `TaskItem.tsx` to include a button that calls `DELETE /tasks/{task_name}` to delete a task.
    - **Acceptance Criteria:** Deleting a task via the UI removes it from the backend and UI.

### 2.5. Frontend Running Instructions

- **Task:** Document frontend startup command.
    - **Description:** Add instructions on how to run the Next.js development server (e.g., `npm run dev` from `frontend/` directory).
    - **Acceptance Criteria:** Startup command is clearly documented.
