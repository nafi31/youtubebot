import psycopg


def create_table():
    conn = psycopg.connect(
        "host=abul.db.elephantsql.com  dbname=ovooekmc  user=ovooekmc password=Q0JeWjZOXDqQ1JHsvl3xfjIkZcgRWNpl ")

    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE  userdata(
    id serial PRIMARY KEY,
    user_id bigint)
    ''')
    conn.commit()
    conn.close()
    print('done')


def getallusers():
    conn = psycopg.connect(
        "host=abul.db.elephantsql.com  dbname=ovooekmc  user=ovooekmc password=Q0JeWjZOXDqQ1JHsvl3xfjIkZcgRWNpl ")

    cur = conn.cursor()
    cur.execute("SELECT * FROM userdata")
    conn.commit()
    res = cur.fetchall()

    conn.close()
    return res


def getusers(user_ids):
    conn = psycopg.connect(
        "host=abul.db.elephantsql.com  dbname=ovooekmc  user=ovooekmc password=Q0JeWjZOXDqQ1JHsvl3xfjIkZcgRWNpl ")

    cur = conn.cursor()
    cur.execute("select * from userdata where user_id = %s", (user_ids,))
    conn.commit()
    res = cur.fetchall()

    conn.close()
    return res


def add_user(user_ids):
    conn = psycopg.connect(
        "host=abul.db.elephantsql.com  dbname=ovooekmc  user=ovooekmc password=Q0JeWjZOXDqQ1JHsvl3xfjIkZcgRWNpl ")

    cur = conn.cursor()
    if not getusers(user_ids):

        cur.execute("INSERT INTO userdata (user_id) values(%s)", (user_ids,))
        conn.commit()
        conn.close()

    else:
        conn.close()

        #print("no si")
create_table()
