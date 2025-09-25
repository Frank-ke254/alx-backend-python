from typing import Optional

def get_token_from_request(request) -> Optional[str]:
    if request is None:
        return None

    auth = ""
    meta = getattr(request, "META", None)
    if meta:
        auth = meta.get("HTTP_AUTHORIZATION", "") or meta.get("Authorization", "")

    if not auth:
        headers = getattr(request, "headers", None)
        if headers:
            auth = headers.get("Authorization", "")

    if not auth:
        return None

    parts = auth.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None


def is_request_authenticated(request) -> bool:
    user = getattr(request, "user", None)
    return bool(user and getattr(user, "is_authenticated", False))

def verify_jwt_token(token: str) -> bool:
    if not token:
        return False
    try:
        from rest_framework_simplejwt.tokens import UntypedToken
    except Exception:
        return False

    try:
        UntypedToken(token)
        return True
    except Exception:
        return False


class AuthHelper:
    """Small helper combining token extraction and verification."""

    @staticmethod
    def is_authenticated_request(request) -> bool:
        """Return True if request.user is authenticated or contains a valid JWT."""
        if is_request_authenticated(request):
            return True
        token = get_token_from_request(request)
        return verify_jwt_token(token)
