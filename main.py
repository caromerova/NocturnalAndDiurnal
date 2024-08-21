from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.vehicles import vehicles_router
from routers.user import user_router

app = FastAPI()
app.title = "Nocturnal And Diurnal"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)

app.include_router(vehicles_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)


vehicles = [
    {
        "id": 1,
        "plate": "XLW70G",
        "overview": "vehiculo de carga de color blanco y capacidad para 60 toneladas",
        "model": 2025,
        "type": "furgon",
        "category": "Carga"
    },
    {
        "id": 2,
        "plate": "XLW70G",
        "overview": "vehiculo de carga de color blanco y capacidad para 60 toneladas",
        "model": "2025",
        "type": "furgon",
        "category": "Carga"
    }
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Welcome everybody to Nocturnal And Diurnal</h1>')


