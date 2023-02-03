from fastapi import FastAPI,Depends
from models.user import User
from routes.user import user
from routes.task import *
from services.user import get_current_user
from schemas.task import Todo
from services.user import auth

app = FastAPI()
app.include_router(user)
app.include_router(auth)


@app.get('/',summary="List all the todos")
async def all_tasks(current_user:User = Depends(get_current_user)):
    '''
    Retrieve all the tasks that belongs to the current user
    '''
    return await find_all_tasks(current_user)


@app.post('/create',summary="Create a todo")
async def create_todo(data:Todo,current_user:User=Depends(get_current_user)):
    '''
    Create a task that belongs to the current user
    '''
    return await add_task(current_user,data)


@app.put('/update',summary="Update a todo")
async def update_todo(data:Todo,id:str,current_user:User=Depends(get_current_user)):
    '''
    Update a task that belongs to the current user
    '''
    return await update_task(data,id,current_user)


@app.delete('/delete',summary="Delete a todo")
async def delete_todo(id:str,current_user:User=Depends(get_current_user)):
    '''
    Delete a task that belongs to the current user
    '''
    return await delete_task(id,current_user)
    



