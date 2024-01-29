from app import auth2, database, models, schema
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status, HTTPException
router = APIRouter(prefix='/vote', tags=['Likes/Unlike'])


@router.post('', status_code=status.HTTP_201_CREATED)
def Reaction(data: schema.Vote, current_user: int = Depends(auth2.get_current_user), db: Session = Depends(database.get_db)):

    post = db.query(models.Post).filter(models.Post.id == data.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id of {data.post_id} not found")

    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == data.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if data.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'user {current_user.id} has already voted on this post')
        new_vote = models.Votes(post_id=data.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": 'successfully added vote'}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f'Could not find vote')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message': 'successfully deleted vote'}
