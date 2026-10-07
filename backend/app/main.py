from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.health import router as health_router
from app.api.professionals import router as professionals_router
from app.api.categories import router as categories_router
from app.api.professional_categories import (
    router as professional_categories_router,
)
from app.api.search import router as search_router
from app.api.locations import router as locations_router
from app.api.professional_locations import (
    router as professional_locations_router,
)
from app.api.jobs import router as jobs_router
from app.api.reviews import router as reviews_router
from app.api.reputation import router as reputation_router
from app.api.verifications import router as verifications_router
from app.api.verification_admin import router as verification_admin_router
from app.api.public_search import router as public_search_router
from app.api.public_profile import router as public_profile_router
from app.api import public_registration
from app.api.admin_auth import router as admin_auth_router
from app.api.professional_auth import router as professional_auth_router
from app.api.professional_activation import (
    router as professional_activation_router,
)
from app.api.professional_profile import (
    router as professional_profile_router,
)


app = FastAPI(
    title="Guia Pro API",
    version="0.1.0",
    description="API de Guia Pro",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://guia-pro-frontend.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# API
# ============================================================

app.include_router(health_router)

app.include_router(professionals_router)

app.include_router(categories_router)

app.include_router(
    professional_categories_router
)

app.include_router(search_router)

app.include_router(locations_router)

app.include_router(
    professional_locations_router
)

app.include_router(jobs_router)

app.include_router(reviews_router)

app.include_router(reputation_router)

app.include_router(verifications_router)

app.include_router(
    verification_admin_router
)

app.include_router(
    public_search_router
)

app.include_router(
    public_profile_router
)

app.include_router(
    public_registration.router
)

app.include_router(
    admin_auth_router
)

app.include_router(
    professional_auth_router
)

app.include_router(
    professional_activation_router
)

app.include_router(
    professional_profile_router
)


# ============================================================
# FRONTEND
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

FRONTEND_DIR = BASE_DIR / "frontend"


app.mount(
    "/",
    StaticFiles(
        directory=FRONTEND_DIR,
        html=True,
    ),
    name="frontend",
)