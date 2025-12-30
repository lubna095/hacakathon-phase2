from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Optional 

class Task(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    completed: bool = False
    owner: str

class TaskCreate(BaseModel):
    name: str
    description: str

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class User(BaseModel):
    username: str
    password: Optional[str] = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


class AuthService(ABC):
    @abstractmethod
    def get_user(self, username: str) -> Optional[UserInDB]:
        pass

    @abstractmethod
    def create_user(self, user: User) -> UserInDB:
        pass

    @abstractmethod
    def authenticate_user(self, username: str, password: str) -> Optional[UserInDB]:
        pass
