from mysql.connector import pooling, PoolError
from dotenv import load_dotenv
import os
from sql_models import *
load_dotenv()

def initiate_pool(): # create a pool of connections to the DB (10 connections)
    try:
        connection_pool = pooling.MySQLConnectionPool(
            pool_name=os.getenv('pool_name'),
            pool_size=10,
            pool_reset_session=True,
            host=os.getenv('database_hostname'),
            database=os.getenv('database_name'),
            user=os.getenv('database_username'),
            password=os.getenv('database_password')
            )
        return connection_pool
    except PoolError:
        print(PoolError)

def create_table(_connection_pool, sql: str): # execute given sql to create a table
    try:
         connection = _connection_pool.get_connection()
    except PoolError:
        print(PoolError)

    cursor = connection.cursor()
    cursor.execute(sql)
    connection.close()

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
    
def query_username(_connection_pool,username):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)

    cursor.execute(query_username_sql,(username,))
    result = cursor.fetchone()

    connection.close()
    return result

def query_password(_connection_pool,username):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)

    cursor.execute(query_password_sql,(username,))
    result = cursor.fetchone()

    connection.close()
    return result[0]

def username_to_id(_connection_pool,username):
    connection = _connection_pool.get_connection() 
    cursor = connection.cursor(buffered=True)

    cursor.execute(username_to_id_sql,(username,))
    result = cursor.fetchone()

    connection.close()
    return result[0]


def id_to_username(_connection_pool, id):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)

    cursor.execute(id_to_username_sql, (id,))
    result = cursor.fetchone()

    connection.close()
    return result[0]

def query_permissions(_connection_pool,id):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)
    
    cursor.execute(query_permissions_sql,(id,))    
    result = cursor.fetchone()

    connection.close()
    return result[0]

def query_account(_connection_pool,username):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)
    
    cursor.execute(query_account_sql, (username,))
    result = cursor.fetchone()

    connection.close()
    if not result:
        return False
    
    return result

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

def get_post_by_id(_connection_pool,id):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)
    
    cursor.execute(get_post_by_id_sql, (id,))
    result = cursor.fetchone()

    connection.close()
    
    return result

def get_pfp(_connection_pool,username):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)
    
    cursor.execute(get_pfp_sql, (username,))
    result = cursor.fetchone()

    connection.close()
    
    return result

def search_users(_connection_pool,query):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)
    
    cursor.execute(search_users_sql, (query, query, query, query))
    result = cursor.fetchall()

    connection.close()
    
    return result

def search_posts(_connection_pool, query):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)

    cursor.execute(search_posts_sql, (query, query,
                   query, query, query, query))
    result = cursor.fetchall()

    connection.close()

    return result

def get_user_posts(_connection_pool,id):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)

    cursor.execute(get_user_posts_sql, (id,))
    result = cursor.fetchall()

    connection.close()

    return result

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
    

def get_post_comments(_connection_pool, id):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)

    cursor.execute(get_comments_sql, (id,))
    result = cursor.fetchall()

    connection.close()

    return result


def get_comment(_connection_pool, id):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)

    cursor.execute(get_comment_sql, (id,))
    result = cursor.fetchall()

    connection.close()

    return result


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
    
def get_feed(_connection_pool):
    connection = _connection_pool.get_connection()
    cursor = connection.cursor(buffered=True)

    cursor.execute(feed_sql)
    result = cursor.fetchall()

    connection.close()

    return result

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