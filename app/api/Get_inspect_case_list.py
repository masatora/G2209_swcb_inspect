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
              案由, 時間, 會勘單位與人員, 土地基本資料, 行為人基本資料, 違規類別, 輔導類別, 各單位意見, 行為人意見, 行為人簽名, 會勘結論, 現場照片, 散會, 填寫人,
              TO_CHAR(修改時間, 'YYYY-MM-DD HH24:MI') AS 更新時間,
              TO_CHAR(建立時間, 'YYYY-MM-DD HH24:MI') AS 案件時間
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
