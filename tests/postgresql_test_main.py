import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="kunal_test",
        user="postgres",
        password="1234"
    )
    # create a cursor
    cur = conn.cursor()
    
    # execute a statement
    print('PostgreSQL database version:')
    cur.execute('SELECT version()')

    # display the PostgreSQL database server version
    db_version = cur.fetchone()
    print(db_version)
    
    cur.execute('SELECT * from iwaaa')
    result = cur.fetchall()
    print(result)

    # close the communication with the PostgreSQL
    cur.close()
except:
    print("ERROR!")