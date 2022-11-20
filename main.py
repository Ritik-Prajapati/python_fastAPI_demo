from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published_by: Optional[str] = None
    rating: Optional[int] = None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "title of post 2", "content": "content of post 2", "id": 2}]

def find_post(id):
    # print(id, type(id))
    for p in my_posts:
        if p['id'] == id:
            return p

def find_post_index(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i
    return None

        

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def root():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/latest")
async def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"Newest post": post}


@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found!")

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} not found!"}
    return {"post requested": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist!")
    
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found!")
    
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}