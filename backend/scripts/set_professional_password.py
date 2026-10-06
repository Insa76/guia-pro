import argparse
from pathlib import Path
import sys

from sqlalchemy import select

# Permite importar "app" al ejecutar el script directamente
# desde /app/scripts dentro del contenedor.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.professional_auth import hash_password
from app.db.session import SessionLocal
from app.models.professional import Professional


def main():

    parser = argparse.ArgumentParser(
        description="Configura la contraseña de un profesional."
    )

    parser.add_argument(
        "--phone",
        required=True,
        help="Teléfono del profesional.",
    )

    parser.add_argument(
        "--password",
        required=True,
        help="Nueva contraseña.",
    )

    args = parser.parse_args()

    phone = args.phone.strip()

    if len(args.password) < 8:
        print(
            "ERROR: la contraseña debe tener al menos 8 caracteres."
        )
        sys.exit(1)

    db = SessionLocal()

    try:

        professional = db.scalar(
            select(Professional).where(
                Professional.phone == phone
            )
        )

        if professional is None:
            print(
                f"ERROR: no existe un profesional con teléfono {phone}."
            )
            sys.exit(1)

        professional.password_hash = hash_password(
            args.password
        )

        professional.account_enabled = True

        db.commit()

        print(
            f"Cuenta habilitada correctamente para "
            f"{professional.first_name} "
            f"{professional.last_name}."
        )

        print(
            f"Professional ID: {professional.id}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()