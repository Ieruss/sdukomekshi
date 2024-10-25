import asyncio
from loader import db
from scheduler.sender import send_message
from loader import config


def create_progress_bar(progress, bar_length):
    filled_length = int(bar_length * progress // 100)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    return f"[{bar}]"

async def notify_all_users(ctx, msg_id, main_msg_id, text):
    admin = config.admins.list[0]
    users_id = await db.user.get_all()

    progress_bar_length = 20
    last_update, update_interval = 0, 3
    print(users_id)
    for i, user_id in enumerate(users_id):
        if str(user_id) != admin:
            await send_message(ctx, user_id, text)

        progress = int(i / len(users_id) * 100)
        if progress >= last_update + update_interval:
            progress_bar = create_progress_bar(progress, progress_bar_length)
            await ctx['bot'].edit_message_text(chat_id=admin, message_id=msg_id, text=f"{progress_bar} {progress}% ")
            last_update = progress
            await asyncio.sleep(0.1)

    await ctx['bot'].delete_message(chat_id=admin, message_id=msg_id)
    await ctx['bot'].edit_message_text(chat_id=admin, message_id=main_msg_id, text=f"✅ All users have been notified.")

