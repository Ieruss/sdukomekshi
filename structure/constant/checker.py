from parsing.login import login_user


def check_user_login(login: str) -> bool:
    if len(login) != 9:
        return False
    if not login.isdigit():
        return False
    return True


async def check_user(user_login, user_password) -> bool:
    try:
        if await login_user(user_login, user_password):
            return True
        else:
            return False
    except:
        return False
