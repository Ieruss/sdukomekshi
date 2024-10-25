from sqlalchemy import BigInteger, DateTime, String, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True


class UserModel(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    login: Mapped[str | None] = mapped_column(String(150), nullable=True)
    password: Mapped[str | None] = mapped_column(String(150), nullable=True)
    fullname: Mapped[str | None] = mapped_column(String(150), nullable=True)
    username: Mapped[str | None] = mapped_column(String(150), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default='not_registered')
    created: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.timezone('Asia/Almaty', func.now()))
    updated: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.timezone('Asia/Almaty', func.now()), onupdate=func.timezone('Asia/Almaty', func.now()))

    schedules: Mapped[list["ScheduleModel"]] = relationship(
        "ScheduleModel", back_populates="user", cascade="all, delete-orphan"
    )
    grades: Mapped[list["GradeModel"]] = relationship(
        "GradeModel", back_populates="user", cascade="all, delete-orphan"
    )


class ScheduleModel(Base):
    __tablename__ = 'schedules'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    time: Mapped[str] = mapped_column(String(10))
    location: Mapped[str] = mapped_column(String(100))
    day: Mapped[str] = mapped_column(String(10))
    lesson: Mapped[str] = mapped_column(String(100))
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"))
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="schedules")


class GradeModel(Base):
    __tablename__ = 'grades'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    lesson: Mapped[str] = mapped_column(String(10))
    absence: Mapped[str] = mapped_column(String(10), default="0")
    grade: Mapped[str] = mapped_column(String(10), default=None)
    letter_grade: Mapped[str] = mapped_column(String(10), default=None)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"))
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="grades")


class MessageModel(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    from_message_id: Mapped[int] = mapped_column(BigInteger)
    to_message_id: Mapped[int] = mapped_column(BigInteger)
    question: Mapped[str] = mapped_column(String)
    answer: Mapped[str | None] = mapped_column(String, nullable=True, default=None)

