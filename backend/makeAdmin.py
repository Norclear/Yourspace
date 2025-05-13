import mysql.connector
import os

# This is a separate python script tat can be run separately to convert generic user accounts to admin accounts.
# There is no gui, takes all required details as command line arguments.

# database details
# Get database details from environment variables
database_hostname = os.getenv("DB_HOSTNAME")
database_port = os.getenv("DB_PORT", "3306") # 3306 default port if the env var is not set
database_username = os.getenv("DB_USERNAME")
database_password = os.getenv("DB_PASSWORD")
database_name = os.getenv("DB_NAME")

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
