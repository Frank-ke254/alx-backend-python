from typing import Any
from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsMessageOwner(BasePermission):
    def has_permission(self, request: Request, view: Any) -> bool:
        user = getattr(request, "user", None)
        return bool(user and getattr(user, "is_authenticated", False))

    def has_object_permission(self, request: Request, view: Any, obj: Any) -> bool:
        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            return False

        sender = getattr(obj, "sender", None)
        receiver = getattr(obj, "receiver", None)
        return user == sender or user == receiver


class IsConversationParticipant(BasePermission):
    def has_permission(self, request: Request, view: Any) -> bool:
        user = getattr(request, "user", None)
        return bool(user and getattr(user, "is_authenticated", False))

    def has_object_permission(self, request: Request, view: Any, obj: Any) -> bool:
        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            return False

        if hasattr(obj, "participants"):
            participants = getattr(obj, "participants")
            try:
                return user in participants.all()
            except Exception:
                return user in participants

        if hasattr(obj, "users"):
            users = getattr(obj, "users")
            try:
                return user in users.all()
            except Exception:
                return user in users

        if hasattr(obj, "user1") and hasattr(obj, "user2"):
            return user == getattr(obj, "user1") or user == getattr(obj, "user2")
        owner = getattr(obj, "owner", None)
        if owner is not None:
            return user == owner
        return False
