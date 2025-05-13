from typing import List
from fastapi import FastAPI, HTTPException
from schemas import UserCreate, UserRead, TaskCreate, Task
from models import users_db, tasks_db

app = FastAPI()

# Auto-incrementing IDs
user_id_counter = 1
task_id_counter = 1

@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate):
    global user_id_counter
    new_user = UserRead(id=user_id_counter, **user.dict())
    users_db.append(new_user)
    user_id_counter += 1
    return new_user

@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate):
    global task_id_counter
    # Verify user exists
    if not any(user.id == task.user_id for user in users_db):
        raise HTTPException(status_code=404, detail="User not found")
    new_task = Task(id=task_id_counter, **task.dict())
    tasks_db.append(new_task)
    task_id_counter += 1
    return new_task

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
def update_task_status(task_id: int, status: str):
    allowed_statuses = {"pending", "in_progress", "completed"}
    if status not in allowed_statuses:
        raise HTTPException(status_code=400, detail=f"Status must be one of: {allowed_statuses}")
    for task in tasks_db:
        if task.id == task_id:
            task.status = status
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/users/{user_id}/tasks", response_model=List[Task])
def get_user_tasks(user_id: int):
    # Verify user exists
    if not any(user.id == user_id for user in users_db):
        raise HTTPException(status_code=404, detail="User not found")
    user_tasks = [task for task in tasks_db if task.user_id == user_id]
    return user_tasks
