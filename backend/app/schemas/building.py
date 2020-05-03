from typing import List, Dict, Union

from pydantic import AnyHttpUrl, validator
from app.schemas.base import FastModel


class BuildingPolygon(FastModel):
    type: str
    id: str
    points: str
    marker: Union[str, None]


class BuildingPath(FastModel):
    type: str
    id: str
    d: str
    marker: Union[str, None]


class BuildingRect(FastModel):
    type: str
    id: str
    x: float
    y: float
    width: float
    height: float
    marker: Union[str, None]


class BuildingEntrance(FastModel):
    type: str
    id: str
    x1: float
    y1: float
    x2: float
    y2: float


class BuildingRoute(FastModel):
    type: str
    id: str
    x1: float
    y1: float
    x2: float
    y2: float


class BuildingEntranceRoute(FastModel):
    type: str
    id: str


class BuildingMarker(FastModel):
    title: str
    type: str
    description: Union[str, None]
    site: Union[str, None]


class BuildingLayer(FastModel):
    id: int
    objects: List[Union[BuildingRect, BuildingPath, BuildingPolygon]]
    entrances: List[BuildingEntrance]
    routes: List[Union[BuildingRoute, BuildingEntranceRoute]]
    markers: Dict[str, BuildingMarker]


class BuildingSchema(FastModel):
    title: str
    designation: str
    background: AnyHttpUrl
    layers: List[BuildingLayer]
