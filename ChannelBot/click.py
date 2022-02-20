import os
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    CallbackQuery,
)
from pyrogram import Client, filters
from pyrogram.errors import MessageNotModified
from dotenv import load_dotenv

@Bot.on_message(filters.command(["count"]))
async def count(_, update: Message):
    await update.reply_text(
        text="Total 0 clicks",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Click Here", callback_data="count")]]
        ),
    )


@Bot.on_message(filters.command("reset"))
async def reset_count(_, update: Message):
    if (reply := update.reply_to_message) and (reply.reply_markup):
        try:
            await reply.edit(text="Total 0 clicks", reply_markup=reply.reply_markup)
            await reply.reply_text("Counter has been reset successfully", True)
        except MessageNotModified:
            await reply.reply_text("Counter is already at 0", True)
    else:
        await update.reply_text("Please reply to an active counter message")


@Bot.on_callback_query(filters.regex(r"^count$"))
async def callback(_, update: CallbackQuery):
    count = int(update.message.text.split(" ")[1]) + 1
    text = f"Total {count} clicks"
    await update.message.edit_text(text=text, reply_markup=update.message.reply_markup)
    await update.answer(text=f"Added your click,\n\n{text}", show_alert=True)


