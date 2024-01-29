import mysql.connector

# database details
database_hostname = "localhost"
database_port = "3306"
database_password = "local_Development747"
database_name = "yourspace"
database_username = "root"

def update_permission(username, permission):
    # Connect to the database
    connection = mysql.connector.connect(
        host=database_hostname,
        port=database_port,
        user=database_username,
        password=database_password,
        database=database_name
    )

    # Create a cursor to execute queries
    cursor = connection.cursor()

    # Update the user's permissions
    query = "UPDATE Users SET permissions = %s WHERE username = %s"
    cursor.execute(query, (permission, username))

    # Commit the changes
    connection.commit()

    # Close the connection
    connection.close()

if __name__ == "__main__":
    import sys

    username = sys.argv[1]
    permission = int(sys.argv[2])
    update_permission(username, permission)