import os

from io import BytesIO
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from PIL import Image

from skrman.database.crud import (
    add_description,
    add_sticker,
    search_sticker,
    delete_description,
)
from skrman.utils import get_sticker_type

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()


@dp.message(Command("start"))
async def on_cmd_start(message: types.Message):
    await message.reply(
        """
这是一个表情包管理机器人.
向它发送 sticker、图片、gif 等资源并回复一个关键字，就可以将资源关联到这个关键字上.
之后，当你使用 inline 模式时，就可以通过关键字搜索到这个资源.
"""
    )


@dp.message(F.photo)
@dp.message(F.document.mime_type.contains("image"))
async def on_msg_photo(message: types.Message, bot: Bot):
    """
    将用户发来的图片转换为 webp 再发送回去
    """
    if message.photo:
        image = await bot.download(message.photo[-1].file_id)
    elif message.document:
        image = await bot.download(message.document.file_id)
    io = BytesIO()
    Image.open(image).save(io, "webp")
    io.seek(0)
    input_file = types.BufferedInputFile(io.read(), filename="image.webp")
    await message.reply_sticker(input_file)


@dp.message(F.reply_to_message.photo & F.text)
@dp.message(F.reply_to_message.document & F.text)
@dp.message(F.reply_to_message.animation & F.text)
@dp.message(F.reply_to_message.video & F.text)
@dp.message(F.reply_to_message.audio & F.text)
@dp.message(F.reply_to_message.sticker & F.text)
async def on_msg_reply(message: types.Message):
    """
    添加用户对 sticker 的描述，或者删除描述
    """
    file_type, file_id, file_unique_id = get_sticker_type(message.reply_to_message)

    if message.text == "/delete":
        delete_description(message.from_user.id, file_unique_id)
        await message.reply("删除成功")
    else:
        sticker = add_sticker(file_type, file_id, file_unique_id)
        add_description(sticker.id, message.from_user.id, message.text)
        await message.reply("添加成功")


@dp.inline_query(F.query)
async def on_inline_query(query: types.InlineQuery):
    stickers = search_sticker(query.from_user.id, query.query)
    results = []
    for sticker in stickers:
        result = None
        match sticker.file_type:
            case "photo":
                result = types.InlineQueryResultCachedPhoto(
                    id=sticker.file_unique_id, photo_file_id=sticker.file_id
                )
            case "document":
                result = types.InlineQueryResultCachedDocument(
                    id=sticker.file_unique_id, document_file_id=sticker.file_id
                )
            case "animation":
                result = types.InlineQueryResultCachedGif(
                    id=sticker.file_unique_id, gif_file_id=sticker.file_id
                )
            case "video":
                result = types.InlineQueryResultCachedVideo(
                    id=sticker.file_unique_id, video_file_id=sticker.file_id
                )
            case "audio":
                result = types.InlineQueryResultCachedAudio(
                    id=sticker.file_unique_id, audio_file_id=sticker.file_id
                )
            case "sticker":
                result = types.InlineQueryResultCachedSticker(
                    id=sticker.file_unique_id, sticker_file_id=sticker.file_id
                )
        results.append(result)
    await query.answer(results)
