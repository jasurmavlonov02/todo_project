import psycopg2

from utils import hash_password

db_info = {
    'host': 'localhost',
    'user': 'postgres',
    'password': '1',
    'database': 'n60_projects',
    'port': 5432
}

conn = psycopg2.connect(**db_info)
cur = conn.cursor()


def commit(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        conn.commit()
        return result

    return wrapper


def create_user_table():
    query = """CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        username varchar(255) not null unique,
        password text ,
        role varchar(10) default 'user',
        login_try_count int default 0,
        created_at timestamptz default current_timestamp
    );"""
    cur.execute(query)


def create_todo_table():
    query = """CREATE TABLE IF NOT EXISTS todos(
        id SERIAL PRIMARY KEY,
        title varchar(100) not null,
        description text,
        todo_type varchar(20) default 'low',
        user_id int references users(id) on delete cascade,
        created_at timestamptz default current_timestamp
    );"""
    cur.execute(query)


@commit
def insert_user_admin():
    insert_query = '''insert into users(username,password,role)
    values (%s,%s,%s);'''
    cur.execute(insert_query, ('admin', hash_password('123'), 'admin'))


@commit
def init():
    create_user_table()
    create_todo_table()

# init()

# insert_user_admin()