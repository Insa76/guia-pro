from fastapi import APIRouter, HTTPException, Request

from app.schemas.admin_auth import (
    AdminLoginRequest,
    AdminLoginResponse,
)

from app.core.admin_auth import (
    authenticate_admin,
    create_admin_token,
    ADMIN_TOKEN_EXPIRE_SECONDS,
)

from app.core.rate_limit import admin_login_limiter


router = APIRouter(
    prefix="/api/admin/auth",
    tags=["admin-auth"],
)


@router.post(
    "/login",
    response_model=AdminLoginResponse,
)
def admin_login(
    request: Request,
    data: AdminLoginRequest,
):
    client_ip = (
        request.client.host
        if request.client
        else "unknown"
    )

    if not admin_login_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail=(
                "Demasiados intentos de inicio de sesión. "
                "Intentá nuevamente más tarde."
            ),
        )

    try:
        authenticated = authenticate_admin(
            data.username,
            data.password,
        )

    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    if not authenticated:
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos.",
        )

    admin_login_limiter.reset(client_ip)

    token = create_admin_token()

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": ADMIN_TOKEN_EXPIRE_SECONDS,
    }