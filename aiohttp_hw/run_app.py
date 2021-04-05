import asyncio
import os
import aiohttp_jinja2
import jinja2
from aiohttp import web
import uvloop
from routеs import routes
import click

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())  # Third party library that replaces the default event
                                                         # loop with the faster one from the uvloop library


def create_app():
    """Create app"""
    app = web.Application()
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates"))
    )
    app.add_routes(routes)
    return app

@click.command()
@click.option("--host","-h", help = "Host start server", default= "localhost") #creat flag host for command line
@click.option("--port", "-p", help="Number of port for server", default = 8000) #creat flag port for command line
# for example command start app server: python3 run_app.py --host 0.0.0.0 --port 8090
# or python3 run_app.py -h 0.0.0.0 -p 8090
def run_app(host, port):
    """Function start app server"""
    return web.run_app(create_app(), host = host, port = port)


if __name__ == "__main__":
    run_app()
