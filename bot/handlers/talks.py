from telegram import Update
from telegram.ext import CallbackContext


def start_ask_question(update: Update, context: CallbackContext) -> None:
    context.user_data["awaiting_question"] = True

    update.message.reply_text(
        "Окей! Напиши, пожалуйста, свой вопрос для текущего спикера.\n\n"
        "Если передумаешь, нажми любую кнопку внизу, и я отменю ввод вопроса."
    )


def handle_question_if_waiting(update: Update, context: CallbackContext) -> bool:
    if not context.user_data.get("awaiting_question"):
        return False

    question_text = update.message.text
    user = update.effective_user

    # TODO: здесь будет вызов Django API, например:
    # api_client.create_question(
    #     telegram_id=user.id,
    #     text=question_text,
    # )
    print(f"[QUESTION] from {user.id} (@{user.username}): {question_text}")

    context.user_data["awaiting_question"] = False

    update.message.reply_text(
        "Спасибо! Я передал твой вопрос спикеру.\n"
        "Можешь задать ещё один или вернуться к программе/нетворкингу через меню."
    )

    return True


def show_schedule(update: Update, context: CallbackContext) -> None:
    # TODO: запросить программу из Django API и срендерить её
    dummy_text = (
        "Программа митапа (пример):\n\n"
        "19:00 — Вступительное слово\n"
        "19:15 — Доклад 1: «Введение в asyncio»\n"
        "20:00 — Доклад 2: «Django в продакшене»\n"
        "20:45 — Нетворкинг\n"
        "21:15 — Доклад 3: «Как не бояться рефакторинга»\n"
    )

    update.message.reply_text(dummy_text)