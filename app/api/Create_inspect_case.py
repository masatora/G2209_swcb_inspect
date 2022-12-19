from __init__ import web
from sanic.views import HTTPMethodView
from sanic.response import json
from psycopg2 import connect, DatabaseError
from datetime import datetime
from json import loads, dumps

class Create_inspect_case(HTTPMethodView):
  async def post(self, request):
    try:
      resp = {}
      for i in request.form:
        print(i)

      # with connect(**loads(web.config['DATABASE_CONFIG_INSPECT'])) as conn:
      #   with conn.cursor() as cursor:
      #     cursor.excute('''
      #       INSERT INTO hillside_inspect (
      #         案由, 時間, 會勘單位與人員, 土地基本資料, 行為人基本資料, 違規類別, 輔導類別, 各單位意見, 請行為人陳述意見, 會勘結論, 現場照片, 散會, 修改時間, 建立時間
      #       ) VALUES (
      #         %(案由)s, %(時間)s, %(會勘單位與人員)s, %(土地基本資料)s, %(行為人基本資料)s, %(違規類別)s, %(輔導類別)s, %(各單位意見)s, %(請行為人陳述意見)s, %(會勘結論)s, %(現場照片)s, %(散會)s, %(修改時間)s, %(建立時間)s
      #       )
      #     ''', {
      #       '案由': '',
      #       '時間': '',
      #       '會勘單位與人員': '',
      #       '土地基本資料': '',
      #       '行為人基本資料': '',
      #       '違規類別': '',
      #       '輔導類別': '',
      #       '各單位意見': '',
      #       '請行為人陳述意見': '',
      #       '會勘結論': '',
      #       '現場照片': '',
      #       '散會': '',
      #       '修改時間': '',
      #       '建立時間': ''
      #     })
      #     assert cursor.rowcount == 1, ''
    except AssertionError as e:
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
