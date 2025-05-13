from pydantic import BaseModel, EmailStr, constr, field_validator
from datetime import date
from typing import Optional, Annotated

class UserCreate(BaseModel):
    username:  Annotated[str, constr(min_length=3, max_length=20)]
    email: EmailStr

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: date
    status: str = "pending"

    @field_validator("due_date")
    @classmethod
    def due_date_cannot_be_in_past(cls, v):
        if v < date.today():
            raise ValueError("Due date cannot be in the past")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        allowed_statuses = {"pending", "in_progress", "completed"}
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of: {allowed_statuses}")
        return v

class TaskCreate(TaskBase):
    user_id: int

class Task(TaskBase):
    id: int
    user_id: int
