from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Todo REST API", version="1.0.0")


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    completed: bool = False


class Todo(TodoCreate):
    id: int


_todos: list[Todo] = []
_next_id = 1


@app.get("/todos", response_model=list[Todo])
def list_todos() -> list[Todo]:
    return _todos


@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate) -> Todo:
    global _next_id
    todo = Todo(id=_next_id, **payload.model_dump())
    _todos.append(todo)
    _next_id += 1
    return todo


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Todo REST API. See /docs for the interactive documentation."}
