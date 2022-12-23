from __init__ import web
from sanic.views import HTTPMethodView
from sanic.response import json
from psycopg2 import connect, DatabaseError
from datetime import datetime
from json import loads

class Update_perpetrator_sign(HTTPMethodView):
  async def post(self, request):
    try:
      assert request.content_type.find('multipart/form-data') != -1, '無法處理的 request'
      assert len(request.form) > 0, '參數錯誤'

      resp = {}
      case_id = request.form.get('caseId')
      perpetrator_sign = request.form.get('perpetratorSign')
      print(case_id)
      assert type(case_id) is str and int(case_id) > 0, '案件編號格式錯誤'

      with connect(**loads(web.config['DATABASE_CONFIG_INSPECT'])) as conn:
        with conn.cursor() as cursor:
          now = datetime.now()
          cursor.execute('''
            UPDATE hillside_inspect
            SET 行為人簽名 = %(行為人簽名)s, 修改時間 = %(修改時間)s
            WHERE 案件編號 = %(案件編號)s
          ''', {
            '案件編號': case_id,
            '行為人簽名': perpetrator_sign,
            '修改時間': now,
          })
          assert cursor.rowcount == 1, '更新行為人簽名失敗'

      resp = { 'status': 'success', 'msg': '更新行為人簽名成功' }
    except AssertionError as e:
      err_str = str(e)
      resp = { 'status': 'fail', 'msg': err_str }
    except DatabaseError as e:
      err_str = str(e)
      resp = { 'status': 'fail', 'msg': err_str }
    except Exception as e:
      err_str = str(e)
      resp = { 'status': 'fail', 'msg': '更新行為人簽名 API 暫時無法服務' }
    finally:
      if 'err_str' in locals():
        if web.config['DEBUG']:
          print(err_str)

      return json(resp, ensure_ascii=False)
