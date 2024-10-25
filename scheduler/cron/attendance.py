import asyncio
import sys
from loader import bot
from loader import db
from parsing.grades import parse_grades
from scheduler.sender import send_message


def generate_attendance_message(old_absences, new_absences):
    if new_absences > 30:
        return "😱 <b>Warning:</b>\n\nYou've exceeded the <b>30%</b> absence limit, and now it's a <b>retake</b>.\nMake a plan to catch up!"
    elif new_absences == 30:
        return "🚨 <b>Alert:</b>\n\nYou've reached the <b>maximum</b> of <b>30%</b> absences.\nAnother missed class will result in a <b>retake</b>."
    elif new_absences > old_absences:
        if new_absences > 25:
            return "😟 <b>Alert:</b>\n\nYour absence has increased to <b>{}%</b> (up from <b>{}%</b>).\nYou're getting close to the <b>30%</b> limit.".format(new_absences, old_absences)
        elif 20 < new_absences <= 25:
            return "⚠️ <b>Warning:</b>\n\nYour absence has increased to <b>{}%</b>, which is higher than before (<b>{}%</b>).\nStay attentive to avoid the <b>30%</b> threshold.".format(new_absences, old_absences)
        elif 10 < new_absences <= 20:
            return "⚠️ <b>Note:</b>\n\nYou've missed <b>{}%</b> of your classes (up from <b>{}%</b>).\nKeep an eye on your attendance!".format(new_absences, old_absences)
        else:
            return "😊 <b>Good job!</b>\n\nYour attendance is now at <b>{}%</b>.\nYou're doing well but don't lose focus!".format(new_absences)
    elif new_absences < old_absences:
        if new_absences < 5:
            return "🎉 <b>Great work!</b>\n\nYour attendance has improved to <b>{}%</b>!\nKeep it up and stay engaged.".format(new_absences)
        elif 5 <= new_absences < 10:
            return "😊 <b>Nice progress!</b>\n\nYour attendance is now at <b>{}%</b>.\nKeep going!".format(new_absences)
        elif 10 <= new_absences < old_absences:
            return "👍 <b>Improvement detected!</b>\n\nYour attendance is now at <b>{}%</b>, down from <b>{}%</b>.\nKeep it steady to avoid issues.".format(new_absences, old_absences)
        else:
            return "🙂 <b>Good job!</b>\n\nYour attendance is now at <b>{}%</b>.\nYou're on the right track!".format(new_absences)
    else:
        return "⚠️ <b>Reminder:</b>\n\nYour attendance remains at <b>{}%</b>.\nStay consistent to maintain good standing.".format(new_absences)



async def periodic_attendance_check(ctx):
    users_id = await db.user.get_all()
    for user_id in users_id:
        username, password = await db.user.get_login_password(user_id)
        result = await db.grade.get_attendance(user_id)

        old_data = {
            lesson: int(attendance) if attendance not in (None, 'None') else 0
            for lesson, attendance in result
        }
        print(old_data)
        new_data = await parse_grades(username, password)

        for lesson, attendance, grade, letter_grade in new_data:
            int_attendance = int(attendance)
            if lesson in old_data:
                if old_data[lesson] != int_attendance:
                    msg = None
                    if int_attendance > old_data[lesson]:
                        msg = f"😞 attendance added in <b>{lesson}</b> from <b>{old_data[lesson]}%</b> to <b>{int_attendance}%</b>"
                    else:
                        msg = f"🎉 attendance removed in <b>{lesson}</b> from <b>{old_data[lesson]}%</b> to <b>{int_attendance}%</b>"

                    additional_msg = generate_attendance_message(old_data[lesson], int_attendance)
                    message_id = await send_message(ctx, user_id, msg)
                    await send_message(ctx, user_id, additional_msg, message_id)
                    await db.grade.update(user_id=user_id, user_grades=[(lesson, int_attendance, grade, letter_grade)])

            else:
                await db.grade.add(user_id, [(lesson, attendance, grade, letter_grade)])


# if __name__ == '__main__':
#     if sys.platform == 'win32':
#         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#
#     ctx = {
#         'bot': bot,
#     }
#     asyncio.run(periodic_attendance_check(ctx=ctx))

