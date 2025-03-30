from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random

# --- База упражнений ---
exercises = {
    "Приседания": {"reps": 40},
    "Отжимания": {"reps": 25},
    "Планка": {"time": 90},
    "Берпи": {"reps": 15},
    "Скручивания": {"reps": 50},
    "Выпады": {"reps": 30},
    "Прыжки на месте": {"reps": 30},
    "Альпинист": {"reps": 30},
    "Подъём ног": {"reps": 25},
    "Супермен": {"reps": 40},
    "Выпады назад": {"reps": 20},
    "V-складки крестом": {"reps": 30},
    "V-складки строгие": {"reps": 30},
    "Пресс": {"reps": 30},
    "Отжимания с отрывом рук": {"reps": 30},
    "Скручивания с весом": {"reps": 30},
    "Планка стульчик": {"time": 90},
    "Планка боковая": {"time": 90}
}

# --- Сложности ---
def scale_difficulty(data, level):
    if level == "easy":
        reps = int(data.get("reps", 0) * 0.75)
        time = int(data.get("time", 0) * 0.75)
    elif level == "hard":
        reps = int(data.get("reps", 0) * 1.25)
        time = int(data.get("time", 0) * 1.25)
    else:
        reps = data.get("reps")
        time = data.get("time")
    return reps, time

# --- Генерация тренировки ---
def generate_game(level):
    chosen = random.sample(list(exercises.keys()), 3)
    result = []
    for ex in chosen:
        reps, time = scale_difficulty(exercises[ex], level)
        if reps:
            result.append(f"{ex}: {reps} повторений")
        elif time:
            min = time // 60
            sec = time % 60
            t = f"{min} мин" if sec == 0 else f"{min} мин {sec} сек"
            result.append(f"{ex}: {t}")
    return result

# --- Обработчики ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("Лёгкий", callback_data="easy")],
        [InlineKeyboardButton("Средний", callback_data="medium")],
        [InlineKeyboardButton("Сложный", callback_data="hard")],
    ]
    welcome_text = (
        "🏋️ Добро пожаловать в *CrossFit Mini Games*!\n"
        "Здесь тебя ждёт мини-испытание на каждый день — 3 случайных упражнения с неожиданной дозировкой.\n\n"
        "🎯 Раз ты уже здесь — считай, ты на полпути к успеху. Осталось только нажать кнопку 😉\n\n"
        "Выбери уровень и влетай в игру! 🔥"
    )
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    level = query.data
    workout = generate_game(level)
    text = "\n".join([f"• {line}" for line in workout])
    buttons = [
        [InlineKeyboardButton("🔁 Сгенерировать ещё", callback_data=level)]
    ]
    await query.edit_message_text(f"Твоя тренировка:\n\n{text}", reply_markup=InlineKeyboardMarkup(buttons))

# --- Запуск ---
TOKEN = "8027740837:AAFlypGWqBNgyQRhMK7nqSQCO9pGIhHLzMA"

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

print("Бот запущен...")
app.run_polling()
