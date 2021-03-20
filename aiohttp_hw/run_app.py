import asyncio
import os
import aiohttp_jinja2
import jinja2
from aiohttp import web
import uvloop
from routs import routes

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def create_app():
    app = web.Application()
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates"))
    )
    app.add_routes(routes)
    return app

if __name__ == "__main__":
    web.run_app(create_app(), host="localhost",port=8000)