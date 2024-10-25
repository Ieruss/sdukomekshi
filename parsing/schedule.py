import sys
import aiohttp
import asyncio
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
from parsing.login import login_user
from structure.constant.other import get_day_of_week
from structure.constant.template import schedule_data_template
from structure.constant.url import MAIN_URL



async def parse_schedule(username, password) -> str:
    arr = []
    schedule_datas = schedule_data_template.copy()
    HEADERS = {'User-Agent': UserAgent().random}
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        await login_user(username=username, password=password, session=session)

        async with session.post(MAIN_URL, data=schedule_datas, ssl=False) as response:
            schedule = await response.text()
            soup = BS(schedule, 'lxml')

            table = soup.find('table', attrs={'class': 'clTbl'})
            trs = table.find_all('tr')
            for i in range(1, len(trs) - 4):
                tr = trs[i]
                tds = tr.find_all('td')
                time = tds[0].find('span').text
                for j in range(1, len(tds)):
                    td = tds[j]
                    if len(td) == 1:
                        continue
                    lessons = td.find_all('a')
                    locations = td.find_all('span', title=True)
                    for z in range(len(lessons)):
                        lesson = lessons[z].text.replace(" ", "")
                        location = locations[z*2+1].text.replace(" ", "")
                        arr.append([time, get_day_of_week(j), lesson, location])

    return arr
