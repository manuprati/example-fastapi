from typing import List, Optional

from sqlalchemy import func

from app import oauth2
from .. import models,schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session 
from ..database import  get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# @router.get("/")
@router.get("/", response_model=List[schemas.Post])
def get_data(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int =10, skip:int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(current_user.email,current_user.password)

    # result = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    # print(result)

    return posts




@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print(current_user.id)
    new_post= models.Post(owner_id=current_user.id ,**post.dict())
    # new_post = models.Post(title=post.title,content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # cursor.execute("""INSERT INTO posts(title,content,published) values(%s, %s, %s) RETURNING *""",(post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 10000000)
    # my_posts.append(post_dict)
    return  new_post

# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title {payload['title']} content:{payload['content']}"}


# @app.get("/posts/{id}")
# def get_post(id):
#     print(id)
#     return {"post details": f"Hear is post {id}"}
# @app.get("/posts/latest")
# def latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"details":post}


@router.get("/{id}",response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  # , response: Response)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(post)

    # post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    # # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    # print(test_post)
    # post = find_post(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with id {id} was not found")
    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"you are not authorised to perform the desired action")
    
        # response.status_code =  status.HTTP_404_NOT_FOUND
        # return {"msg": f"The post with id {id} was not found"}
    return  post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # logic to delete a post is to find the index of element and pop the element at the index
    # cursor.execute(""" DELETE FROM posts WHERE id = %s returning * """,(str(id),))
    # del_post = cursor.fetchone()
    # index = find_index(id)

    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"The post with id={id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"you are not authorised to perform the desired action")

    post_query.delete(synchronize_session=False)
    db.commit()
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    #{"msg":"The post was successfully deleted"}


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(''' UPDATE posts SET title=%s, content=%s,published=%s WHERE id=%s RETURNING *''',(post.title,post.content,post.published,str(id)))
    # updated_posts = cursor.fetchone()
    # conn.commit()
    
    # index = find_index(id)

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"The post with id={id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"you are not authorised to perform the desired action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    # post_dict = dict(post)
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    return post_query.first()