from typing import List, Dict, Union

from pydantic import AnyHttpUrl
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
    p1: str
    p2: str
    x1: float
    y1: float
    x2: float
    y2: float


class BuildingEntranceRoute(FastModel):
    type: str
    id: str
    p1: str
    p2: str


class BuildingMarker(FastModel):
    title: str
    description: str
    site: str


class BuildingLayer(FastModel):
    objects: List[Union[BuildingRect, BuildingPath, BuildingPolygon]]
    entrances: List[BuildingEntrance]
    routes: List[Union[BuildingRoute, BuildingEntranceRoute]]
    markers: Dict[str, BuildingMarker]


class BuildingSchema(FastModel):
    title: str
    designation: str
    background: AnyHttpUrl
    layers: List[BuildingLayer]
