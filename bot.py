import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging
from database import init_db, add_transaction, get_balance, get_summary

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привет! Я бот для учёта финансов.\n"
        "Используй:\n"
        "/доход 1000 еда\n"
        "/расход 300 транспорт\n"
        "/баланс\n"
        "/сводка"
    )

def handle_income(update: Update, context: CallbackContext):
    try:
        amount = float(context.args[0])
        category = context.args[1] if len(context.args) > 1 else "Другое"
        add_transaction(update.effective_user.id, "income", amount, category)
        update.message.reply_text(f"✅ Доход {amount} в категории '{category}' добавлен!")
    except (IndexError, ValueError):
        update.message.reply_text("❌ Используй: /доход <сумма> [категория]")

def handle_expense(update: Update, context: CallbackContext):
    try:
        amount = float(context.args[0])
        category = context.args[1] if len(context.args) > 1 else "Другое"
        add_transaction(update.effective_user.id, "expense", amount, category)
        update.message.reply_text(f"✅ Расход {amount} в категории '{category}' добавлен!")
    except (IndexError, ValueError):
        update.message.reply_text("❌ Используй: /расход <сумма> [категория]")

def show_balance(update: Update, context: CallbackContext):
    balance = get_balance(update.effective_user.id)
    update.message.reply_text(f"💰 Баланс: {balance:.2f}")

def show_summary(update: Update, context: CallbackContext):
    income, expense = get_summary(update.effective_user.id)
    balance = income - expense
    update.message.reply_text(
        f"📊 Сводка:\n"
        f"Доходы: {income:.2f}\n"
        f"Расходы: {expense:.2f}\n"
        f"Баланс: {balance:.2f}"
    )

def main():
    init_db()
    
    # СЮДА ВСТАВЬ СВОЙ ТОКЕН!
    TOKEN = "8384481730:AAH0q69zUDAFXZ-Ry0hgGtkL7LFA96XFs7Q"
    
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("доход", handle_income))
    dp.add_handler(CommandHandler("расход", handle_expense))
    dp.add_handler(CommandHandler("баланс", show_balance))
    dp.add_handler(CommandHandler("сводка", show_summary))

    print("Бот запущен!")
    updater.start_polling()
    updater.idle()
    
# В самом конце bot.py (перед if __name__ == "__main__")

def main():
    init_db()
    TOKEN = os.environ.get("BOT_TOKEN")  # ← будем брать токен из переменной среды
    if not TOKEN:
        raise ValueError("Токен не задан! Установите переменную BOT_TOKEN.")
    
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("доход", handle_income))
    dp.add_handler(CommandHandler("расход", handle_expense))
    dp.add_handler(CommandHandler("баланс", show_balance))
    dp.add_handler(CommandHandler("сводка", show_summary))

    print("✅ Бот запущен и работает в облаке!")
    updater.start_polling()
    updater.idle()
if __name__ == "__main__":
    main()
