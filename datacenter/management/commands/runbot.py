import logging
from django.core.management.base import BaseCommand
from telegram.ext import Updater

from tg_bot.config import TELEGRAM_BOT_TOKEN
from tg_bot.common import register_common_handlers


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **options):
        self.stdout.write("Запуск телеграм бота...")
        
        try:
            updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
            dispatcher = updater.dispatcher

            register_common_handlers(dispatcher)

            logger.info("Бот запускается...")
            self.stdout.write(
                self.style.SUCCESS("Бот запущен. Нажми Ctrl+C для остановки.")
            )
            
            updater.start_polling()
            updater.idle()
            
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            self.stdout.write(
                self.style.ERROR(f"Ошибка при запуске бота: {e}")
            )
