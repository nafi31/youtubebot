import psycopg
conn = psycopg.connect(
    "host=abul.db.elephantsql.com  dbname=ovooekmc  user=ovooekmc password=Q0JeWjZOXDqQ1JHsvl3xfjIkZcgRWNpl ")

cur = conn.cursor()
def create_table():
    cur.execute('''
    CREATE TABLE  userdata(
    id serial PRIMARY KEY,
    user_id integer)
 ''')



def getusers(user_ids):
    cur.execute("select * from userdata where user_id=(%s) ",(user_ids,))
    return cur.fetchall()

def add_user(user_ids):
    if not getusers(user_ids):

        cur.execute("INSERT INTO userdata (user_id) values(%s)" , (user_ids,))
        conn.commit()
        print("success")
        
    else:
        print("no si")
