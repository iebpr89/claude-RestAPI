from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Todo REST API", version="1.1.0")


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    completed: bool = False


class TodoUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    completed: bool | None = None


class Todo(TodoCreate):
    id: int


class TodoStore:
    """In-memory Todo storage. Not shared across processes and reset on restart."""

    def __init__(self) -> None:
        self._todos: dict[int, Todo] = {}
        self._next_id = 1

    def list(self) -> list[Todo]:
        return list(self._todos.values())

    def get(self, todo_id: int) -> Todo | None:
        return self._todos.get(todo_id)

    def add(self, data: TodoCreate) -> Todo:
        todo = Todo(id=self._next_id, **data.model_dump())
        self._todos[todo.id] = todo
        self._next_id += 1
        return todo

    def replace(self, todo_id: int, data: TodoCreate) -> Todo | None:
        if todo_id not in self._todos:
            return None
        todo = Todo(id=todo_id, **data.model_dump())
        self._todos[todo_id] = todo
        return todo

    def update(self, todo_id: int, data: TodoUpdate) -> Todo | None:
        existing = self._todos.get(todo_id)
        if existing is None:
            return None
        updated = existing.model_copy(update=data.model_dump(exclude_unset=True))
        self._todos[todo_id] = updated
        return updated

    def delete(self, todo_id: int) -> bool:
        return self._todos.pop(todo_id, None) is not None

    def clear(self) -> None:
        self._todos.clear()
        self._next_id = 1


store = TodoStore()


def get_store() -> TodoStore:
    return store


StoreDep = Annotated[TodoStore, Depends(get_store)]


def _not_found(todo_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo {todo_id} not found",
    )


@app.get("/todos", response_model=list[Todo])
def list_todos(store: StoreDep) -> list[Todo]:
    return store.list()


@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate, store: StoreDep) -> Todo:
    return store.add(payload)


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int, store: StoreDep) -> Todo:
    todo = store.get(todo_id)
    if todo is None:
        raise _not_found(todo_id)
    return todo


@app.put("/todos/{todo_id}", response_model=Todo)
def replace_todo(todo_id: int, payload: TodoCreate, store: StoreDep) -> Todo:
    todo = store.replace(todo_id, payload)
    if todo is None:
        raise _not_found(todo_id)
    return todo


@app.patch("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, payload: TodoUpdate, store: StoreDep) -> Todo:
    todo = store.update(todo_id, payload)
    if todo is None:
        raise _not_found(todo_id)
    return todo


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, store: StoreDep) -> None:
    if not store.delete(todo_id):
        raise _not_found(todo_id)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Todo REST API. See /docs for the interactive documentation."}
