from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["myDatabase"]
collection = db["todo_list"]

templates = Jinja2Templates(directory="templates")

@app.get('/')
async def index(request: Request):
    todo_list = collection.find()
    return templates.TemplateResponse("index.html", {"request": request, "todo_list": todo_list})

@app.post('/add')
async def add_todo(request: Request, new_todo: str = Form(...), new_description: str = Form(...)):
    new_task = {'todo': new_todo, 'description': new_description, 'status': 'Pending'}
    collection.insert_one(new_task)
    return {"message": "Todo added successfully"}

@app.get('/update_status/{todo_id}/{status}')
async def update_status(todo_id: str, status: str):
    valid_statuses = ['Pending', 'In Progress', 'Testing', 'Done']
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    collection.update_one({'_id': ObjectId(todo_id)}, {'$set': {'status': status}})
    return {"message": "Status updated successfully"}

@app.get('/delete/{todo_id}')
async def delete_todo(todo_id: str):
    collection.delete_one({'_id': ObjectId(todo_id)})
    return {"message": "Todo deleted successfully"}
