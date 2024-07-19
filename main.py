from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from uuid import uuid4
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Annotated, Union
from fastapi import FastAPI, Header, Request




app = FastAPI()
templates = Jinja2Templates(directory="templates")

# create in-memory Todo model; usecase for dataclass
class Todo:
    def __init__(self, title):
        self.id = uuid4()
        self.title = title
        self.done = False

todos = []
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/todos", response_class=HTMLResponse)
async def list_todos(request: Request, hx_request: Annotated[Union[str, None], Header()] = None):
    if hx_request:
        return templates.TemplateResponse(
            request=request, name="todos.html", context={"todos": todos}
        )
    return JSONResponse(content=jsonable_encoder(todos))


@app.post("/todos", response_class=HTMLResponse)
async def create_todo(request: Request, todo: Annotated[str, Form()]):
    todos.append(Todo(todo))
    return templates.TemplateResponse(
        request=request, name="todos.html", context={"todos": todos}
    )

@app.put("/todos/{todo_id}", response_class=HTMLResponse)
async def update_todo(request: Request, todo_id: str, title:Annotated[str, Form()]):
    for todo in todos:
        if str(todo.id) == todo_id:
            todo.title = title
            break
    return templates.TemplateResponse(
        request=request, name="todos.html", context={"todos": todos}
    )