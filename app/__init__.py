from sanic import Sanic
from sanic_ext import Extend

web = Sanic(__name__)

import config
import api

Extend(web)

# print(web.router.routes_all)
