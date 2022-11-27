from fastapi import FastAPI, Response, status, HTTPException

app = FastAPI()

my_posts = [{"id": 1 , "title": "title of post 1", "content": "content of post 1"},
            {"id": 2 , "title": "favorite foods", "content": "I like pizza"}]

def find_post(id):
    pass

@app.get("/posts/{id}")
def get_posts(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'Post with id: {id} was not found.')
    return {"data": post}