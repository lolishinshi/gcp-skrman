import sys
import logging
from skrman.handler import dp, bot

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
dp.run_polling(bot)
