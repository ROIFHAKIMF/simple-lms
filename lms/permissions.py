from functools import wraps
from ninja.security import HttpBearer
from ninja.errors import HttpError
from django.http import HttpRequest
from .auth_utils import get_user_from_token


class JWTAuth(HttpBearer):
    """Extract and validate JWT from Authorization: Bearer <token> header."""

    def authenticate(self, request: HttpRequest, token: str):
        try:
            user = get_user_from_token(token)
            request.user = user
            return user
        except ValueError as e:
            raise HttpError(401, str(e))


jwt_auth = JWTAuth()


# ─────────────────────────────────────────
# Role helpers
# ─────────────────────────────────────────

def _get_role(request: HttpRequest) -> str:
    """Return the role of the authenticated user, or empty string."""
    user = getattr(request, "user", None)
    if user is None or not user.is_authenticated:
        return ""
    profile = getattr(user, "profile", None)
    return profile.role if profile else ""


def require_role(*roles):
    """
    Decorator factory for Django Ninja endpoint functions.
    Usage:
        @router.get("/...", auth=jwt_auth)
        @require_role("instructor", "admin")
        def my_view(request, ...):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            role = _get_role(request)
            if role not in roles:
                raise HttpError(403, f"Required role: {', '.join(roles)}")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def is_instructor(func):
    return require_role("instructor", "admin")(func)


def is_admin(func):
    return require_role("admin")(func)


def is_student(func):
    return require_role("student", "admin")(func)