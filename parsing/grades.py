import json
import aiohttp
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
from parsing.login import login_user
from structure.constant.template import grade_data_template
from structure.constant.url import MAIN_URL


async def parse_grades(username: str, password: str):
    HEADERS = {'User-Agent': UserAgent().random}

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        await login_user(username, password, session)
        grade_data = grade_data_template.copy()
        async with session.post(MAIN_URL, data=grade_data, ssl=False) as grade_response:
            grade_content = await grade_response.text(encoding='utf-8-sig')
            parsed_data = json.loads(grade_content)

            value_of_data = parsed_data.get('DATA')
            soup = BS(value_of_data, "lxml")
            csrows = soup.find_all('tr', {"class": "csrow"})

            grades = []
            for csrow in csrows:
                tds = csrow.find_all("td")
                row = [cell.text.strip() for cell in tds]
                row[6] = row[6] if row[6] else 'None'
                row[5] = row[5] if row[5].isdigit() else 'None'
                absense = row[4].split('\xa0')[0]
                need = [row[0], absense, row[5], row[6]]
                grades.append(need)

            return grades

