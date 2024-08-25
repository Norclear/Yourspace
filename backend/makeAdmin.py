import mysql.connector

# This is a separate python script tat can be run separately to make certain user's admin.
# There is no gui, takes all required details as command line arguments.

# database details
# They have been hard coded but this file is not public and cannot be accessed by malicious users.. i think?
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

# This will take the command line arguments.
if __name__ == "__main__":
    import sys

    username = sys.argv[1]
    permission = int(sys.argv[2])
    update_permission(username, permission)