import psycopg


def create_table():
    conn = psycopg.connect(
        CREDENTIALS GO HERE)

    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE  userdata2(
    id serial PRIMARY KEY,
    user_id bigint)
    ''')
    conn.commit()
    conn.close()
    print('done')


def getallusers():
    conn = psycopg.connect(CREDENTIALS GO HERE)

    cur = conn.cursor()
    cur.execute("SELECT * FROM userdata2")
    conn.commit()
    res = cur.fetchall()

    conn.close()
    return res


def getusers(user_ids):
    conn = psycopg.connect(
        CREDENTIALS GO HERE)

    cur = conn.cursor()
    cur.execute("select * from userdata2 where user_id = %s", (user_ids,))
    conn.commit()
    res = cur.fetchall()

    conn.close()
    return res


def add_user(user_ids):
    conn = psycopg.connect(
        CREDENTIALS GO HERE)

    cur = conn.cursor()
    if not getusers(user_ids):

        cur.execute("INSERT INTO userdata2 (user_id) values(%s)", (user_ids,))
        conn.commit()
        conn.close()

    else:
        conn.close()

        #print("no si")
