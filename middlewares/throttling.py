from aiogram import BaseMiddleware, types

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, redis, limit: int = 10, window: int = 60):
        super().__init__()
        self.redis = redis
        self.limit = limit
        self.window = window

    async def __call__(self, handler, event, data):
        if isinstance(event, types.Update) and event.message:
            if isinstance(event.message, types.Message):
                user_id = event.message.from_user.id
                key = f"user:{user_id}:requests"
                warning_key = f"user:{user_id}:warning_sent"

                current_count = await self.redis.incr(key)
                if current_count == 1:
                    await self.redis.expire(key, self.window)

                if current_count > self.limit:
                    warning_sent = await self.redis.get(warning_key)
                    if not warning_sent:
                        await event.message.reply("⚠️ Please wait (1 minute) before sending more messages.")
                        await self.redis.set(warning_key, "1", ex=self.window)
                    return

                await self.redis.delete(warning_key)

        return await handler(event, data)
