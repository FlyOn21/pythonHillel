# Вашей задачей будет создать сервер агрегатор (он выполнит несколько запросов на адреса сторонних сайтов).
# Количество сайтов и сами сайты на которые вы будете слать реквесты вы определяете сами (вот например по ссылке
# ниже найдете список популярных ресурсов, но, как правило, они требуют регистрации, после чего они предоставят
# вам что-то типа ключа с которым вы сможете запросить информацию)
#
# 1) Познакомиться с фреймворком AIOHTTP (https://docs.aiohttp.org/en/stable/).
#
# 2)Создать сервер который мог бы принимать GET запросы на адрес (http://localhost/collect_info)
#
# 3) В ответе должна быть агрегирована информация полученная от сторонних ресурсов.

import datetime
import os
from config import API_KEY
import aiohttp_jinja2
import jinja2
from aiohttp import web, ClientSession



routes = web.RouteTableDef()


@routes.get("/")
async def main(request: web.Request):
    context = {
        'current_date': datetime.date.today()
    }
    response = aiohttp_jinja2.render_template("index.html", request,
                                              context=context)
    return response



@routes.get("/collect_info")
async def collect_info(request: web.Request):
    async with ClientSession() as session:
        covid_19_data = await covid_19("https://covid-19-data.p.rapidapi.com/totals", session)
        weather_data = await weather("https://community-open-weather-map.p.rapidapi.com/weather", session)
    context = {
        "weather": weather_data,
        "covid": covid_19_data,
        "current_date": datetime.date.today()
    }
    response = aiohttp_jinja2.render_template("collect_info.html", request,
                                              context=context)
    return response


async def covid_19(url, session):
    params = {"format": "json"}
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
    }
    response = await session.get(url, params=params, headers=headers)
    if response.status == 200:
        covid_19_info = await response.json()
        print(covid_19_info)
        return covid_19_info[0]
    return False


async def weather(url, session):
    params = {"q": "Kiev", "lang": "ru", "units": "metric", "mode": "json"}

    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    }
    response = await session.get(url, params=params, headers=headers)

    if response.status == 200:
        weather_info = await response.json()
        print(weather_info)
        return weather_info
    return False


app = web.Application()
aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates"))
)
app.add_routes(routes)

if __name__ == "__main__":
    web.run_app(app, host="localhost", port=2000)
