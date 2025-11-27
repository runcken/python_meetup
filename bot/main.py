import logging

from telegram.ext import Updater
from config import TELEGRAM_BOT_TOKEN
from handlers.common import register_common_handlers


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    register_common_handlers(dispatcher)

    logger.info("Бот запускается...")

    updater.start_polling()
    logger.info("Бот запущен. Нажми Ctrl+C для остановки.")

    updater.idle()


if __name__ == "__main__":
    main()
