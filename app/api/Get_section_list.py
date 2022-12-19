from __init__ import web
from sanic.views import HTTPMethodView
from sanic.response import json
import requests

class Get_section_list(HTTPMethodView):
  async def get(self, request):
    try:
      resp = {}

      district = request.args.get('district')
      assert type(district) is not None and district != '', '缺少必要參數'

      r = requests.get('https://www.ntpcswc.ntpc.gov.tw/ntpcagr-api/get_sectionList/' + district)
      assert r.status_code == 200 and r.text != '', '無法取得地段資料'
      section_list = r.json()

      resp = { 'status': 'success', 'msg': '取得地段地籍資料成功', 'row': section_list }
    except AssertionError as e:
      err_str = str(e)
      resp = { 'status': 'fail', 'msg': err_str }
    except requests.ConnectionError as e:
      err_str = str(e)
      resp = { 'status': 'fail', 'msg': err_str }
    except Exception as e:
      err_str = str(e)
      resp = { 'status': 'fail', 'msg': '新增水土保持案件 API 暫時無法服務' }
    finally:
      if 'err_str' in locals():
        if web.config['DEBUG']:
          print(err_str)

      return json(resp, ensure_ascii=False)
