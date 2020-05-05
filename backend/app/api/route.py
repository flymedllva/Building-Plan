from typing import List

import ujson
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from arango.exceptions import CollectionDeleteError

from app.core import arangodb
from app.core.exceptions import DELETE_EXCEPTION
from app.config import DIRECTORY
from app.database import database
from app.core.helpers import check_file_in_background_folder
from app.schemas.building import BuildingSchema
from app.schemas.building_import import ImportData

router = APIRouter()


@router.get("/buildings", tags=["collections"], response_model=List[str])
async def get_buildings():
    """
    Получает все названия зданий
    """

    return [
        item["_key"] for item in await database.find_or_create_collection("buildings")
    ]


@router.get("/{building}", tags=["collections"], response_model=BuildingSchema)
async def get_building(building: str):
    """
    Получает JSON здания
    """

    if database.instance.has_collection("buildings"):
        building_collection = database.instance.collection("buildings")
        for data in building_collection:
            if data["_key"] == building:
                return BuildingSchema(**ujson.loads(data["data"]))


@router.get("/{building}/background", tags=["collections"])
async def get_building_background(building):
    """
    Получает фон здания
    """

    return FileResponse(f"{DIRECTORY}backgrounds/{building}.svg")


@router.put("/{building}/background", tags=["collections"], response_model=bool)
async def update_building_background(building, file: UploadFile = File(...)):
    """
    Загружает новый фон для здания
    """

    if ".svg" in file.filename and database.instance.has_collection(
        building + "_objects"
    ):
        return await check_file_in_background_folder(building + ".svg", file)
    return False


@router.delete(
    "/{building}", tags=["collections"], response_model=bool,
)
async def delete_building(building: str):
    """
    Удаляет здание
    """

    try:
        database.instance.delete_collection(f"{building}_objects")
        database.instance.delete_collection(f"{building}_connections")
        database.instance.delete_collection(f"{building}_data")
    except CollectionDeleteError:
        raise DELETE_EXCEPTION

    database.instance.delete_graph(building)

    if database.instance.has_collection("buildings"):
        building_collection = database.instance.collection("buildings")
        if building_collection.has(building):
            building_collection.delete(building)

    return True


@router.get("/route/{building}/{of}/{to}", tags=["routes"])
async def search_route_in_building(building: str, of: str, to: str):
    """
    Ищет путь в здании
    """

    return await database.find_shortest_path(
        of=f"{building}_objects/{of}", to=f"{building}_objects/{to}", graph=building
    )


@router.post("/import/", tags=["core"], response_model=BuildingSchema)
async def import_file(data: ImportData):
    """
    Загружает файл в ArangoDB
    """

    return await arangodb.parsing_imported_file(data)
