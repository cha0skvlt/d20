from __future__ import annotations

import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from dotenv import load_dotenv

from .utils import parse_dice_expression

TOKEN_ENV = "TELEGRAM_BOT_TOKEN"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    await update.message.reply_text("Send dice expression like '2d6 + 3'")


async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    text = update.message.text or ""
    try:
        result = parse_dice_expression(text)
    except ValueError:
        return
    reply = (
        f"Rolls: {result['rolls']}\n"
        f"Modifier: {result['modifier']}\n"
        f"Total: {result['total']}"
    )
    await update.message.reply_text(reply)


def main() -> None:
    load_dotenv()
    token = os.getenv(TOKEN_ENV)
    if not token:
        raise RuntimeError(f"Set {TOKEN_ENV} environment variable")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, roll))
    app.run_polling()


if __name__ == "__main__":
    main()
