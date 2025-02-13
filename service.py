from migrations.db import cur, commit

from sessions import Session
from utils import Response, match_password, hash_password
from models import User, Todo

session = Session()


def login_required(func):
    def wrapper(*args, **kwargs):
        if not session.session:
            raise Exception('User not authenticated')
        result = func(*args, **kwargs)
        return result

    return wrapper


@commit
def login(username: str, password: str) -> Response:
    user: User | None = session.check_session()
    if user is not None:
        return Response(message='You already logged in', status_code=401)
    get_user_by_username_query = '''select * from users where username = %s;'''
    cur.execute(get_user_by_username_query, (username,))
    user_data = cur.fetchone()
    if user_data is None:
        return Response(message='Invalid username or password', status_code=401)
    user = User.from_tuple(user_data)
    if not match_password(password, user.password):
        update_user_query = '''update users set login_try_count = login_try_count + 1 where username = %s;'''
        cur.execute(update_user_query, (username,))
        return Response('Invalid username or password', status_code=401)
    session.add_session(user)
    return Response('Login successful', status_code=200)


@commit
def register(username, password):
    get_user_by_username = '''select * from users where username = %s;'''
    cur.execute(get_user_by_username, (username,))
    user_data = cur.fetchone()
    if user_data is not None:
        return Response(message=f'This {username} already exists', status_code=400)

    user = User(username=username, password=password)
    user.save()
    return Response('User successfully created', status_code=201)


def logout():
    if session.session:
        session.session = None
        return Response(message='Logged out', status_code=200)
    return Response(message='You must login first', status_code=404)


@commit
@login_required
def todo_add(title: str):
    user: User = session.check_session()
    if user.role != 'admin':
        return Response(message='Adding todo must be an admin', status_code=401)
    todo = Todo(title=title, user_id=user.id)
    todo.save()
    return Response(message='Todo added', status_code=201)


def set_admin():
    pass
