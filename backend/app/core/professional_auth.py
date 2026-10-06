import base64
import binascii
import hashlib
import hmac
import json
import os
import secrets
import time

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


PROFESSIONAL_TOKEN_SECRET = os.getenv(
    "PROFESSIONAL_TOKEN_SECRET"
)

PROFESSIONAL_TOKEN_EXPIRE_SECONDS = int(
    os.getenv(
        "PROFESSIONAL_TOKEN_EXPIRE_SECONDS",
        "28800",
    )
)

bearer_scheme = HTTPBearer(auto_error=False)


def _validate_configuration():
    if not PROFESSIONAL_TOKEN_SECRET:
        raise RuntimeError(
            "PROFESSIONAL_TOKEN_SECRET no está configurado."
        )


def hash_password(password: str) -> str:
    """
    Hash de contraseña usando PBKDF2-HMAC-SHA256.

    No almacenamos nunca la contraseña original.
    """

    if not password:
        raise ValueError(
            "La contraseña no puede estar vacía."
        )

    salt = secrets.token_bytes(16)

    iterations = 310_000

    derived_key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
    )

    salt_encoded = base64.urlsafe_b64encode(
        salt
    ).decode("utf-8").rstrip("=")

    hash_encoded = base64.urlsafe_b64encode(
        derived_key
    ).decode("utf-8").rstrip("=")

    return (
        f"pbkdf2_sha256${iterations}"
        f"${salt_encoded}"
        f"${hash_encoded}"
    )


def verify_password(
    password: str,
    password_hash: str,
) -> bool:

    try:
        algorithm, iterations, salt_encoded, hash_encoded = (
            password_hash.split("$", 3)
        )

        if algorithm != "pbkdf2_sha256":
            return False

        iterations = int(iterations)

        salt = base64.urlsafe_b64decode(
            salt_encoded + "=="
        )

        expected_hash = base64.urlsafe_b64decode(
            hash_encoded + "=="
        )

        calculated_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            iterations,
        )

        return hmac.compare_digest(
            calculated_hash,
            expected_hash,
        )

    except (
        ValueError,
        TypeError,
        binascii.Error,
    ):
        return False


def create_professional_token(
    professional_id: int,
) -> str:

    _validate_configuration()

    payload = {
        "sub": str(professional_id),
        "type": "professional",
        "exp": int(
            time.time()
            + PROFESSIONAL_TOKEN_EXPIRE_SECONDS
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
        PROFESSIONAL_TOKEN_SECRET.encode("utf-8"),
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
        f"{payload_encoded}."
        f"{signature_encoded}"
    )


def verify_professional_token(
    token: str,
) -> int | None:

    _validate_configuration()

    try:
        payload_encoded, signature_encoded = (
            token.split(".", 1)
        )

        expected_signature = hmac.new(
            PROFESSIONAL_TOKEN_SECRET.encode("utf-8"),
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
            return None

        payload = json.loads(
            base64.urlsafe_b64decode(
                payload_encoded + "=="
            )
        )

        expiration = int(
            payload.get("exp", 0)
        )

        if expiration <= int(time.time()):
            return None

        if payload.get("type") != "professional":
            return None

        professional_id = int(
            payload.get("sub")
        )

        return professional_id

    except (
        ValueError,
        TypeError,
        KeyError,
        json.JSONDecodeError,
        binascii.Error,
    ):
        return None


def require_professional(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
) -> int:

    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Autenticación de profesional requerida.",
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

    professional_id = verify_professional_token(
        credentials.credentials
    )

    if professional_id is None:
        raise HTTPException(
            status_code=401,
            detail="Sesión de profesional inválida o vencida.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    return professional_id