import base64
import hashlib
import hmac
import json
import os
import time

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
ADMIN_TOKEN_SECRET = os.getenv("ADMIN_TOKEN_SECRET")

ADMIN_TOKEN_EXPIRE_SECONDS = int(
    os.getenv(
        "ADMIN_TOKEN_EXPIRE_SECONDS",
        "28800",
    )
)


bearer_scheme = HTTPBearer(
    auto_error=False
)


def _validate_configuration():

    if not ADMIN_USERNAME:
        raise RuntimeError(
            "ADMIN_USERNAME no está configurado."
        )

    if not ADMIN_PASSWORD:
        raise RuntimeError(
            "ADMIN_PASSWORD no está configurado."
        )

    if not ADMIN_TOKEN_SECRET:
        raise RuntimeError(
            "ADMIN_TOKEN_SECRET no está configurado."
        )


def authenticate_admin(
    username: str,
    password: str,
) -> bool:

    _validate_configuration()

    username_valid = hmac.compare_digest(
        username,
        ADMIN_USERNAME,
    )

    password_valid = hmac.compare_digest(
        password,
        ADMIN_PASSWORD,
    )

    return (
        username_valid
        and password_valid
    )


def create_admin_token() -> str:

    _validate_configuration()

    payload = {
        "sub": ADMIN_USERNAME,
        "exp": int(
            time.time()
            + ADMIN_TOKEN_EXPIRE_SECONDS
        ),
    }

    payload_json = json.dumps(
        payload,
        separators=(",", ":"),
    ).encode("utf-8")

    payload_encoded = (
        base64.urlsafe_b64encode(
            payload_json
        )
        .decode("utf-8")
        .rstrip("=")
    )

    signature = hmac.new(
        ADMIN_TOKEN_SECRET.encode("utf-8"),
        payload_encoded.encode("utf-8"),
        hashlib.sha256,
    ).digest()

    signature_encoded = (
        base64.urlsafe_b64encode(
            signature
        )
        .decode("utf-8")
        .rstrip("=")
    )

    return (
        f"{payload_encoded}.{signature_encoded}"
    )


def verify_admin_token(
    token: str,
) -> bool:

    _validate_configuration()

    try:

        payload_encoded, signature_encoded = (
            token.split(".", 1)
        )

        expected_signature = hmac.new(
            ADMIN_TOKEN_SECRET.encode("utf-8"),
            payload_encoded.encode("utf-8"),
            hashlib.sha256,
        ).digest()

        provided_signature = (
            base64.urlsafe_b64decode(
                signature_encoded + "=="
            )
        )

        if not hmac.compare_digest(
            provided_signature,
            expected_signature,
        ):
            return False

        payload = json.loads(
            base64.urlsafe_b64decode(
                payload_encoded + "=="
            )
        )

        expiration = int(
            payload.get("exp", 0)
        )

        if expiration <= int(time.time()):
            return False

        if payload.get("sub") != ADMIN_USERNAME:
            return False

        return True

    except (
        ValueError,
        TypeError,
        KeyError,
        json.JSONDecodeError,
    ):
        return False


def require_admin(
    credentials: HTTPAuthorizationCredentials | None =
        Depends(bearer_scheme),
):
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Autenticación administrativa requerida.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="Esquema de autenticación inválido.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    if not verify_admin_token(
        credentials.credentials
    ):
        raise HTTPException(
            status_code=401,
            detail="Sesión administrativa inválida o vencida.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    return True