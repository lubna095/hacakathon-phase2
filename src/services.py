import json
import os
import tempfile
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse
from pymongo import MongoClient
from bson import ObjectId

from passlib.context import CryptContext

from src.models import Task, TaskCreate, TaskUpdate, User, UserInDB, AuthService 



# --- Constants ---
DATA_FILE = 'data/tasks.json'
USERS_FILE = 'data/users.json'

# --- Security ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --- Helper Functions for File-based Persistence ---

def _load_tasks_from_file(file_path: Path) -> List[Task]:
    """Loads tasks from a JSON file."""
    if not file_path.exists():
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            if not content:
                return []
            tasks_data = json.loads(content)
        return [Task(**data) for data in tasks_data]
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def _save_tasks_to_file(file_path: Path, tasks_list: List[Task]) -> None:
    """Saves tasks to a JSON file atomically."""
    os.makedirs(file_path.parent, exist_ok=True)
    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8", dir=file_path.parent)
    try:
        json.dump([task.model_dump() for task in tasks_list], temp_file, indent=4)
        temp_file.flush()
        os.fsync(temp_file.fileno())
    except Exception as e:
        temp_file.close()
        os.remove(temp_file.name)
        raise e
    finally:
        temp_file.close()
    os.replace(temp_file.name, file_path)

def _load_users_from_file(file_path: Path) -> Dict[str, UserInDB]:
    if not file_path.exists():
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            if not content:
                return {}
            users_data = json.loads(content)
        return {username: UserInDB(**data) for username, data in users_data.items()}
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def _save_users_to_file(file_path: Path, users_dict: Dict[str, UserInDB]) -> None:
    os.makedirs(file_path.parent, exist_ok=True)
    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8", dir=file_path.parent)
    try:
        json.dump({name: user.model_dump(exclude={'password'}) for name, user in users_dict.items()}, temp_file, indent=4)
        temp_file.flush()
        os.fsync(temp_file.fileno())
    except Exception as e:
        temp_file.close()
        os.remove(temp_file.name)
        raise e
    finally:
        temp_file.close()
    os.replace(temp_file.name, file_path)


# --- Abstract Base Class for Task Service ---

class TaskService(ABC):
    """Abstract Base Class for task management services."""

    @abstractmethod
    def create_task(self, task_create: TaskCreate, owner: str) -> Task:
        """Creates a new task for a given owner."""
        pass

    @abstractmethod
    def get_task(self, task_id: str, owner: str) -> Optional[Task]:
        """Retrieves a task by its ID for a specific owner."""
        pass

    @abstractmethod
    def list_tasks(self, owner: str) -> List[Task]:
        """Returns a list of all tasks for a specific owner."""
        pass

    @abstractmethod
    def update_task(self, task_id: str, task_update: TaskUpdate, owner: str) -> Optional[Task]:
        """Updates an existing task."""
        pass

    @abstractmethod
    def delete_task(self, task_id: str, owner: str) -> bool:
        """Deletes a task by its ID for a specific owner."""
        pass


# --- Service Implementations ---

class InMemoryTaskService(TaskService):
    """In-memory implementation of the TaskService. Data is not persisted."""
    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def create_task(self, task_create: TaskCreate, owner: str) -> Task:
        task = Task(id=str(self._next_id), owner=owner, **task_create.model_dump())
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_task(self, task_id: str, owner: str) -> Optional[Task]:
        for task in self._tasks:
            if task.id == str(task_id) and task.owner == owner:
                return task
        return None

    def list_tasks(self, owner: str) -> List[Task]:
        return [task for task in self._tasks if task.owner == owner]

    def update_task(self, task_id: str, task_update: TaskUpdate, owner: str) -> Optional[Task]:
        task = self.get_task(task_id, owner)
        if not task:
            return None
        
        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)
        return task

    def delete_task(self, task_id: str, owner: str) -> bool:
        task = self.get_task(task_id, owner)
        if task:
            self._tasks.remove(task)
            return True
        return False


class FileTaskService(TaskService):
    """File-based (JSON) implementation of the TaskService."""
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._tasks: List[Task] = []
        self._next_id: int = 1
        self.load_tasks()

    def load_tasks(self) -> None:
        """Loads tasks from the file system."""
        self._tasks = _load_tasks_from_file(self.file_path)
        if self._tasks:
            self._next_id = max(int(task.id) for task in self._tasks if task.id is not None) + 1

    def save_tasks(self) -> None:
        """Saves tasks to the file system."""
        _save_tasks_to_file(self.file_path, self._tasks)

    def create_task(self, task_create: TaskCreate, owner: str) -> Task:
        task = Task(id=str(self._next_id), owner=owner, **task_create.model_dump())
        self._tasks.append(task)
        self._next_id += 1
        self.save_tasks()
        return task

    def get_task(self, task_id: str, owner: str) -> Optional[Task]:
        for task in self._tasks:
            if task.id == str(task_id) and task.owner == owner:
                return task
        return None

    def list_tasks(self, owner: str) -> List[Task]:
        return [task for task in self._tasks if task.owner == owner]

    def update_task(self, task_id: str, task_update: TaskUpdate, owner: str) -> Optional[Task]:
        task = self.get_task(task_id, owner)
        if not task:
            return None
        
        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)
        
        self.save_tasks()
        return task

    def delete_task(self, task_id: str, owner: str) -> bool:
        task = self.get_task(task_id, owner)
        if task:
            self._tasks.remove(task)
            self.save_tasks()
            return True
        return False


