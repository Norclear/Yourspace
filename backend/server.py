from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from database import create_table,connection_pool
from sql_models import user_table, post_table, comment_table
from routers import user, authorise, post, filter, comment, admin

# Initiate the fast api server.
app = FastAPI()

origins = ['*']

# Set key properties such as request types and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'DELETE', 'PUT'],
    allow_headers=['*']
)

# Attempt to create all required tables.
create_table(connection_pool,user_table)
create_table(connection_pool,post_table)
create_table(connection_pool,comment_table)


# Include routers to all sub routes for the api.
app.include_router(user.router)
app.include_router(authorise.router)
app.include_router(post.router)
app.include_router(filter.router)
app.include_router(comment.router)
app.include_router(admin.router)



# The root url, has no purpose
@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"Root url for Yourspace internal API"}

