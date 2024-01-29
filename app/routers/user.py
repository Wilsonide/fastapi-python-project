from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from .. import models,schema,utils
from ..database import get_db

router = APIRouter(prefix="/user",tags=["Users"])



@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schema.User)
def get_user(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found")
    return user