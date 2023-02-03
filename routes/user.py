from fastapi import APIRouter
from bson import ObjectId
from models.user import User
from config.db import conn
from schemas.user import *
from services.user import *

user = APIRouter() # An API Router to include the routes in main.py

@user.post("/user/sign-up/")
async def user_sign_up(user:User):
    '''
    A function to create a user
    '''
    curr_user = get_user(user.username)
    if curr_user!=True:
        user.password = get_hashed_password(user.password)
        conn.local.user.insert_one(dict(user))
        return serializeList(conn.local.user.find())

    else:
        return {"Error":"User already exisits!"}

    
   

@user.get('/user/get/')
async def find_all_user():
    '''
    Retrieve all the users
    '''
    return serializeList(conn.local.user.find())



@user.put('/user/update/{id}')
async def update_user(id,user:User):
    '''
    Update user details
    '''
    conn.local.user.find_one_and_update({"_id":ObjectId(id)},{
    "$set":dict(user)
    })
    return serializeDict(conn.local.user.find_one({"_id":ObjectId(id)}))

@user.delete('/user/delete/{id}')
async def delete_user(id):
    '''
    Delete the user
    '''
    try:
        res = conn.local.user.find_one_and_delete({"_id":ObjectId(id)})
        serializeDict(res)
        return {"Message":"Deleted Successfully!"}
    except:
        return HTTPException(status_code=404,detail="ID not found!")
    
