from typing import Literal

import rjieba
from peewee import fn, SQL

from ..models import Description, Sticker

FileType = Literal["photo", "document", "animation", "video", "audio", "sticker"]


def add_sticker(
    file_type: FileType, file_id: str, file_unique_id: str, title: str | None
) -> Sticker:
    """
    增加一条 sticker 记录，如果已存在则更新 file_id
    """
    Sticker.insert(
        file_id=file_id, file_unique_id=file_unique_id, file_type=file_type, title=title
    ).on_conflict(
        conflict_target=(Sticker.file_unique_id,),
        update={Sticker.file_id: file_id, Sticker.title: title},
    ).execute()
    return Sticker.get(Sticker.file_unique_id == file_unique_id)


def add_description(sticker: int, user: int, description: str):
    """
    增加一条对 sticker 的描述，每个用户只能对每个 sticker 有一条描述
    """
    # jieba 分词会将空格作为一个词，所以先去掉空格
    words = [w for w in rjieba.cut_for_search(description) if w != " "]
    tsvector = fn.to_tsvector("simple", " ".join(words))
    Description.insert(
        user=user,
        sticker=sticker,
        description=description,
        description_tsv=tsvector,
    ).on_conflict(
        conflict_target=(Description.user, Description.sticker),
        update={
            Description.description: description,
            Description.description_tsv: tsvector,
        },
    ).execute()


def delete_description(user: int, file_unique_id: int):
    sticker = Sticker.get(Sticker.file_unique_id == file_unique_id)
    Description.delete().where(
        Description.user == user, Description.sticker == sticker
    ).execute()


def search_sticker(user: int, query: str) -> list[Sticker]:
    words = " ".join([w for w in rjieba.cut_for_search(query) if w != " "])
    result = (
        Description.select(
            Description,
            fn.ts_rank(
                Description.description_tsv, fn.plainto_tsquery("simple", words)
            ).alias("rank"),
        )
        .where(Description.description_tsv.match(words, language="simple", plain=True))
        .order_by(SQL("rank").desc())
        .limit(8)
    )
    return [d.sticker for d in result]
