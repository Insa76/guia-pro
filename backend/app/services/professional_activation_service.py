from datetime import datetime, timedelta, timezone
import hashlib
import os
import secrets

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.professional_auth import hash_password
from app.models.professional import Professional
from app.models.verification import Verification


ACTIVATION_TOKEN_EXPIRE_SECONDS = int(
    os.getenv("PROFESSIONAL_ACTIVATION_EXPIRE_SECONDS", "86400")
)


def _hash_activation_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_activation_token(
    db: Session,
    verification_id: int,
) -> tuple[Professional, str, datetime]:

    verification = db.get(Verification, verification_id)

    if verification is None:
        raise ValueError("Verification not found")

    professional = db.get(Professional, verification.professional_id)

    if professional is None:
        raise ValueError("Professional not found")

    if verification.status != "verified":
        raise ValueError(
            "The professional must be verified before account activation."
        )

    if not professional.identity_verified:
        raise ValueError(
            "The professional identity must be verified before activation."
        )

    if not professional.is_active:
        raise ValueError(
            "The professional must be active before account activation."
        )

    if professional.account_enabled:
        raise ValueError(
            "This professional account is already activated."
        )

    raw_token = secrets.token_urlsafe(32)
    token_hash = _hash_activation_token(raw_token)

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(seconds=ACTIVATION_TOKEN_EXPIRE_SECONDS)

    professional.activation_token_hash = token_hash
    professional.activation_token_created_at = now
    professional.activation_token_expires_at = expires_at

    db.commit()
    db.refresh(professional)

    return professional, raw_token, expires_at


def validate_activation_token(
    db: Session,
    token: str,
) -> Professional | None:

    token_hash = _hash_activation_token(token)

    statement = select(Professional).where(
        Professional.activation_token_hash == token_hash
    )

    professional = db.scalar(statement)

    if professional is None:
        return None

    if professional.account_enabled:
        return None

    if not professional.activation_token_expires_at:
        return None

    now = datetime.now(timezone.utc)

    if professional.activation_token_expires_at <= now:
        return None

    if not professional.identity_verified:
        return None

    if not professional.is_active:
        return None

    return professional


def activate_professional_account(
    db: Session,
    token: str,
    password: str,
) -> Professional:

    professional = validate_activation_token(db, token)

    if professional is None:
        raise ValueError(
            "Activation token is invalid or expired."
        )

    professional.password_hash = hash_password(password)
    professional.account_enabled = True

    # El token es de un solo uso.
    professional.activation_token_hash = None
    professional.activation_token_created_at = None
    professional.activation_token_expires_at = None

    db.commit()
    db.refresh(professional)

    return professional