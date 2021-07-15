from aiohttp import web
import json

from aiohttp.web_response import Response

app = web.Application()
routes = web.RouteTableDef()


@routes.get('/')
async def handle(request: web.Request) -> web.Response:
    response_obj = { 'status' : 'success' }
    return web.Response(text=json.dumps(response_obj))

@routes.post('/user')
async def new_user(request: web.Request) -> web.Response:
    try:
        ## happy path where name is set
        user = request.query['name']
        ## Process our new user
        print("Creating new user with name: " , user)

        response_obj = { 'status' : 'success' }
        ## return a success json response with status code 200 i.e. 'OK'
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        ## Bad path where name is not set
        response_obj = { 'status' : 'failed', 'reason': str(e) }
        ## return failed with a status code of 500 i.e. 'Server Error'
        return web.Response(text=json.dumps(response_obj), status=500)

"""
async def greet_user(request: web.Request) -> web.Response:
    user = request.match_info.get("username", "")
    if (pagenum := request.rel_url.query.get("page", "")) == "": pagenum = "1"
    return web.Response(text=f"Hello, {user} {pagenum}")
"""


app.add_routes(routes)
web.run_app(app)

