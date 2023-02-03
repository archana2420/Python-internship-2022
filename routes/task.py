from schemas.user import *
from services.user import *
from models.task import Task
from models.user import User
from config.db import conn
from bson import ObjectId
from fastapi import HTTPException



async def find_all_tasks(user:User):
    return serializeList(conn.local.task.find({"owner":user["username"]}))
    


async def add_task(user:User,todo:Task):
    todo = dict(todo)
    new_task = {**todo,"owner":user["username"]}
    conn.local.task.insert_one(new_task)
    return serializeList(conn.local.task.find({"owner":user["username"]}))


async def update_task(todo:Task,id,user:User):
    try:
        conn.local.task.find_one_and_update({"_id":ObjectId(id),"owner":user["username"]},{
        "$set":dict(todo)
        })
        return serializeDict(conn.local.task.find_one({"_id":ObjectId(id)}))
    except:
        return HTTPException(status_code=404,detail="ID not found!")


async def delete_task(id,user:User):
    try:
        res = conn.local.task.find_one_and_delete({"_id":ObjectId(id),"owner":user["username"]})
        serializeDict(res)
        return {"Message":"Deleted Successfully!"}
    except:
        return HTTPException(status_code=404,detail="ID not found!")