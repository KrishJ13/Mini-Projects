
"""
The naive approach when implementing a database is to establish a new connection to the database for every request.
Instead, we establish a 'pool' of connections, that each request borrows and returns from. 
Therefore, the lifecycle of a request is:
    1. Borrow connection from pool
    2. Create temporary cursor from connection
    3. Use cursor to execute SQL
    4. Close temporary cursor
    5. Return reusable connection to pool
"""

import os
from psycopg2 import pool
from contextlib import contextmanager

# DATABASE_URL is going to be injected to the postgres container as an environment variable
database_url = os.environ["DATABASE_URL"]

# Set up the Threaded connection pool (Handle mutliple threads competing for a request)
connection_pool = pool.ThreadedConnectionPool(minconn=1, maxconn=10, dsn=database_url)


# Define our contextmanager function, to ensure that if SQL message fails, the connection is safely returned to the pool
@contextmanager
def get_cursor(commit: bool = False):
    # Get a connection from the connection pool
    connection = connection_pool.getconn()
    # Get the cursor object from the returned connection and yield it back up the call
    cursor = connection.cursor()

    # No matter what, we need to put these objects back
    try:
        # Yield the cursor object so we can write SQL commands through it
        yield cursor
        # If it is a write command, we need to commit
        if commit:
            connection.commit()
    except:
        # If something goes wrong, raise an error and rollback the connection
        connection.rollback()
        raise
    finally:
        # Close the cursor object, but not the connection -> We put this back
        cursor.close()
        connection_pool.putconn(conn=connection)

    
