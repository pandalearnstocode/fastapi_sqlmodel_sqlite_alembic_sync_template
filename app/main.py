from fastapi import FastAPI, Depends
from sqlmodel import Session
from app.db import create_db_and_tables, get_session
from app.models import Task, TaskCreate

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/ping")
def pong():
    return {"ping": "pong!"}

@app.post("/task/", response_model=Task)
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    db_task = Task.from_orm(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task