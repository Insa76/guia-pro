# Guia Pro

MVP de la guía local de profesionales de Resistencia, Chaco.

## Base técnica
- FastAPI
- PostgreSQL 16
- SQLAlchemy
- Docker Compose
- Health check
- Test básico

## Ejecutar

```powershell
docker compose up --build
```

API: http://localhost:8000
Health: http://localhost:8000/api/health
Docs: http://localhost:8000/docs

## Detener

```powershell
docker compose down
```

## Próximo paso
Construir el modelo de datos de profesionales, categorías, zonas, verificaciones y valoraciones.
