from fastapi import FastAPI

app = FastAPI(
    title="Airport Service",
    description="Microservicio encargado de consultar y gestionar información de aeropuertos.",
    version="1.0.0"
)


@app.get("/")
def inicio():
    return {
        "message": "Airport Service funcionando correctamente"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "airport-service"
    }