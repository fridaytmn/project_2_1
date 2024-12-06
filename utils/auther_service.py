from dataclasses import dataclass

USERS = {
    "shvets_vv": {
        "password": "NSsQ3DGm",
        "ROLE": "ROLE.ADMIN",
        "token": "IJndin1idun2iuendi2endo",
        "refresh_token": "1111",
    }
}


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
    token: str = ""
    refresh_token: str = ""


class AutherService:

    @classmethod
    def get_identity(cls, username: str, password: str) -> Identity:
        payload = {"username": username, "password": password}

        res = validate_user(payload)
        print(res)  # noqa

        if res == 400:
            raise AutherError("Ошибка входа", "Не все поля заполнены")
        if res == 500:
            raise AutherError("Ошибка входа", "Неправильный логин или пароль")
        return Identity(res["token"], res["refresh_token"])

    @classmethod
    def check(cls, token) -> bool:
        print(token)  # noqa
        return True


def validate_user(payload: dict):

    if payload["password"] is None or payload["username"] is None:
        return 400
    if not payload["password"] == USERS.get(payload["username"], {"password": ""})["password"]:
        return 500
    return USERS.get(payload["username"])
