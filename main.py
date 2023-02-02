from fastapi import FastAPI
from routes.user import user
from routes.task import task
app = FastAPI()
app.include_router(user)
app.include_router(task)
@app.get('/')
async def home():
    return {"message":"Hello,World"}



