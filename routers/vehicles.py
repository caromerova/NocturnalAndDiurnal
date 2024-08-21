from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.vehicles import Vehicles as VehiclesModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.vehicles import VehiclesService

vehicles_router = APIRouter()


class Vehicles(BaseModel):
    id: Optional[int] = Field(default=1)
    plate: str = Field(default="placa", min_length=5, max_length=15)  #validacion ....
    overview: str = Field(default="describelo", min_length=10, max_length=50) 
    model: int = Field(default=2024, le=2024)
    type: str = Field(default="automovil")
    category: str = Field(default="carga")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "plate": "letras00",
                "overview": "carro particular",  
                "model": 2024,
                "type": "auto",
                "category": "carga"
            }
        }


@vehicles_router.get('/vehicles', tags=['vehicles'], response_model=List[Vehicles], status_code=200, dependencies=[Depends(JWTBearer())])
def get_vehicles() -> List[Vehicles]:
    db = Session()
    result = VehiclesService(db).get_vehicles()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@vehicles_router.get('/vehicles/{id}', tags=['vehicles'], response_model=Vehicles)
def get_vehicles(id: int = Path(ge=1, le=2000))-> Vehicles:
    db = Session()
    result = db.query(VehiclesModel).filter(VehiclesModel.id == id).first()
    if not result:
        return JSONResponse(status_code = 404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@vehicles_router.get('/vehicles/', tags=['vehicles'], response_model=List[Vehicles])
def get_vehicles_by_category(category: str = Query(min_length=4, max_length=15)) -> List[Vehicles]:
    db = Session()
    result = db.query(VehiclesModel).filter(VehiclesModel.category == category).all()
    data = [item for item in vehicles if item['category'] == category ]
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# inicio de código para el método POST
@vehicles_router.post('/vehicles', tags=['vehicles'], response_model=dict, status_code=201)
def create_vehicles(vehicles: Vehicles) -> dict:
    db = Session()# para conectarme a mi base de datos
    new_vehicle = VehiclesModel(**vehicles.dict())# para conectar mi modelo indicandole que se cree como dic y cree los parametros que ya le he indicado
    db.add(new_vehicle)# para agregar ese nuevo vehiculo a mi clase Vehicles
    db.commit()# y con esto se actualiza mi db para que se reflejen mis ultimos cambios
    return JSONResponse(status_code=201, content={"message": "the vehicle has been registered succesfully"})
        
#inicio decódigo para el método PUT
@vehicles_router.put('/vehicles/{id}', tags=['vehicles'], response_model=dict, status_code=200)
def update_vehicles(id: int, vehicle: Vehicles) -> dict:
    db = Session()
    result = db.query(VehiclesModel).filter(VehiclesModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})

    # Actualizar solo los campos que están presentes en la solicitud
    update_data = vehicle.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(result, key, value)
    
    db.commit()
    return JSONResponse(status_code=200, content={"message": "The vehicle has been modified successfully"})

# inicio de códio para el metodo DELETE
@vehicles_router.delete('/vehicles/{id}', tags=['vehicles'], response_model=dict, status_code=200)
def delete_vehicles(id: int)-> dict:
    db = Session()
    result = db.query(VehiclesModel).filter(VehiclesModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    db.delete(result)
    db.commit()   
    return JSONResponse(status_code=200, content={"message": "the vehicle has been deleted succesfully"})