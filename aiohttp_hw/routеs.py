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
import asyncio
import datetime
from config import API_KEY
import aiohttp_jinja2
from aiohttp import web, ClientSession

routes = web.RouteTableDef()  # A route definition used to describe routes by decorators.


@routes.get("/")
async def main(request: web.Request):
    """index.html route"""
    context = {}
    response = aiohttp_jinja2.render_template("index.html", request,
                                              context=context)
    return response


@routes.get("/collect_info")
async def collect_info(request: web.Request, city="Kiev"):
    """Function collects information from the specified resources
    and generates a response page for the collect_info endpoint"""

    async with ClientSession() as session:
        data_for_tasks = [(covid_19("https://covid-19-data.p.rapidapi.com/totals", session)),
                          (weather("https://community-open-weather-map.p.rapidapi.com/weather", session, city=city))]
        tasks = []
        for task in data_for_tasks:
            task = asyncio.create_task(task)
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        print(results)
    context = {
        "weather": results[1],
        "covid": results[0],
        "current_date": datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
    }
    response = aiohttp_jinja2.render_template("collect_info.html", request,
                                              context=context)
    return response


@routes.post("/collect_info")
async def city_weather(request: web.Request):
    """Endpoint processes a post request from the form to get the weather for the specified city"""
    data = await request.post()
    current_city = data["city"]
    return await collect_info(request, city=current_city)



async def covid_19(url, session):
    """Function sends a request to obtain information about the
    incidence statistics of covid and returns a data dictionary or False"""
    params = {"format": "json"}
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
    }
    response = await session.get(url, params=params, headers=headers)
    if response.status == 200:
        covid_19_info = await response.json()
        return covid_19_info[0]
    return False


async def weather(url, session, city):
    """Function sends a request to obtain information about the
    weather in current city and returns a data dictionary or False"""
    params = {"q": city, "lang": "ru", "units": "metric", "mode": "json"}
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    }
    response = await session.get(url, params=params, headers=headers)
    if response.status == 200:
        weather_info = await response.json()
        return weather_info
    return False
