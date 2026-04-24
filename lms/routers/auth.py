from ninja import Router
from ninja.errors import HttpError
from django.contrib.auth.models import User
from django.http import HttpRequest

from ..models import UserProfile
from ..auth_utils import (
    hash_password, verify_password,
    create_access_token, create_refresh_token,
    decode_token, get_user_from_token,
)
from ..permissions import jwt_auth
from ..schemas import (
    RegisterIn, LoginIn, RefreshIn,
    TokenOut, AccessTokenOut,
    ProfileOut, ProfileUpdateIn, MessageOut,
)

router = Router(tags=["Auth"])


def _profile_out(user: User) -> ProfileOut:
    role = getattr(user, "profile", None)
    return ProfileOut(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=role.role if role else "student",
    )


@router.post("/register", response=ProfileOut, summary="Register new user")
def register(request: HttpRequest, data: RegisterIn):
    """Register a new user with role (admin | instructor | student)."""
    if User.objects.filter(username=data.username).exists():
        raise HttpError(400, "Username already taken")
    if User.objects.filter(email=data.email).exists():
        raise HttpError(400, "Email already registered")
    if data.role not in ("admin", "instructor", "student"):
        raise HttpError(400, "Role must be admin, instructor, or student")

    user = User.objects.create_user(
        username=data.username,
        email=data.email,
        password=data.password,
    )
    UserProfile.objects.create(user=user, role=data.role)
    return _profile_out(user)


@router.post("/login", response=TokenOut, summary="Login and receive JWT tokens")
def login(request: HttpRequest, data: LoginIn):
    """Authenticate and receive access + refresh tokens."""
    try:
        user = User.objects.select_related("profile").get(username=data.username)
    except User.DoesNotExist:
        raise HttpError(401, "Invalid credentials")

    if not user.check_password(data.password):
        raise HttpError(401, "Invalid credentials")

    return TokenOut(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@router.post("/refresh", response=AccessTokenOut, summary="Refresh access token")
def refresh(request: HttpRequest, data: RefreshIn):
    """Use a refresh token to get a new access token."""
    try:
        payload = decode_token(data.refresh_token)
    except ValueError as e:
        raise HttpError(401, str(e))

    if payload.get("type") != "refresh":
        raise HttpError(401, "Not a refresh token")

    try:
        user = User.objects.get(pk=int(payload["sub"]))
    except User.DoesNotExist:
        raise HttpError(401, "User not found")

    return AccessTokenOut(access_token=create_access_token(user.id))


@router.get("/me", response=ProfileOut, auth=jwt_auth, summary="Get current user profile")
def me(request: HttpRequest):
    """Return the authenticated user's profile."""
    return _profile_out(request.user)


@router.put("/me", response=ProfileOut, auth=jwt_auth, summary="Update current user profile")
def update_me(request: HttpRequest, data: ProfileUpdateIn):
    """Update first_name, last_name, or email for the authenticated user."""
    user = request.user
    if data.first_name is not None:
        user.first_name = data.first_name
    if data.last_name is not None:
        user.last_name = data.last_name
    if data.email is not None:
        if User.objects.exclude(pk=user.pk).filter(email=data.email).exists():
            raise HttpError(400, "Email already in use")
        user.email = data.email
    user.save()
    return _profile_out(user)