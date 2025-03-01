from typing import Union, Any
from requests import Response
import os
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_userid_from_mail(user_mail: str) -> str:
    for identity in requests.get(f"{os.getenv('KRATOS_ADMIN_URL')}/identities").json():
        if identity["traits"]["email"] == user_mail:
            return identity["id"]
    return None


def resolve_user_mail_by_id(user_id: str) -> str:
    res: Response = requests.get(f"{os.getenv('KRATOS_ADMIN_URL')}/identities/{user_id}")
    data: Any = res.json()
    if res.status_code == 200 and data["traits"]:
        return data["traits"]["email"]
    return None


def resolve_user_name_by_id(user_id: str) -> str:
    res: Response = requests.get(f"{os.getenv('KRATOS_ADMIN_URL')}/identities/{user_id}")
    data: Any = res.json()
    if res.status_code == 200 and data["traits"]:
        return data["traits"]["name"]
    return None
