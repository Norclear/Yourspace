from mysql.connector import pooling, PoolError
from dotenv import load_dotenv
import os
from sql_models import *

load_dotenv()

# This file contains all functions related to the the Yourspace server database.
# Draws environment variables from the operating system with the OS library.

connection_pool_size = 10

# Here we define a function that will initiate a pool of database connections.
# Rather than constantly opening and closing connections for each query (This is highly inefficient)
# We can create a 'pool' of connections that we can simply use when we need them, when we are done with 
# them we can return them to the pool for later use, but the pool of connections will always remain open.
def initiate_pool():
    try:

        # Initiate our connection pool 'pointer' that will, it is initiated and immediately defining all of it's essential properties
        # which are stored as operating system environment/run-time variables for security purposes.
        connection_pool = pooling.MySQLConnectionPool(
            pool_name=os.getenv('pool_name'),
            pool_size=connection_pool_size,
            pool_reset_session=True,
            host=os.getenv('database_hostname'),
            database=os.getenv('database_name'),
            user=os.getenv('database_username'),
            password=os.getenv('database_password')
            )
        
        return connection_pool
    
    except PoolError:
        print(PoolError)

# This function will run one time on server initialisation to create any tables if necessary.
def create_table(_connection_pool, sql: str):
    try:
         connection = _connection_pool.get_connection()
    except PoolError:
        print(PoolError)

    cursor = connection.cursor()
    cursor.execute(sql)
    connection.close()

# This function will create a new instance of a user in the database.
def create_user(_connection_pool, user):
    try:
        connection = _connection_pool.get_connection()
        cursor = connection.cursor(buffered=True)
        cursor.execute(user_create_sql,(user.username,user.password,user.permissions, user.pfp))

        connection.commit()
        connection.close()

    except PoolError:
        print(PoolError)
        return PoolError

# This function will query the database using a username and return all other account details.
def query_username(_connection_pool,username):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)

    cursor.execute(query_username_sql,(username,))
    result = cursor.fetchone()

    connection.close()
    return result

# This function will return a user's hashed password when given a username.
def query_password(_connection_pool,username):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)

    cursor.execute(query_password_sql,(username,))
    result = cursor.fetchone()

    connection.close()
    return result[0]

# This function will return the user ID of a user given their username.
def username_to_id(_connection_pool,username):
    connection = _connection_pool.get_connection() 
    cursor = connection.cursor(buffered=True)

    cursor.execute(username_to_id_sql,(username,))
    result = cursor.fetchone()

    connection.close()
    return result[0]

# This function will return the username of a user given their user ID.
def id_to_username(_connection_pool, id):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)

    cursor.execute(id_to_username_sql, (id,))
    result = cursor.fetchone()

    connection.close()
    return result[0]

# This function will return the user permission levels given their user ID.
def query_permissions(_connection_pool,id):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)
    
    cursor.execute(query_permissions_sql,(id,))    
    result = cursor.fetchone()

    connection.close()
    return result[0]

# This function will return the following user details: reg_date, permissions, profile_picture 
# Given a username
def query_account(_connection_pool,username):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)
    
    cursor.execute(query_account_sql, (username,))
    result = cursor.fetchone()

    connection.close()
    if not result:
        return False
    
    return result

# This function will create a post that is tied to a user.
def create_post(_connection_pool,user_id,title,descrption,attachment,private):
    try:
        connection = _connection_pool.get_connection()
        cursor = connection.cursor(buffered=True)
        cursor.execute(create_post_sql, (title, descrption,
                       attachment, user_id, private))
        connection.commit()

    except PoolError:
        print(PoolError)
        return PoolError
    
    connection.close()

# Will return all details of a post given a specific post ID.
def get_post_by_id(_connection_pool,id):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)
    
    cursor.execute(get_post_by_id_sql, (id,))
    result = cursor.fetchone()

    connection.close()
    
    return result

# Will get the profile picture of a user.
def get_pfp(_connection_pool,username):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)
    
    cursor.execute(get_pfp_sql, (username,))
    result = cursor.fetchone()

    connection.close()
    
    return result

# Will run an extensive database search query to search for a user based on certain parameters
def search_users(_connection_pool,query):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)
    
    cursor.execute(search_users_sql, (query, query, query, query))
    result = cursor.fetchall()

    connection.close()
    
    return result

# Will run an extensive database search query to search for a post based on certain parameters
def search_posts(_connection_pool, query):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)

    cursor.execute(search_posts_sql, (query, query,
                   query, query, query, query))
    result = cursor.fetchall()

    connection.close()

    return result

# Returns all the posts by a certain user given their user ID
def get_user_posts(_connection_pool,id):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)

    cursor.execute(get_user_posts_sql, (id,))
    result = cursor.fetchall()

    connection.close()

    return result

# Deletes a post from the database given the post ID.
def delete_post(_connection_pool, id):
    try:
        connection = _connection_pool.get_connection()
        cursor = connection.cursor(buffered=True)

        cursor.execute(delete_post_sql, (id,))
        connection.commit()

        connection.close()
    except PoolError:
        print(PoolError)
        return PoolError

# Updates the details of a post given the post ID and the new details of the post 
# being the title and description.
def update_post(_connection_pool,id,title,description):
    try:
        connection = _connection_pool.get_connection()
        cursor = connection.cursor(buffered=True)

        cursor.execute(edit_post_sql, (title,description,id))
        connection.commit()

        connection.close()
    except PoolError:
        print(PoolError)
        return PoolError
    
# Will create a new comment attached to a specific post and user
def create_comment(_connection_pool,post_id,username,comment):
    try:
        connection = _connection_pool.get_connection()
        cursor = connection.cursor(buffered=True)

        cursor.execute(create_comment_sql, (post_id, username, comment))
        connection.commit()

        connection.close()
    except PoolError:
        print(PoolError)
        return PoolError
    
# Returns all the comments for one post given the post ID.
def get_post_comments(_connection_pool, id):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)

    cursor.execute(get_comments_sql, (id,))
    result = cursor.fetchall()

    connection.close()

    return result

# Gets all the details of a comment given a comment ID.
def get_comment(_connection_pool, id):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)

    cursor.execute(get_comment_sql, (id,))
    result = cursor.fetchall()

    connection.close()

    return result

# Runs a query to delete a comment from the database.
def delete_comment(_connection_pool, id):
    try:
        connection = _connection_pool.get_connection()
        cursor = connection.cursor(buffered=True)

        cursor.execute(delete_comment_sql, (id,))
        connection.commit()

        connection.close()
    except PoolError:
        print(PoolError)
        return PoolError

# Returns a feed of all posts on the site, is returned most recent first to oldest last.
def get_feed(_connection_pool):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)

    cursor.execute(feed_sql)
    result = cursor.fetchall()

    connection.close()

    return result

# Runs a query to delete a user's account, all associated details, their posts and comments.
def delete_user(_connection_pool, username):
    try:
        connection = _connection_pool.get_connection()
        cursor = connection.cursor(buffered=True)

        result = cursor.execute(delete_user_sql, (username,))
        connection.commit()

        connection.close()
        return result
    except PoolError:
        print(PoolError)
        return PoolError
    
connection_pool = initiate_pool() # create a pool of connections to the mysql database, they are in constant existance and there is 10, can be changed by poolsize in database.py