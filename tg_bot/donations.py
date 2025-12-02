from telegram import Update
from telegram.ext import CallbackContext
from django.utils import timezone
from datacenter.models import Participant, Donation
import logging

logger = logging.getLogger(__name__)

DONATION_STATE_KEY = "donation_state"
DONATION_AMOUNT_KEY = "donation_amount"


def start_donation(update: Update, context: CallbackContext) -> None:
    context.user_data[DONATION_STATE_KEY] = "waiting_for_amount"

    text = (
        "Спасибо, что хочешь поддержать митап!\n\n"
        "Донаты помогают оплачивать площадку и делать следующие мероприятия лучше.\n\n"
        "Если хочешь задонатить, напиши сумму в рублях цифрами (например: 300 или 500).\n"
        "Если передумал, просто напиши «В другой раз»."
    )

    update.message.reply_text(text)


def handle_donation_message_if_active(update: Update, context: CallbackContext) -> bool:
    state = context.user_data.get(DONATION_STATE_KEY)
    if state != "waiting_for_amount":
        return False

    text_raw = update.message.text or ""
    text = text_raw.strip().lower()

    if text in ("в другой раз", "не сейчас", "нет", "потом", "отмена", "отменить"):
        context.user_data[DONATION_STATE_KEY] = None
        context.user_data.pop(DONATION_AMOUNT_KEY, None)

        update.message.reply_text(
            "Без проблем!\n"
            "Спасибо, что вообще задумался поддержать митап.\n"
            "Можешь в любой момент вернуться к донату через кнопку «Поддержать митап»."
        )
        return True

    digits = "".join(char for char in text_raw if char.isdigit())
    if not digits:
        update.message.reply_text(
            "Я не понял сумму\n"
            "Пожалуйста, напиши только число в рублях, например: 200 или 500.\n"
            "Или напиши «В другой раз», если передумал."
        )
        return True

    amount = int(digits)
    if amount <= 0:
        update.message.reply_text(
            "Сумма должна быть больше нуля\n"
            "Напиши, пожалуйста, сумму в рублях или «В другой раз»."
        )
        return True

    context.user_data[DONATION_AMOUNT_KEY] = amount
    context.user_data[DONATION_STATE_KEY] = None

    user = update.effective_user

    try:
        participant, created = Participant.objects.get_or_create(
            telegram_id=user.id,
            defaults={
                "username": user.username,
                "full_name": f"{user.first_name} {user.last_name or ''}".strip()
            }
        )
        
        if not created:
            update_fields = {}
            if user.username and user.username != participant.username:
                participant.username = user.username
                update_fields['username'] = user.username
            
            full_name = f"{user.first_name} {user.last_name or ''}".strip()
            if full_name and full_name != participant.full_name:
                participant.full_name = full_name
                update_fields['full_name'] = full_name
            
            if update_fields:
                participant.save(update_fields=update_fields)
        
        donation = Donation.objects.create(
            participant=participant,
            amount=amount
        )
        
        logger.info(f"DONATION created: ID={donation.id}, from {user.id} (@{user.username}): {amount} RUB")
        
        update.message.reply_text(
            f"*Спасибо за поддержку!*\n\n"
            f"Ты поддержал(а) митап на *{amount} ₽*\n\n"
            f"Твой донат поможет сделать следующие мероприятия ещё лучше!\n\n"
            f"*Детали доната:*\n"
            f"• Сумма: {amount} ₽\n"
            f"• Дата: {donation.created_at.strftime('%d.%m.%Y %H:%M')}\n"
            f"• ID транзакции: {donation.id}\n\n"
            f"_Если у тебя есть вопросы по донату, свяжись с организаторами_",
            parse_mode='Markdown'
        )

    except Exception as e:
        logger.error(f"Error saving donation: {e}", exc_info=True)
        update.message.reply_text(
            "Произошла ошибка при обработке доната. Попробуйте позже или свяжитесь с организаторами."
        )
    
    return True
