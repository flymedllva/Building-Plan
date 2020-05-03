from typing import Union, Tuple, Dict

import ujson
from arango.exceptions import GraphCreateError, DocumentInsertError
from arango.collection import StandardCollection
from app.database import database
from app.schemas.building_import import (
    ImportData,
    ImportRect,
    ImportPath,
    ImportPolygon,
    ImportEntrance,
    ImportPoint,
    ImportLine,
    ImportEntranceLine,
    ImportUpstairLine,
)
from app.schemas.building import BuildingSchema
from app.core.exceptions import CONFLICT_GRAPH_EXCEPTION, DOCUMENT_INSERT_EXCEPTION


async def objects_to_dict_with_key(
    item: Union[ImportRect, ImportPath, ImportPolygon, ImportEntrance, ImportPoint]
) -> Dict:
    """
    Преобразует обьектвы в словарь с _key вместо id

    :param item:
    :return:
    """

    dict_item: dict = item.dict()
    dict_item["_key"] = dict_item.pop("id")

    return dict_item


async def connections_to_dict_with_key_from_to(
    item: Union[ImportLine, ImportEntranceLine, ImportUpstairLine], building_title: str
) -> Tuple[Dict, Dict]:
    """
    Преобразует связи в словарь с _key вместо id

    :param item:
    :param building_title:
    :return:
    """

    dict_item: dict = item.dict()

    dict_item["_key"] = dict_item.pop("id")
    dict_item["_from"] = f"{building_title}/{dict_item.pop('p1')}"
    dict_item["_to"] = f"{building_title}/{dict_item.pop('p2')}"

    dict_item_2 = dict_item.copy()
    dict_item["_key"] = dict_item["_key"] + "___2"
    dict_item["_to"], dict_item["_from"] = dict_item["_from"], dict_item["_to"]

    return dict_item, dict_item_2


async def parsing_imported_file(data: ImportData) -> BuildingSchema:
    """
    Парсинг полученого файла + загрузка в ArangoDB

    :param data: файл
    :return:
    """

    building_objects_label = f"{data.designation}_objects"
    building_connections_label = f"{data.designation}_connections"
    building_data_label = f"{data.designation}_data"
    building_key_value_store_label = f"{data.designation}_key_value_store"

    try:
        graph = database.instance.create_graph(data.designation)
    except GraphCreateError:
        raise CONFLICT_GRAPH_EXCEPTION

    building_objects = graph.create_vertex_collection(building_objects_label)
    building_connections = graph.create_edge_definition(
        edge_collection=building_connections_label,
        from_vertex_collections=[building_objects_label],
        to_vertex_collections=[building_objects_label],
    )

    if database.instance.has_collection(building_data_label):
        database.instance.delete_collection(building_data_label)
    building_data: StandardCollection = database.instance.create_collection(
        building_data_label
    )

    if database.instance.has_collection(building_key_value_store_label):
        database.instance.delete_collection(building_key_value_store_label)
    building_key_value_store: StandardCollection = database.instance.create_collection(
        building_key_value_store_label
    )

    try:
        for layer in data.layers:
            for item in layer.objects:
                building_objects.insert(await objects_to_dict_with_key(item))
            for item in layer.entrances:
                building_objects.insert(await objects_to_dict_with_key(item))
            for item in layer.points:
                building_objects.insert(await objects_to_dict_with_key(item))
            for item in layer.routes:
                item_1, item_2 = await connections_to_dict_with_key_from_to(
                    item, building_objects_label
                )
                building_connections.insert(item_1)
                building_connections.insert(item_2)

        for item in data.upstairs:
            item_1, item_2 = await connections_to_dict_with_key_from_to(
                item, building_objects_label
            )
            building_connections.insert(item_1)
            building_connections.insert(item_2)
    except DocumentInsertError as e:
        error = DOCUMENT_INSERT_EXCEPTION
        error.detail = f"{error.detail} {e}"
        raise error

    building_schema = BuildingSchema(**data.dict())
    building_data.insert({"data": ujson.dumps(building_schema.dict())})

    return building_schema
