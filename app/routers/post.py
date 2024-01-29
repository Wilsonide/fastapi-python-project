from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,status,HTTPException
from .. import models,schema,auth2
from ..database import get_db
from sqlalchemy import func
from typing import List

router = APIRouter(prefix="/blog",tags=["Blogs"])

@router.get("/",status_code=status.HTTP_200_OK,response_model=List[schema.PostOut])
async def read_root(db:Session = Depends(get_db),current_user:int = Depends(auth2.get_current_user)):
    post = db.query(models.Post).all()
    results = db.query(models.Post,func.count(models.Votes.post_id).label('votes')).join(models.Votes,models.Votes.post_id == models.Post.id,isouter=True).group_by(models.Post.id).all()
    return results

@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schema.PostOut)
async def read_hello(id: int,db:Session = Depends(get_db),current_user:int = Depends(auth2.get_current_user)):
    post = db.query(models.Post,func.count(models.Votes.post_id).label('votes')).join(models.Votes,models.Votes.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": "not found"}
    return post

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.Post)
async def create_blog(blog:schema.Post_create,db:Session = Depends(get_db),current_user:int = Depends(auth2.get_current_user)):
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **blog.dict())
    new_post.owner = current_user
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db:Session = Depends(get_db),current_user:int = Depends(auth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    #return Response(status_code=status.HTTP_204_NO_CONTENT)
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} is not found")
    deleted_post.delete(synchronize_session=False)
    db.commit()

@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED,response_model=schema.Post)
def update_post(id:int, posts:schema.Post_create,db:Session = Depends(get_db),user_id:int = Depends(auth2.get_current_user)):
    updated_post = db.query(models.Post).filter(models.Post.id == id)

    if not updated_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} not found")
    updated_post.update(posts.dict(),synchronize_session=False)
    db.commit()
    return updated_post.first()