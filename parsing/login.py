import asyncio

import aiohttp
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

from structure.constant.template import login_data_template
from structure.constant.url import LOGIN_URL


async def login_user(username: str, password: str, session: aiohttp.ClientSession = None) -> bool:
    login_data = login_data_template.copy()
    login_data['username'] = username
    login_data['password'] = password

    if session is None:
        HEADERS = {'User-Agent': UserAgent().random}
        async with aiohttp.ClientSession(headers=HEADERS) as new_session:
            return await _perform_login(new_session, login_data)
    else:
        return await _perform_login(session, login_data)

async def _perform_login(session: aiohttp.ClientSession, login_data: dict) -> bool:
    async with session.post(LOGIN_URL, data=login_data, ssl=False) as response:
        if response.status != 200:
            return False
        text = await response.text()

        soup = BS(text, 'lxml')
        if soup.find("a", {"class": "loginLink"}):
            return False
    return True
