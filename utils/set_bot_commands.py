from aiogram import Bot
from aiogram.methods.set_my_commands import BotCommand
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommandScopeChat
from loader import config


async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="start the bot"),
        BotCommand(command="/attendance", description="inform about your attendance"),
        BotCommand(command="/grade", description="inform about your grade"),
        BotCommand(command="/schedule", description="you can see your schedule"),
        BotCommand(command="/message", description="send a message to the admin"),
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())

    admin_commands = [
        BotCommand(command="/start", description="start the bot"),
        BotCommand(command="/attendance", description="inform about your attendance"),
        BotCommand(command="/grade", description="inform about your grade"),
        BotCommand(command="/schedule", description="you can see your schedule"),
        BotCommand(command="/message", description="send a message to the admin"),
        BotCommand(command="/send_all", description="send a message to all users"),
        BotCommand(command="/statistics", description="get statistics"),
    ]
    await bot.set_my_commands(commands=admin_commands, scope=BotCommandScopeChat(chat_id=config.admins.list[0]))


async def set_start_commands(user_id: int):
    from loader import bot
    commands = [
        BotCommand(command="/start", description="start the bot"),
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeChat(chat_id=user_id))
