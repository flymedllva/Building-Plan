import os

import aiofiles
from fastapi import UploadFile

from app.config import DIRECTORY


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


async def check_file_in_background_folder(label: str, object: UploadFile) -> bool:
    """
    Обновляет файл в директории

    :param label:
    :param object:
    :return:
    """

    background_folder = DIRECTORY + "backgrounds/"

    if not os.path.exists(background_folder):
        os.makedirs(background_folder)

    file_path = background_folder + label
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(await object.read())

    return True
