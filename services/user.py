from fastapi import APIRouter,Depends,HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from config.db import conn
import jwt
from schemas.user import *

SECRET_KEY = "secret"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token:str = Depends(oauth2_scheme)):
    '''
    Returns the current user after decoding the token 
    '''
    try :
        payload = jwt.decode(
            token,SECRET_KEY,algorithms=[ALGORITHM]
        )
        
        user = get_user(payload["user"])
        if user:
            user = conn.local.user.find_one({"username":payload["user"]})
            

    except:
        raise HTTPException(status_code=401,detail="Invalid Email or Password")
    
    return serializeDict(user)

def get_user(username):
    '''
    A function to find if user exists or not
    '''
    user = conn.local.user.find_one({"username":username})
    if user:
        return True
    return False


def authenticate_user(username,password):
    '''
    A function to check if the user exists and if the password is correct
    '''
    try:
        user = get_user(username)
        if user:
            user = conn.local.user.find_one({"username":username})
            user = serializeDict(user)
            
            password_check = pwd_context.verify(password,user['password'])

            return password_check
    except :
        return False

def create_access_token(data :dict):
    '''
    Creating an access token using JWT
    '''
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm = ALGORITHM)
    return encoded_jwt

auth = APIRouter()

@auth.post("/token")
def login(form_data:OAuth2PasswordRequestForm = Depends()):
    '''
    Function to login and create access token 
    '''
    username = form_data.username
    password = form_data.password
    
    if authenticate_user(username,password):
        access_token = create_access_token(
            data = {"user":username}
        )
        return {"access_token":access_token,"token_type":"bearer"}
    else:
        raise HTTPException(status_code=400,detail="Incorrect username or password")


@auth.get('/user/auth')
def get_token(token:str = Depends(oauth2_scheme)):
    return {"token":token}

pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")

def get_hashed_password(password):
    '''
    Returns hashed password
    '''
    return pwd_context.hash(password)



