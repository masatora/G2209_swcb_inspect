from __init__ import web
from sanic.views import HTTPMethodView
from sanic.response import json
from psycopg2 import connect, DatabaseError
from psycopg2.extras import RealDictCursor
from datetime import datetime
from json import loads, dumps
from re import sub

class Get_inspect_case_list(HTTPMethodView):
  async def get(self, request):
    try:
      resp = {}
      with connect(**loads(web.config['DATABASE_CONFIG_INSPECT'])) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
          cursor.execute('''
            SELECT
              案件編號, 案由, 行為人簽名, 填寫人,
              土地基本資料 ->> '行政區' AS 行政區,
              行為人基本資料 ->> '行為人姓名' AS 行為人姓名,
              TO_CHAR(時間, 'YYYY-MM-DD HH24:MI') AS 案件時間,
              TO_CHAR(修改時間, 'YYYY-MM-DD HH24:MI') AS 更新時間
            FROM hillside_inspect
            ORDER BY 建立時間 DESC, 修改時間 DESC, 案件編號 DESC
          ''')
          assert cursor.rowcount > 0, '無相關會勘紀錄表資料'
          row = cursor.fetchall()

      resp = { 'status': 'success', 'msg': 'OK', 'row': row }
    except AssertionError as e:
      err_str = str(e)
      resp = { 'status': 'fail', 'msg': err_str }
    except DatabaseError as e:
      err_str = str(e)
      resp = { 'status': 'fail', 'msg': err_str }
    except Exception as e:
      err_str = str(e)
      resp = { 'status': 'fail', 'msg': '取得會勘紀錄表 API 暫時無法服務' }
    finally:
      if 'err_str' in locals():
        if web.config['DEBUG']:
          print(err_str)

      return json(resp, ensure_ascii=False)