class MongoTaskService(TaskService):
    """MongoDB implementation of the TaskService."""
    def __init__(self, connection_string: str):
        client = MongoClient(connection_string)
        # Get the default database from the connection string, or default to "taskdb"
        self.db = client.get_database() if client.get_database().name != 'test' else client.get_database("taskdb")
        self.tasks_collection = self.db.tasks

    def create_task(self, task_create: TaskCreate, owner: str) -> Task:
        task_data = task_create.model_dump()
        task_data["owner"] = owner
        result = self.tasks_collection.insert_one(task_data)
        # MongoDB generates an _id, we map it to our 'id' for the Pydantic model
        new_task = Task(id=str(result.inserted_id), **task_data)
        return new_task

    def get_task(self, task_id: str, owner: str) -> Optional[Task]:
        try:
            object_id = ObjectId(task_id)
        except Exception: # Catch InvalidId or other conversion errors
            return None
        
        task_data = self.tasks_collection.find_one({"_id": object_id, "owner": owner})
        if task_data:
            return Task(id=str(task_data["_id"]), **{k: v for k, v in task_data.items() if k != "_id"})
        return None

    def list_tasks(self, owner: str) -> List[Task]:
        tasks_data = list(self.tasks_collection.find({"owner": owner}))
        return [Task(id=str(task["_id"]), **{k: v for k, v in task.items() if k != "_id"}) for task in tasks_data]

    def update_task(self, task_id: str, task_update: TaskUpdate, owner: str) -> Optional[Task]:
        update_data = task_update.model_dump(exclude_unset=True)
        if not update_data:
            return self.get_task(task_id, owner) # No updates to apply

        try:
            object_id = ObjectId(task_id)
        except Exception: # Catch InvalidId or other conversion errors
            return None

        try:
            result = self.tasks_collection.update_one(
                {"_id": object_id, "owner": owner},
                {"$set": update_data}
            )
            if result.matched_count:
                return self.get_task(task_id, owner)
            return None
        except:
            return None # Invalid ObjectId


    def delete_task(self, task_id: str, owner: str) -> bool:
        try:
            object_id = ObjectId(task_id)
        except Exception: # Catch InvalidId or other conversion errors
            return False
        try:
            result = self.tasks_collection.delete_one({"_id": object_id, "owner": owner})
            return result.deleted_count > 0
        except:
            return False # Invalid ObjectId


class FileAuthService(AuthService):
    def __init__(self, users_file: str = USERS_FILE):
        self.users_file_path = Path(users_file)
        self._users = _load_users_from_file(self.users_file_path)

    def get_user(self, username: str) -> Optional[UserInDB]:
        return self._users.get(username)

    def create_user(self, user: User) -> UserInDB:
        if user.username in self.users:
            raise ValueError("Username already registered")
        hashed_password = pwd_context.hash(user.password)
        user_in_db = UserInDB(**user.model_dump(), hashed_password=hashed_password)
        self._users[user.username] = user_in_db
        _save_users_to_file(self.users_file_path, self._users)
        return user_in_db

    def authenticate_user(self, username: str, password: str) -> Optional[UserInDB]:
        user = self.get_user(username)
        if not user:
            return None
        if not pwd_context.verify(password, user.hashed_password):
            return None
        return user


class MongoAuthService(AuthService):
    """MongoDB implementation of the AuthService."""
    def __init__(self, connection_string: str):
        client = MongoClient(connection_string)
        # Get the default database from the connection string, or default to "userdb"
        self.db = client.get_database() if client.get_database().name != 'test' else client.get_database("userdb")
        self.users_collection = self.db.users

    def get_user(self, username: str) -> Optional[UserInDB]:
        user_data = self.users_collection.find_one({"username": username})
        if user_data:
            return UserInDB(**{k: v for k, v in user_data.items() if k != "_id"})
        return None

    def create_user(self, user: User) -> UserInDB:
        if self.get_user(user.username):
            raise ValueError("Username already registered")
        hashed_password = pwd_context.hash(user.password)
        user_in_db_data = user.model_dump()
        user_in_db_data["hashed_password"] = hashed_password
        self.users_collection.insert_one(user_in_db_data)
        return UserInDB(**user_in_db_data)

    def authenticate_user(self, username: str, password: str) -> Optional[UserInDB]:
        user = self.get_user(username)
        if not user:
            return None
        if not pwd_context.verify(password, user.hashed_password):
            return None
        return user


# --- Service Factories ---

def get_task_service(storage_uri: Optional[str] = None, test_file_path: Optional[str] = None) -> TaskService:
    """
    Factory function to get the appropriate task service based on the storage URI.
    """
    storage_uri = os.environ.get("STORAGE_URI", storage_uri or f"file://{DATA_FILE}")

    print("Task storage_uri:", storage_uri)

    if test_file_path:
        return FileTaskService(file_path=test_file_path)

    parsed_uri = urlparse(storage_uri)
    
    if parsed_uri.scheme == "in-memory":
        return InMemoryTaskService()
    elif parsed_uri.scheme == "file":
        path = storage_uri.replace("file://", "")
        return FileTaskService(file_path=path)
    elif parsed_uri.scheme in ["mongodb", "mongodb+srv"]:
        return MongoTaskService(connection_string=storage_uri)
    else:
        raise ValueError(f"Unsupported storage URI scheme: {parsed_uri.scheme}")

def get_auth_service(storage_uri: Optional[str] = None) -> AuthService:
    storage_uri = os.environ.get("STORAGE_URI", storage_uri or f"file://{USERS_FILE}")
    parsed_uri = urlparse(storage_uri)

    if parsed_uri.scheme == "file":
        path = storage_uri.replace("file://", "")
        return FileAuthService(users_file=path)
    elif parsed_uri.scheme in ["mongodb", "mongodb+srv"]:
        return MongoAuthService(connection_string=storage_uri)
    else:
        raise ValueError(f"Unsupported storage URI scheme for auth: {parsed_uri.scheme}")