from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from database import create_table,connection_pool
from sql_models import user_table, post_table, comment_table
from routers import user, authorise, post, filter, comment, admin

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'DELETE', 'PUT'],
    allow_headers=['*']
)


create_table(connection_pool,user_table) # create the users table using the connection pool and the sql model from models.py
create_table(connection_pool,post_table)
create_table(connection_pool,comment_table)



app.include_router(user.router)
app.include_router(authorise.router)
app.include_router(post.router)
app.include_router(filter.router)
app.include_router(comment.router)
app.include_router(admin.router)




@app.get("/", status_code=status.HTTP_200_OK)  # root url, will remain out of use .
def root():
    return {"Root url for Yourspace internal API"}

