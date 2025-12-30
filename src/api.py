from datetime import timedelta
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from src.models import Task, TaskCreate, TaskUpdate, User, UserInDB, Token
from src.security import (ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token,
                        get_current_user)
from src.services import AuthService, TaskService, get_auth_service, get_task_service

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get TaskService instance
def get_task_service_dep() -> TaskService:
    return get_task_service()

# --- Authentication Endpoints ---

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(get_auth_service)):
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User, auth_service: AuthService = Depends(get_auth_service)):
    try:
        created_user = auth_service.create_user(user)
        return created_user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# --- Task Endpoints ---

@app.get("/tasks", response_model=List[Task])
async def list_all_tasks(
    task_service: TaskService = Depends(get_task_service_dep),
    current_user: UserInDB = Depends(get_current_user)
):
    return task_service.list_tasks(owner=current_user.username)

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    task_create: TaskCreate,
    task_service: TaskService = Depends(get_task_service_dep),
    current_user: UserInDB = Depends(get_current_user)
):
    try:
        return task_service.create_task(task_create, owner=current_user.username)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/tasks/{task_id}", response_model=Task)
async def get_single_task(
    task_id: str,
    task_service: TaskService = Depends(get_task_service_dep),
    current_user: UserInDB = Depends(get_current_user)
):
    task = task_service.get_task(task_id, owner=current_user.username)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_existing_task(
    task_id: str,
    task_update: TaskUpdate,
    task_service: TaskService = Depends(get_task_service_dep),
    current_user: UserInDB = Depends(get_current_user)
):
    updated_task = task_service.update_task(task_id, task_update, owner=current_user.username)
    if updated_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return updated_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_task(
    task_id: str,
    task_service: TaskService = Depends(get_task_service_dep),
    current_user: UserInDB = Depends(get_current_user)
):
    if not task_service.delete_task(task_id, owner=current_user.username):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return None
