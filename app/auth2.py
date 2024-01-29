from jose import JWTError, jwt
from datetime import datetime,timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from .database import get_db
from . import models,schema
from .settings import setting



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data:dict):
    to_encode = data.copy()
    """ expire = datetime.utcnow()+timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire}) """
    encoded_jwt = jwt.encode(to_encode,setting.SECRET_KEY,algorithm=setting.ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,setting.SECRET_KEY,algorithms=[setting.ALGORITHM])
        expire = payload.get("expires")
        print("hellllllllllllllllllllllllllllllllllllllllllllllo worlddddddddddddddddddddddddddddddddddddddddddddd!!!!!!!")
        print(expire)
        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied",
            )
        if datetime.utcnow() > datetime.utcnow()+timedelta(minutes=expire):
            print (expire)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Token expired!"
            )
        
        """ user_id : str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception """
        id = payload.get("user_id")
        token_data = schema.Token_data(id=id)
        return token_data
    except JWTError:
        raise credentials_exception
    

def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user

