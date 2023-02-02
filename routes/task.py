from fastapi import APIRouter
from schemas.user import serializeDict,serializeList
from models.task import Task
from config.db import conn
from bson import ObjectId

task = APIRouter()

@task.get('/task/get/')
async def find_all_tasks():
    return serializeList(conn.local.task.find())

@task.post('/task/add/')
async def add_task(todo:Task):
    conn.local.task.insert_one(dict(todo))
    return serializeList(conn.local.task.find())

@task.put('/task/update/{id}')
async def update_task(id,task:Task):
    conn.local.task.find_one_and_update({"_id":ObjectId(id)},{
    "$set":dict(task)
    })
    return serializeDict(conn.local.task.find_one({"_id":ObjectId(id)}))

@task.delete('/task/delete/{id}')
async def delete_task(id):
    return serializeDict(conn.local.task.find_one_and_delete({"_id":ObjectId(id)}))