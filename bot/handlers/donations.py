from telegram import Update
from telegram.ext import CallbackContext

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

    if text in ("в другой раз", "не сейчас", "нет", "потом", "отмена"):
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

    # TODO: здесь должен быть вызов Django API или Telegram Payments:
    # api_client.create_donation(telegram_id=user.id, amount=amount)
    # или send_invoice(...) с provider_token и т.д.
    print(f"[DONATION INTENT] from {user.id} (@{user.username}): {amount} RUB")

    update.message.reply_text(
        f"Спасибо! Ты выбрал(а) поддержать митап на {amount} ₽\n\n"
    )

    return True