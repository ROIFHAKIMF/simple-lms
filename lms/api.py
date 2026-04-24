from ninja import NinjaAPI
from ninja.errors import HttpError, ValidationError
from django.http import HttpRequest

from .routers.auth import router as auth_router
from .routers.courses import router as courses_router
from .routers.enrollments import router as enrollments_router

api = NinjaAPI(
    title="Simple LMS API",
    version="1.0.0",
    description=(
        "REST API for Simple LMS built with **Django Ninja**.\n\n"
        "## Authentication\n"
        "Use `POST /api/auth/login` to get a JWT access token, then pass it as:\n"
        "```\nAuthorization: Bearer <access_token>\n```"
    ),
    docs_url="/docs",
)

api.add_router("/auth", auth_router)
api.add_router("/courses", courses_router)
api.add_router("/enrollments", enrollments_router)


@api.exception_handler(HttpError)
def http_error_handler(request: HttpRequest, exc: HttpError):
    return api.create_response(request, {"detail": exc.message}, status=exc.status_code)


@api.exception_handler(ValidationError)
def validation_error_handler(request: HttpRequest, exc: ValidationError):
    return api.create_response(request, {"detail": exc.errors}, status=422)