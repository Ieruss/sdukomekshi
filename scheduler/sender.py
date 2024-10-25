import asyncio
from asyncio.log import logger
from loader import db
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError, TelegramRetryAfter



async def send_message(ctx, user_id: int, text: str, reply_message_id: int = None):
    message_id = None
    try:
        message = await ctx['bot'].send_message(chat_id=user_id, text=text, reply_to_message_id=reply_message_id, parse_mode='HTML')
        message_id = message.message_id
    except TelegramForbiddenError:
        logger.info(f"Bot is blocked by the user: {user_id}")
        await db.user.set_status(user_id, 'banned')
    except TelegramRetryAfter as e:
        logger.info(f"Flood control exceeded. Retry after {e.retry_after} seconds.")
        await asyncio.sleep(e.retry_after)
        message = await ctx['bot'].send_message(chat_id=user_id, text=text, reply_to_message_id=reply_message_id, parse_mode='HTML')
        message_id = message.message_id
    except TelegramBadRequest as e:
        logger.info(f"Bad request: {e}")
    except Exception as e:
        logger.info(f"Unexpected error: {e}")
    return message_id
