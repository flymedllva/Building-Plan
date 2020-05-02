from typing import List

from fastapi import APIRouter, Depends

from app.core import arangodb
from app.database import database
from app.schemas.building_import import ImportData
from app.schemas.building import BuildingSchema


router = APIRouter()


@router.get("/route/{building}/{of}/{to}", tags=["route"])
async def search_route(building: str, of: str, to: str):
    """
    Ищет путь в здании

    :param building: здание, например building_1
    :param of: id откуда путь, например 001102
    :param to: id куда путь, например 001105
    :return:
    """

    return await database.find_shortest_path(
        of=f"{building}_objects/{of}", to=f"{building}_objects/{to}", graph=building
    )


@router.post("/import/", tags=["core"], response_model=BuildingSchema)
async def import_file(data: ImportData):
    """
    Загружает файл в ArangoDB

    :param data: схема
    :return:
    """

    return await arangodb.parsing_imported_file(data)
