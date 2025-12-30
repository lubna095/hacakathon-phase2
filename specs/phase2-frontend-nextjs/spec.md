# Phase 2: Frontend with Next.js and FastAPI Backend

## 1. Feature Name
`phase2-frontend-nextjs`

## 2. Overview
This feature introduces a web-based user interface for the existing task management system, built with Next.js 15 (App Router) and Tailwind CSS. The frontend will communicate with a new FastAPI backend, which will expose the core task management logic from `src/services.py` via a RESTful API.

## 3. Goals
- Provide a modern, interactive web interface for managing tasks.
- Decouple the user interface from the backend logic.
- Ensure data persistence through the existing `data/tasks.json` file.
- Establish a clear API contract between the frontend and backend.

## 4. Non-Goals
- Implementing user authentication or authorization.
- Advanced search/filtering capabilities beyond basic task listing.
- Real-time updates (e.g., websockets).
- Extensive error handling and UI notifications beyond basic feedback.

## 5. Backend: FastAPI Server

### 5.1 Technology Stack
- Python 3.x
- FastAPI
- Uvicorn (ASGI server)
- Existing `src/services.py` (FileTaskService)
- Pydantic (for request/response models)

### 5.2 API Endpoints

All endpoints will operate on tasks, identified by their `name`.

#### 5.2.1 `GET /tasks`
- **Description:** Retrieve a list of all tasks.
- **Request:**
    - Method: `GET`
    - Path: `/tasks`
- **Response:**
    - Status: `200 OK`
    - Body: `List[Task]` (JSON array of Task objects)
- **Error Handling:**
    - `500 Internal Server Error`: For unexpected server issues.

#### 5.2.2 `GET /tasks/{task_name}`
- **Description:** Retrieve a specific task by its name.
- **Request:**
    - Method: `GET`
    - Path: `/tasks/{task_name}`
    - Parameters:
        - `task_name` (string, path parameter): The unique name of the task.
- **Response:**
    - Status: `200 OK`
    - Body: `Task` (JSON object representing the task)
- **Error Handling:**
    - `404 Not Found`: If the task with the given `task_name` does not exist.
    - `500 Internal Server Error`: For unexpected server issues.

#### 5.2.3 `POST /tasks`
- **Description:** Create a new task.
- **Request:**
    - Method: `POST`
    - Path: `/tasks`
    - Body: `TaskCreate` (JSON object with `name` and `description`)
- **Response:**
    - Status: `201 Created`
    - Body: `Task` (JSON object of the newly created task)
- **Error Handling:**
    - `400 Bad Request`: If the request body is invalid or a task with the same name already exists.
    - `500 Internal Server Error`: For unexpected server issues.

#### 5.2.4 `PUT /tasks/{task_name}`
- **Description:** Update an existing task.
- **Request:**
    - Method: `PUT`
    - Path: `/tasks/{task_name}`
    - Parameters:
        - `task_name` (string, path parameter): The unique name of the task to update.
    - Body: `TaskUpdate` (JSON object with `name`, `description`, `completed`)
- **Response:**
    - Status: `200 OK`
    - Body: `Task` (JSON object of the updated task)
- **Error Handling:**
    - `400 Bad Request`: If the request body is invalid.
    - `404 Not Found`: If the task with the given `task_name` does not exist.
    - `500 Internal Server Error`: For unexpected server issues.

#### 5.2.5 `DELETE /tasks/{task_name}`
- **Description:** Delete a task by its name.
- **Request:**
    - Method: `DELETE`
    - Path: `/tasks/{task_name}`
    - Parameters:
        - `task_name` (string, path parameter): The unique name of the task to delete.
- **Response:**
    - Status: `204 No Content`
    - Body: Empty
- **Error Handling:**
    - `404 Not Found`: If the task with the given `task_name` does not exist.
    - `500 Internal Server Error`: For unexpected server issues.

#### 5.2.6 `PATCH /tasks/{task_name}/toggle`
- **Description:** Toggle the completion status of a task.
- **Request:**
    - Method: `PATCH`
    - Path: `/tasks/{task_name}/toggle`
    - Parameters:
        - `task_name` (string, path parameter): The unique name of the task.
- **Response:**
    - Status: `200 OK`
    - Body: `Task` (JSON object of the toggled task)
- **Error Handling:**
    - `404 Not Found`: If the task with the given `task_name` does not exist.
    - `500 Internal Server Error`: For unexpected server issues.

### 5.3 Implementation Details
- A new Python file (e.g., `src/api.py`) will be created to host the FastAPI application.
- The FastAPI application will instantiate and use the `FileTaskService` from `src/services.py`.
- Pydantic models will be used to define request body schemas (`TaskCreate`, `TaskUpdate`) and response models (Task).

## 6. Frontend: Next.js Application

### 6.1 Technology Stack
- Next.js 15 (App Router)
- React 18+
- Tailwind CSS
- TypeScript (recommended)

### 6.2 Project Structure
- A new directory `frontend/` will be created at the project root.
- The Next.js application will be initialized within `frontend/`.

### 6.3 Core Components & Pages
- **`app/page.tsx`:** The main entry point, displaying the list of tasks.
- **`components/TaskList.tsx`:** Renders a list of tasks, each with its name, description, and completion status.
- **`components/TaskItem.tsx`:** Individual task component, including controls for toggling completion, editing, and deleting.
- **`components/TaskForm.tsx`:** A form for adding new tasks and potentially for editing existing ones.

### 6.4 Styling
- Tailwind CSS will be configured and used for all styling.
- Emphasis on a clean, minimalist design for readability and ease of use.

### 6.5 Data Fetching & State Management
- React's built-in state management (e.g., `useState`, `useReducer`) will be used for local UI state.
- Data fetching from the FastAPI backend will be handled using standard `fetch` API calls.
- UI will reflect loading states and potential errors during API interactions.

## 7. Connection (Frontend <-> Backend)

### 7.1 API Base URL
- The Next.js application will be configured to target the FastAPI backend at a configurable base URL (e.g., `http://localhost:8000`).

### 7.2 Data Flow
- **Displaying Tasks:** Frontend makes a `GET /tasks` request on page load/refresh, then renders the list.
- **Adding Task:** Frontend sends a `POST /tasks` request with new task data.
- **Updating Task:** Frontend sends a `PUT /tasks/{task_name}` request with updated task data.
- **Deleting Task:** Frontend sends a `DELETE /tasks/{task_name}` request.
- **Toggling Task:** Frontend sends a `PATCH /tasks/{task_name}/toggle` request.

## 8. Development Environment Setup

### 8.1 Backend
- Python virtual environment.
- `pip install fastapi uvicorn pydantic`
- Command to run: `uvicorn src.api:app --reload`

### 8.2 Frontend
- Node.js (LTS version) and npm/yarn/pnpm.
- `npx create-next-app@latest frontend`
- Install Tailwind CSS.
- Command to run: `npm run dev` (from `frontend/` directory).

## 9. Testing
- **Backend:** Manual testing of API endpoints using tools like Insomnia/Postman or `curl`.
- **Frontend:** Manual testing of UI interactions and data display.
- Integration: Verify that frontend actions correctly reflect changes in the backend and data persistence.