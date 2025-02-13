from migrations.db import cur, commit
from sessions import Session
from utils import Response, match_password
from models import User

session = Session()


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


response = login('admin', '1234')
print(response.message)
