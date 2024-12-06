from dataclasses import dataclass, field
from enum import Enum


@dataclass
class User:
    username: str = ""
    token: str = ""
    roles: set = field(default_factory=set)


class ROLE(Enum):
    GUEST = "Guest"
    USER = "User"
    ADMIN = "Admin"
