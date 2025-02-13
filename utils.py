import bcrypt


def hash_password(raw_password: str) -> str:
    assert raw_password, 'Password is required'
    raw_password = raw_password.encode('utf-8')
    return bcrypt.hashpw(raw_password, bcrypt.gensalt()).decode()


def match_password(raw_password: str, encoded_password: str) -> bool:
    assert raw_password, 'Password is required'
    assert encoded_password, 'Encoded password is required'
    raw_password = raw_password.encode('utf-8')
    encoded_password = encoded_password.encode('utf-8')
    return bcrypt.checkpw(raw_password, encoded_password)


class Response:
    def __init__(self, message: str, status_code: int = 200) -> None:
        self.message = message
        self.status_code = status_code
