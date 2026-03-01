from .. import model,schema,utils,oauth2
from fastapi import Response,status,HTTPException,Depends,APIRouter
from ..database import get_db
from typing import Optional
from sqlalchemy.orm import Session 
from sqlalchemy import func

router=APIRouter(
    prefix="/posts",
    tags=['Posts'] 
    )
# while True:
#     try:
#         conn=cnx = mysql.connector.connect(
#         port=3306,
#         user="root",
#         database="product")
        
#         cur = cnx.cursor()
#         print("database connection done")
#         break
#     except Exception as error:
#         print("connetion failed")
#         print(error)
#         time.sleep(2)



# my_posts=[{"title":"title of post 1","content":"content of post 1","id":1},
#           {"title":"title of post 2","content":"content of post 2","id":2}]

# def find_post(id):
#     for p in my_posts:
#         if p["id"]== id:
#             return p

# def find_index_post(id):
#     for i ,p in enumerate(my_posts):
#         if p['id']==id: 
#             return i
#         else:
#             return 0




@router.get("/",response_model=list[schema.PostOut])
def get_posts(db:Session = Depends(get_db),current_user:model.User =Depends(oauth2.get_current_user)
              ,limit:int=10,skip:int=0,search:Optional[str]=" "):
    print(current_user.email)
    post=db.query(model.Post,func.count(model.Vote.post_id).label('votes')).join(
        model.Vote,model.Vote.post_id==model.Post.id,isouter=True).group_by(
            model.Post.id).filter(
                model.Post.title.contains(search)).limit(limit).offset(skip).all()

    return post


# #show all posts
# @app.get("/posts")
# def get_posts(db:Session = Depends(get_db)):
#     cur.execute("""SELECT * from post""")
#     posts=cur.fetchall()
#     return posts}

#create post
#in this we are storing the data to the database if available if not we have made a variable 

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.PostResponse)
def userPost(post:schema.PostCreate,db:Session = Depends(get_db),current_user: model.User = Depends(oauth2.get_current_user)
):

    new_post=model.Post(user_id=current_user.id ,**post.model_dump())
    # cur.execute("""INSERT INTO post(title,content) VALUES(%s,%s) """,(post.title,post.content))
    # new_post=cur.fetchone()
    # conn.commit()
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# we use a path paramter to find specific the posts that we did 

#get specific post
@router.get("/{id}",response_model=schema.PostOut)
def get_post(id: int,db:Session = Depends(get_db)):
    # my_post=db.query(model.Post)
    # cur.execute("""select *  from post where id=%s""",(str(id),))
    # post=cur.fetchone()

    my_post=db.query(model.Post,func.count(model.Vote.post_id).label('votes')).join(
        model.Vote,model.Vote.post_id==model.Post.id,isouter=True).group_by(
            model.Post.id).filter(model.Post.id==id).first()
    if not my_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post not found")
    else:
        return my_post








@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.get_current_user)
):
    post = db.query(model.Post).filter(model.Post.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="data not found"
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )

    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


    # cur.execute(""" DELETE FROM post where id=%s""",(str(id),))
    # index=cur.fetchone()
    # conn.commit()
    # cur.execute("SELECT * FROM post WHERE id=%s;", (id,))
    # if index is None:
    #     return Response(status_code=status.HTTP_404_NOT_FOUND)
    # else:
    #     

@router.put("/{id}",response_model=schema.PostResponse)
def update_post(id:int,post:schema.PostCreate,db:Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    post_query=db.query(model.Post).filter(model.Post.id==id)
    updated_post =post_query.first()

    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="data doesnt exist")
    if updated_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )
    else:
        post_query.update({getattr(model.Post, key): value for key, value in post.model_dump().items()}, synchronize_session=False)
        db.commit()
        return post_query.first()




# @app.put("/posts/{id}")
# def update_post(id:int,post:Post,db:Session = Depends(get_db)):
#     updated_post=db.query(model.Post).filter(model.Post.id==id)
    
#     post=updated_post.first()
#     # cur.execute("""UPDATE post SET title=%s,content=%s where id= %s;""",(post.title,post.content,str(id),))
#     # conn.commit()
#     # cur.execute("SELECT * FROM post WHERE id=%s;", (str(id),))
#     # updated_post = cur.fetchone()    
#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sorry")
#     updated_post.update(model.Post(post.model_dump()),synchronize_session=False)
#     db.commit()
#     return updated_ost.first()}
# # @app.get("/posts/latest")
# # def get_latest_post():
# #     post=my_posts[len(my_posts)-1]
# #     return {"detail":post}




