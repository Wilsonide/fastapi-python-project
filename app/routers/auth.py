from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schema,utils,auth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from datetime import datetime,timedelta
from ..settings import setting



router = APIRouter(tags=["Authentication"])

@router.post("/register",status_code=status.HTTP_201_CREATED,response_model=schema.User)
def create_user(user:schema.User_create,db:Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login",response_model=schema.Token)
def login(user_data:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    expires_min = setting.ACCESS_TOKEN_EXPIRE_MINUTES
    user = db.query(models.User).filter(models.User.email == user_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credentials")
    if not utils.verify(user_data.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credentials")
    access_token = auth2.create_access_token(data={"user_id":user.id ,"expires": expires_min})
    return {"access_token":access_token,"token_type":"bearer"}