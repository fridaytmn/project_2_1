from dataclasses import dataclass
from user_log_pass import USERS

class AutherError(Exception):
    """Exception raised for errors in Auth.

    Attributes:
        title -- error title
        reason -- human-readable error description
        description -- original error description
    """

    def __init__(self, title: str, reason: str = "", description: str = ""):
        self.title = title
        self.reason = reason
        self.description = description
        super().__init__(self.description)

    def __str__(self) -> str:
        return f"{self.title}: {self.reason}"


@dataclass
class Identity:
    username: str
    roles: set


class AutherService:

    @classmethod
    def get_identity(cls, username: str, password: str) -> Identity:
        if username not in USERS or USERS[username]["password"] != password:
            raise AutherError("Ошибка входа", "Неправильный логин или пароль")
        role = USERS[username]["ROLE"]
        return Identity(username=username, roles={role})

    @classmethod
    def check(cls, user) -> bool:
        if user.username in USERS:
            if user.roles[0] == USERS[user.username]["ROLE"]:
                return True
        print(user)  # noqa
        return False
