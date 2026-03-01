from .. import model,schema,utils,database,oauth2
from fastapi import FastAPI, Body,Response,status,HTTPException,Depends,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session 

router=APIRouter(
    prefix="/vote",
    tags=['Votes']
)


@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schema.Vote,db:Session=Depends(database.get_db),current_user: model.User = Depends(oauth2.get_current_user)):

    vote_query=db.query(model.Vote).filter(model.Vote.post_id==vote.post_id,model.Vote.user_id==current_user.id)
    found_vote=vote_query.first()
    if (vote.dir==True):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"{current_user.id} has voted already")
        new_vote=model.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"voted successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote not found")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Sussefylly deleted vote"}
    



