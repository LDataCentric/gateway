import os
from typing import Union, List, Dict, Optional

import requests
import logging

from controller.notification.notification_data import __notification_data
from db import events
from exceptions import exceptions
from controller.user.manager import get_or_create_user
from db.business_objects import project, general
from db.business_objects.notification import get_duplicated, create
from db.business_objects.organization import get_organization_id
from db.enums import NotificationType
from db.models import Notification
from util import doc_ock

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_organization_update(
    project_id: str,
    message: str,
    is_global: bool = False,
    organization_id: Optional[str] = None,
) -> None:

    if not os.getenv("WS_NOTIFY_ENDPOINT"):
        print(
            "- WS_NOTIFY_ENDPOINT not set -- did you run the start script?", flush=True
        )
        return

    if is_global:
        message = f"GLOBAL:{message}"
    else:
        message = f"{project_id}:{message}"
    if not organization_id:
        project_item = project.get(project_id)
        organization_id = str(project_item.organization_id)

    req = requests.post(
        f"{os.getenv('WS_NOTIFY_ENDPOINT')}/notify",
        json={
            "organization": organization_id,
            "message": message,
        },
    )
    if req.status_code != 200:
        print("Could not send notification update", flush=True)


def create_notification(
    notification_type: NotificationType, user_id: str, project_id: str, *args
) -> Notification:
    # if value of enum is not unpacked do it here
    if not type(notification_type) == str:
        notification_type = notification_type.value

    if get_duplicated(project_id, notification_type, user_id):
        return None

    message = resolve_message(notification_type, list(args))
    level = get_notification_data(notification_type).get("level")
    new_notification = create(
        project_id, user_id, message, level, notification_type, with_commit=True
    )
    organization_id = get_organization_id(project_id, user_id)
    if organization_id:
        send_organization_update(
            project_id, f"notification_created:{user_id}", True, organization_id
        )
    user = get_or_create_user(user_id)
    doc_ock.post_event(user, events.AddNotification(Level=level, Message=message))
    return new_notification


def resolve_message(notification_type: str, args: Optional[List[str]] = None) -> str:
    if args is None:
        args = []

    notification_data = __notification_data.get(notification_type)
    if not notification_data:
        raise exceptions.NotificationTypeException(
            "No according message template was found."
        )
    message_template = notification_data.get("message_template")
    for arg in args:
        message_template = message_template.replace("@@arg@@", str(arg), 1)

    if "@@arg@@" in message_template:
        raise exceptions.NotificationTypeException(
            "Delivered arguments did not fit message."
        )
    else:
        return message_template


def get_notification_data(notification_type: str) -> Dict[str, str]:
    notification_data = __notification_data.get(notification_type)
    if not notification_data:
        raise exceptions.NotificationTypeException(
            f"No data for type {notification_type} found."
        )
    return notification_data
