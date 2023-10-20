import traceback

from functions_framework import http
from unsync import unsync
from werkzeug import Request


@unsync
async def async_handler(request: Request):
    pass


@http
def handler(request: Request):
    try:
        async_handler(request).result()
    except Exception as e:
        traceback.print_exc()
    return ""
