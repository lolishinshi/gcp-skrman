import traceback

from functions_framework import http
from unsync import unsync
from werkzeug import Request
from aiogram.types import Update
from skrman.handler import bot, dp


@unsync
async def async_handler(request: Request):
    if request.args.get("action") == "set_webhook":
        url = request.base_url.replace("http://", "https://") + "skrman"
        await bot.set_webhook(
            url, allowed_updates=["inline_query", "message", "callback_query"]
        )
    elif request.args.get("action") == "delete_webhook":
        await bot.delete_webhook()
    else:
        update = Update.model_validate(request.get_json(), context={"bot": bot})
        await dp.feed_update(bot, update)


@http
def handler(request: Request):
    try:
        async_handler(request).result()
    except Exception as e:
        traceback.print_exc()
    return ""
