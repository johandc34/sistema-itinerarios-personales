# Sistema de Itinerarios Personales

Proyecto académico orientado al desarrollo de un sistema distribuido para la consulta de aeropuertos y la gestión de itinerarios personales.

## Arquitectura

El sistema será desarrollado utilizando una arquitectura basada en microservicios y principios de arquitectura hexagonal.

## Componentes principales

- Airport Service
- Itinerary Service
- Frontend
- Sistema de notificaciones
- Infraestructura compartida

## Airport Service

Microservicio encargado de consultar información de aeropuertos y exponerla mediante una API REST.

### Tecnologías iniciales

- Python
- FastAPI
- Pydantic
- HTTPX
- Pytest
- Pytest Coverage
- Uvicorn

## Estado actual

Actualmente se encuentra en desarrollo el Airport Service.

Endpoints iniciales disponibles:

- `GET /`
- `GET /health`
- Documentación Swagger: `/docs`