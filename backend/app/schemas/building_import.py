from typing import List, Dict, Union

from pydantic import AnyHttpUrl
from app.schemas.base import FastModel


class ImportPolygon(FastModel):
    type: str
    id: str
    points: str
    marker: Union[str, None]


class ImportPath(FastModel):
    type: str
    id: str
    d: str
    marker: Union[str, None]


class ImportRect(FastModel):
    type: str
    id: str
    x: float
    y: float
    width: float
    height: float
    marker: Union[str, None]


class ImportEntrance(FastModel):
    type: str
    id: str
    x1: float
    y1: float
    x2: float
    y2: float


class ImportPoint(FastModel):
    type: str
    id: str
    cx: float
    cy: float


class ImportLine(FastModel):
    type: str
    id: str
    p1: str
    p2: str
    time: float
    x1: float
    y1: float
    x2: float
    y2: float


class ImportEntranceLine(FastModel):
    type: str
    id: str
    p1: str
    p2: str


class ImportUpstairLine(FastModel):
    type: str
    id: str
    p1: str
    p2: str
    time: int


class ImportMarker(FastModel):
    title: str
    type: str
    description: Union[str, None]
    site: Union[str, None]


class ImportLayer(FastModel):
    id: int
    objects: List[Union[ImportRect, ImportPath, ImportPolygon]]
    entrances: List[ImportEntrance]
    points: List[ImportPoint]
    routes: List[Union[ImportLine, ImportEntranceLine]]
    markers: Dict[str, ImportMarker]


class ImportData(FastModel):
    title: str
    designation: str
    layers: List[ImportLayer]
    upstairs: List[ImportUpstairLine]
