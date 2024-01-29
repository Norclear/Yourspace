#creates the table for storing user and user data on initialisation of the server if the table does not yet exist
user_table = """CREATE TABLE IF NOT EXISTS Users (
id INT UNSIGNED AUTO_INCREMENT UNIQUE KEY,
username VARCHAR(14) NOT NULL UNIQUE KEY,
password VARCHAR(64) NOT NULL,
reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
permissions INT(3),
profile_picture VARCHAR(100), 
PRIMARY KEY (id),
FULLTEXT (username)
)ENGINE=InnoDB;"""

#creates the table for storing posts and post data on initialisation of the server if the table does not yet exist
post_table = """CREATE TABLE IF NOT EXISTS Posts (
post_id INT UNSIGNED AUTO_INCREMENT UNIQUE KEY,
title VARCHAR(25) NOT NULL,
description VARCHAR(500) NOT NULL,
attachment VARCHAR(100), 
post_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
owner_id INT UNSIGNED,
private BOOLEAN NOT NULL,
PRIMARY KEY (post_id),
FOREIGN KEY (owner_id) REFERENCES Users(id) ON DELETE CASCADE,
FULLTEXT (title,description)
)ENGINE=InnoDB;"""

#creates the table for storing comments and comment data on initialisation of the server if the table does not yet exist
comment_table = """CREATE TABLE IF NOT EXISTS comments (
comment_id INT UNSIGNED AUTO_INCREMENT UNIQUE KEY,
post_id INT UNSIGNED NOT NULL,
username VARCHAR (14) NOT NULL,
comment VARCHAR(500) NOT NULL,
date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (comment_id),
FOREIGN KEY (post_id) REFERENCES Posts(post_id) ON DELETE CASCADE,
FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
)ENGINE=InnoDB;"""

#creates a new user upon user registration
user_create_sql = """INSERT INTO Users (username,password,permissions,profile_picture) VALUES (%s,%s,%s,%s)"""

#returns a value if a specific username is in the database, if not it will return null
query_username_sql = """SELECT * FROM Users WHERE username = %s"""

#gets the hashed password of a specific user
query_password_sql = """SELECT password FROM Users WHERE username = %s"""

#returns the user id of a user with a given username
username_to_id_sql = """SELECT id FROM Users WHERE username = %s"""

#returns the username of a user with a given user id
id_to_username_sql = """SELECT username FROM Users WHERE id = %s"""

#queries the permission level of a specific user account given the user id
query_permissions_sql = """SELECT permissions FROM Users WHERE id = %s"""

#returns general account information given the username
query_account_sql = """SELECT reg_date, permissions, profile_picture
FROM Users 
WHERE username = %s"""

#generates a new post in the database
create_post_sql = """INSERT INTO Posts (title,description,attachment,owner_id,private) VALUES (%s,%s,%s,%s,%s)"""

#return a post using it's id
get_post_by_id_sql = """SELECT Posts.title, Posts.description, Posts.attachment, Posts.post_date, Posts.private, Users.username
FROM Posts
JOIN Users ON Posts.owner_id = Users.id
WHERE Posts.post_id = %s"""

#query the database to return a user's pfp (an svg stored as a string)
get_pfp_sql = """SELECT profile_picture FROM users WHERE username = (%s)"""

#
search_users_sql = """SELECT *, MATCH(username) AGAINST(%s IN NATURAL LANGUAGE MODE) as relevance FROM Users WHERE MATCH(username) AGAINST(%s IN NATURAL LANGUAGE MODE) OR username LIKE CONCAT('%', %s, '%') OR SOUNDEX(username) = SOUNDEX(%s)"""

search_posts_sql = """SELECT *, MATCH(title,description) AGAINST(%s IN NATURAL LANGUAGE MODE) as relevance FROM Posts WHERE MATCH(title,description) AGAINST(%s IN NATURAL LANGUAGE MODE) OR (title LIKE CONCAT('%', %s, '%') OR description LIKE CONCAT('%', %s, '%')) OR SOUNDEX(title) = SOUNDEX(%s) OR SOUNDEX(description) = SOUNDEX(%s)"""

get_user_posts_sql = """SELECT * FROM Posts WHERE owner_id = %s"""

delete_post_sql = """DELETE FROM Posts WHERE post_id = %s"""

edit_post_sql = """UPDATE Posts SET title = %s, description = %s WHERE post_id = %s"""

create_comment_sql = """INSERT INTO Comments (post_id,username,comment) VALUES (%s,%s,%s)"""

get_comments_sql = """SELECT * FROM Comments WHERE post_id = %s"""

get_comment_sql = """SELECT * FROM Comments WHERE comment_id = %s"""

delete_comment_sql = """DELETE FROM Comments WHERE comment_id = %s"""

feed_sql = """SELECT * FROM Posts WHERE private = 0 ORDER BY post_date DESC LIMIT 100"""

delete_user_sql = """DELETE FROM Users WHERE username = %s"""