from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)
collection = mongo.db.todo_list

@app.route('/')
def index():
    todo_list = collection.find()
    return render_template('index.html', todo_list=todo_list)

@app.route('/add', methods=['POST'])
def add_todo():
    new_todo = request.form.get('new_todo')
    new_description = request.form.get('new_description')
    if new_todo:
        new_task = {'todo': new_todo, 'description': new_description, 'status': 'Pending'}
        collection.insert_one(new_task)
    return redirect(url_for('index'))

@app.route('/update_status/<ObjectId:_id>/<status>')
def update_status(_id, status):
    valid_statuses = ['Pending', 'In set Progress', 'Testing', 'Done']
    if status in valid_statuses:
        collection.update_one({'_id': _id}, {'$set': {'status': status}})
    return redirect(url_for('index')) 

@app.route('/delete/<ObjectId:_id>')
def delete_todo(_id):
    collection.delete_one({'_id': _id})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5002)
