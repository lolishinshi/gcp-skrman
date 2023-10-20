from aiogram import types
from skrman.database.crud import FileType


def get_sticker_type(message: types.Message) -> tuple[FileType, str, str]:
    if f := message.photo:
        return "photo", f[-1].file_id, f[-1].file_unique_id
    elif f := message.document:
        return "document", f.file_id, f.file_unique_id
    elif f := message.animation:
        return "animation", f.file_id, f.file_unique_id
    elif f := message.video:
        return "video", f.file_id, f.file_unique_id
    elif f := message.audio:
        return "audio", f.file_id, f.file_unique_id
    elif f := message.sticker:
        return "sticker", f.file_id, f.file_unique_id
    else:
        raise ValueError("Unknown message type")
