from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class Admins:
    list: list[str]


@dataclass
class Chats:
    QA_CHAT_ID: int


@dataclass
class Postgres:
    SCHEMA: str
    USER: str
    PASSWORD: str
    HOST: str
    NAME: str
    PORT: int
    IS_ECHO: bool

    def dsn(self) -> str:
        return f"{self.SCHEMA}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


@dataclass
class Config:
    tg_bot: TgBot
    admins: Admins
    db: Postgres
    chats: Chats


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env('BOT_TOKEN')),
        admins=Admins(list=env.list('ADMINS')),
        db=Postgres(SCHEMA=env('DB_SCHEMA'),
                    USER=env('DB_USER'),
                    PASSWORD=env('DB_PASS'),
                    HOST=env('DB_HOST'),
                    NAME=env('DB_NAME'),
                    PORT=env.int('DB_PORT'),
                    IS_ECHO=env.bool('IS_ECHO')),
        chats=Chats(QA_CHAT_ID=env.int('QA_CHAT_ID')),
    )
