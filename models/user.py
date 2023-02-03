from pydantic import BaseModel

# A model as well as a validator for the User's input
class User(BaseModel):
    name:str
    username:str
    password:str