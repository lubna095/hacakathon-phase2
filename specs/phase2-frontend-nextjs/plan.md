# Phase 2: Frontend with Next.js and FastAPI Backend - Plan

## 1. Architectural Decisions

### 1.1 Backend - FastAPI Application
- **Location:** The FastAPI application will be implemented in a new file: `src/api.py`.
- **Relationship to `src/services.py`:** The FastAPI application will import `get_task_service` from `src/services.py` and utilize the `FileTaskService` instance to perform CRUD operations on tasks.
- **Pydantic Models for API:**
    - The existing `src.models.Task` will be used as the response model for task retrieval and creation.
    - New Pydantic models, `TaskCreate` and `TaskUpdate`, will be defined in `src/models.py` to validate incoming request bodies for `POST` and `PUT` operations, respectively.
- **Dependency Injection:** FastAPI's `Depends` system will be used to inject a `TaskService` instance into path operation functions, ensuring a single, reusable instance across requests.
- **Error Handling:** Standard FastAPI `HTTPException` will be used for API-specific error responses (e.g., `404 Not Found`, `400 Bad Request`).
- **CORS Configuration:** `fastapi.middleware.cors.CORSMiddleware` will be configured to explicitly allow requests from `http://localhost:3000` to enable communication with the Next.js frontend during development.
- **ASGI Server:** Uvicorn will be used to serve the FastAPI application.

### 1.2 Frontend - Next.js Application
- **Location:** The Next.js project will reside in a `frontend/` directory at the project root.
- **Data Fetching:** The Next.js application will use standard browser `fetch` API to interact with the FastAPI backend.
- **UI Framework:** React with Next.js 15 (App Router) and Tailwind CSS.

## 2. Backend Implementation Details (`src/api.py`)

### 2.1 Pydantic Models for Request Bodies (to be added to `src/models.py`)
- **`TaskCreate`:**
    - `name: str`
    - `description: str`
- **`TaskUpdate`:**
    - `name: str`
    - `description: str`
    - `completed: bool`

### 2.2 FastAPI Application Setup
- Initialize `FastAPI` instance: `app = FastAPI()`.
- Add `CORSMiddleware`:
    ```python
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    ```
- Dependency for `TaskService`:
    ```python
    def get_task_service_dep() -> TaskService:
        return get_task_service()
    ```

### 2.3 API Endpoints

#### 2.3.1 `GET /tasks`
- **Function:** `list_all_tasks(task_service: TaskService = Depends(get_task_service_dep))`
- **Logic:** Return `task_service.list_tasks()`.
- **Response Model:** `List[Task]`

#### 2.3.2 `GET /tasks/{task_name}`
- **Function:** `get_single_task(task_name: str, task_service: TaskService = Depends(get_task_service_dep))`
- **Logic:**
    - Call `task_service.get_task(task_name)`.
    - If task is `None`, raise `HTTPException(status_code=404, detail="Task not found")`.
    - Return the task.
- **Response Model:** `Task`

#### 2.3.3 `POST /tasks`
- **Function:** `create_new_task(task_create: TaskCreate, task_service: TaskService = Depends(get_task_service_dep))`
- **Logic:**
    - Create a `Task` object from `task_create` data.
    - Call `task_service.create_task()`.
    - Handle `ValueError` (task already exists) by raising `HTTPException(status_code=400, detail=str(e))`.
- **Response Model:** `Task`
- **Status Code:** `201 Created`

#### 2.3.4 `PUT /tasks/{task_name}`
- **Function:** `update_existing_task(task_name: str, task_update: TaskUpdate, task_service: TaskService = Depends(get_task_service_dep))`
- **Logic:**
    - Call `task_service.update_task(task_name, Task(**task_update.model_dump()))`.
    - If update returns `None`, raise `HTTPException(status_code=404, detail="Task not found")`.
- **Response Model:** `Task`

#### 2.3.5 `DELETE /tasks/{task_name}`
- **Function:** `delete_existing_task(task_name: str, task_service: TaskService = Depends(get_task_service_dep))`
- **Logic:**
    - Call `task_service.delete_task(task_name)`.
    - If task not found, raise `HTTPException(status_code=404, detail="Task not found")`.
- **Response Status:** `204 No Content`

#### 2.3.6 `PATCH /tasks/{task_name}/toggle`
- **Function:** `toggle_task_completion(task_name: str, task_service: TaskService = Depends(get_task_service_dep))`
- **Logic:**
    - Call `task_service.toggle_task_completion(task_name)`.
    - If task not found, raise `HTTPException(status_code=404, detail="Task not found")`.
- **Response Model:** `Task`

## 3. Frontend Implementation Details (Next.js in `frontend/`)

### 3.1 Project Setup
- `npx create-next-app@latest frontend --ts --eslint --app --tailwind --src-dir --use-npm` (or similar for pnpm/yarn).

### 3.2 Pages & Layouts
- **`frontend/app/layout.tsx`:** Basic HTML structure, Tailwind CSS setup.
- **`frontend/app/page.tsx`:** Main dashboard page. Will fetch and display tasks.

### 3.3 Components
- **`frontend/components/TaskList.tsx`:**
    - Props: `tasks: Task[]`
    - Renders a `<ul>` of `TaskItem` components.
- **`frontend/components/TaskItem.tsx`:**
    - Props: `task: Task`
    - Displays task name, description, and a checkbox for `completed` status.
    - Buttons for "Edit" and "Delete".
    - Handlers for API calls (toggle, edit, delete).
- **`frontend/components/TaskForm.tsx`:**
    - Props: `onAddTask: (name: string, description: string) => Promise<void>`
    - Input fields for `name` and `description`.
    - Submit button.

### 3.4 API Interaction
- Create a `frontend/lib/api.ts` for FastAPI service client:
    - Base URL for API (e.g., `http://localhost:8000`).
    - Functions for `getAllTasks`, `addTask`, `updateTask`, `deleteTask`, `toggleTask`.

### 3.5 State Management
- Use React's `useState` and `useEffect` for managing task list and form inputs.
- Implement loading states and basic error display.

## 4. Development Workflow

1.  Start FastAPI backend: `uvicorn src.api:app --reload` (from project root).
2.  Start Next.js frontend: `npm run dev` (from `frontend/` directory).

## 5. Risks and Considerations

- **CORS issues:** Ensure `http://localhost:3000` is correctly configured in FastAPI for cross-origin requests.
- **Pydantic version compatibility:** Ensure Pydantic versions are compatible between backend and frontend data models (TypeScript types generated from Python models).
- **Error handling:** Implement robust error handling on both frontend and backend for a better user experience.
- **Asynchronous operations:** Properly handle `async/await` in both FastAPI and Next.js for non-blocking operations.
