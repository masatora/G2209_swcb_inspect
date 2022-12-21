from __init__ import web
from sanic.views import HTTPMethodView
from sanic.response import json
import requests

class Get_region(HTTPMethodView):
  async def get(self, request):
    try:
      resp = {}

      r = requests.get('https://www.ntpcswc.ntpc.gov.tw/ntpcagr-api/get_region')
      assert r.status_code == 200 and r.text != '', '無法取得行政區地籍資料'

      resp = { 'status': 'success', 'msg': '取得行政區地籍資料成功', 'row': r.json() }
    except AssertionError as e:
      err_str = str(e)
      resp = { 'status': 'fail', 'msg': err_str }
    except requests.ConnectionError as e:
      err_str = str(e)
      resp = { 'status': 'fail', 'msg': err_str }
    except Exception as e:
      err_str = str(e)
      resp = { 'status': 'fail', 'msg': '取得行政區地籍 API 暫時無法服務' }
    finally:
      if 'err_str' in locals():
        if web.config['DEBUG']:
          print(err_str)

      return json(resp, ensure_ascii=False)
