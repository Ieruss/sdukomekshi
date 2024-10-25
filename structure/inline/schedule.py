from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def schedule_inline_keyboard(part):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="MO-WE", callback_data=f"schedule_part_{part}_0"),
                InlineKeyboardButton(text="TH-SA", callback_data=f"schedule_part_{part}_1")
            ]
        ]
    )
    return keyboard
