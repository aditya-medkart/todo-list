from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from pathlib import Path
import uvicorn

app2 = FastAPI()
BASE_DIR =Path(__file__).resolve().parent

MONGO_URI = "mongodb://localhost:27017/myDatabase"
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database()
collection = db.todo_list

templates = Jinja2Templates(directory=str(Path(BASE_DIR,'templates')))

@app2.get("/", response_class=HTMLResponse)
async def index(request: Request):
    todo_list = await collection.find().to_list(None)
    return templates.TemplateResponse("index.html", {"request": request, "todo_list": todo_list})

@app2.post("/add")
async def add_todo(new_todo: str = Form(), new_description: str = Form()):
    if new_todo:
        new_task = {'todo': new_todo, 'description': new_description, 'status': 'Pending'}
        await collection.insert_one(new_task)
    return RedirectResponse(url="/", status_code=302)

@app2.get("/update_status/{_id}/{status}")
async def update_status( id: str ,status: str):
    print(status)
    valid_statuses = ['Pending', 'In Progress', 'Testing', 'Done']
    if status in valid_statuses:
        await collection.update_one({'_id': ObjectId(id)}, {'$set': {'status': status}})
    return RedirectResponse(url="/", status_code=302)

@app2.get("/delete/{_id}")
async def delete_todo(id: str):
    await collection.delete_one({'_id': ObjectId(id)})
    return RedirectResponse(url="/", status_code=302)

uvicorn.run(app2, host="127.0.0.1", port=8000)