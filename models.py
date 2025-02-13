from datetime import datetime
from enum import Enum
from migrations.db import cur
from utils import hash_password


class UserRole(Enum):
    USER = 'user'
    ADMIN = 'admin'


class TodoType(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


class User:
    def __init__(self,
                 username: str,
                 password: str,
                 user_id: int | None = None,
                 role: UserRole | None = None,
                 login_try_count: int | None = None,
                 created_at: datetime | None = None
                 ):
        self.username = username
        self.password = password
        self.id = user_id
        self.role = role or UserRole.USER.value
        self.login_try_count = login_try_count or 0
        self.created_at = created_at or datetime.now()

    @staticmethod
    def from_tuple(args: tuple):
        return User(
            user_id=args[0],
            username=args[1],
            password=args[2],
            role=args[3],
            login_try_count=args[4],
            created_at=args[5]
        )

    def save(self):
        create_user_query = '''insert into users(username,password)
        values (%s,%s);'''
        cur.execute(create_user_query, (self.username, hash_password(self.password)))


class Todo:
    def __init__(self,
                 title: str,
                 user_id: int,
                 todo_id: int | None = None,
                 description: str | None = None,
                 todo_type: TodoType | None = None,
                 created_at: datetime | None = None,
                 ):
        self.title = title
        self.user_id = user_id
        self.id = todo_id
        self.description = description
        self.todo_type = todo_type or TodoType.LOW.value
        self.created_at = created_at or datetime.now()

    def save(self):
        create_todo_query = '''insert into todos(title,user_id)
        values (%s,%s);'''
        cur.execute(create_todo_query, (self.title, self.user_id))
