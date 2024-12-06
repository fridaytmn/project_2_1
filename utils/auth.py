import json
import jwt
from dash import callback_context

from utils.auther_service import AutherService
from utils.user import User, ROLE
from utils.page import Page


DATETIME_ONE_YEAR = 365 * 24 * 60 * 60 * 1000

ROLE_BY_JOB_TITLE = {
    "admin": ROLE.ADMIN,
    "user": ROLE.USER,
}

auther_services = AutherService()


class AuthManager:
    @classmethod
    def identify(cls, cookie) -> User:
        if cookie:
            token = json.loads(cookie).get("token", "")
            try:
                jwt_payload = jwt.decode(token, options={"verify_signature": False})
                return User(
                    username=jwt_payload.get("username", ""),
                    token=token,
                    roles=get_user_role(jwt_payload),
                )
            except jwt.exceptions.DecodeError:
                pass
        return User(username="", roles={ROLE.GUEST}, token="")

    @classmethod
    def authenticate(cls, user: User) -> bool:
        if user.roles == {ROLE.GUEST}:
            return True
        return auther_services.check(user.token)

    @classmethod
    def authorize(cls, page: Page, user: User) -> bool:
        if page.get_allowed_users() and user.username not in page.get_allowed_users():
            return False
        if not page.get_allowed_roles() or not page.get_allowed_roles().isdisjoint(user.roles):
            return True
        return False

    @classmethod
    def get_token(cls, username: str, password: str) -> str:
        result = auther_services.get_identity(username=username, password=password)
        return result.token

    @classmethod
    def set_cookie(cls, cookie: str) -> None:
        callback_context.response.set_cookie("dash_cookie", cookie, max_age=DATETIME_ONE_YEAR)


def get_user_role(jwt_payload) -> set:
    user_roles = {group_name for group_name in []}  # noqa
    user_roles.add(ROLE.USER)
    return user_roles
