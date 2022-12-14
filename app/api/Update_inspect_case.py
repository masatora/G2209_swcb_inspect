from __init__ import web
from sanic.views import HTTPMethodView
from sanic.response import json
from psycopg2 import connect, DatabaseError
from datetime import datetime
from json import loads, dumps
from re import sub
from distutils.util import strtobool

class Update_inspect_case(HTTPMethodView):
  async def post(self, request):
    try:
      assert request.content_type.find('multipart/form-data') != -1, '無法處理的 request'
      assert len(request.form) > 0, '參數錯誤'

      resp = {}
      data = {
        '案由': '',
        '時間': '',
        '本市區公所': '',
        '本市區公所簽名': [],
        '本府局處1': '',
        '本府局處1簽名': [],
        '本府局處2': '',
        '本府局處2簽名': [],
        '本府局處3': '',
        '本府局處3簽名': [],
        '本府地政事務所': '',
        '本府地政事務所簽名': [],
        '本府警察局': '',
        '本府警察局簽名': [],
        '本府違章建築拆除大隊': '',
        '本府違章建築拆除大隊簽名': [],
        '其他1': '',
        '其他1簽名': [],
        '其他2': '',
        '其他2簽名': [],
        'TWD97_X': '',
        'TWD97_Y': '',
        '行政區': '',
        '地段': '',
        '小段': '',
        '地號': '',
        '使用面積': '',
        '所有權人': '',
        '行為人姓名': '',
        '行為人出生年月日': '',
        '行為人身分證': '',
        '行為人電話': '',
        '行為人住址': '',
        '違規類別': [],
        '輔導類別': '',
        '各單位意見': '',
        '行為人意見': '',
        '會勘結論': [],
        '現場照片': [],
        '散會': '',
        '行為人簽名': []
      }

      case_id = request.form.get('案件編號')
      assert type(case_id) is str and int(case_id) > 0, '案件編號格式錯誤'

      for (key, value) in request.form.items():
        if key != '案件編號':
          k = sub('\[\d\]', '', key)
          if k in ['本市區公所簽名', '本府局處1簽名', '本府局處2簽名', '本府局處3簽名', '本府地政事務所簽名', '本府警察局簽名', '本府違章建築拆除大隊簽名', '其他1簽名', '其他2簽名', '違規類別', '會勘結論', '現場照片', '行為人簽名']:
            data[k].append(value[0])
          else:
            if key not in ['本市區公所', '本府局處2', '本府局處3', '本府地政事務所', '本府警察局', '本府違章建築拆除大隊', '其他1', '其他2', '其他違規項目', '其他會勘結論']:
              assert type(value[0]) and value[0] != '', key + '不可為空值'
            data[k] = value[0]

      with connect(**loads(web.config['DATABASE_CONFIG_INSPECT'])) as conn:
        with conn.cursor() as cursor:
          now = datetime.now()
          cursor.execute('''
            UPDATE hillside_inspect
            SET 案由 = %(案由)s, 時間 = %(時間)s, 會勘單位與人員 = %(會勘單位與人員)s, 土地基本資料 = %(土地基本資料)s, 行為人基本資料 = %(行為人基本資料)s, 違規類別 = %(違規類別)s, 輔導類別 = %(輔導類別)s,
                各單位意見 = %(各單位意見)s, 行為人意見 = %(行為人意見)s, 會勘結論 = %(會勘結論)s, 現場照片 = %(現場照片)s, 散會 = %(散會)s, 修改時間 = %(修改時間)s
            WHERE 案件編號 = %(案件編號)s
          ''', {
            '案件編號': case_id,
            '案由': data['案由'],
            '時間': data['時間'],
            '會勘單位與人員': dumps({
              '本市區公所': data['本市區公所'],
              '本市區公所簽名': data['本市區公所簽名'],
              '本府局處1': data['本府局處1'],
              '本府局處1簽名': data['本府局處1簽名'],
              '本府局處2': data['本府局處2'],
              '本府局處2簽名': data['本府局處2簽名'],
              '本府局處3': data['本府局處3'],
              '本府局處3簽名': data['本府局處3簽名'],
              '本府地政事務所': data['本府地政事務所'],
              '本府地政事務所簽名': data['本府地政事務所簽名'],
              '本府警察局': data['本府警察局'],
              '本府警察局簽名': data['本府警察局簽名'],
              '本府違章建築拆除大隊': data['本府違章建築拆除大隊'],
              '本府違章建築拆除大隊簽名': data['本府違章建築拆除大隊簽名'],
              '其他1': data['其他1'],
              '其他1簽名': data['其他1簽名'],
              '其他2': data['其他2'],
              '其他2簽名': data['其他2簽名']
            }),
            '土地基本資料': dumps({
              'TWD97_X': data['TWD97_X'],
              'TWD97_Y': data['TWD97_Y'],
              '行政區': data['行政區'],
              '地段': data['地段'],
              '小段': data['小段'],
              '地號': data['地號'],
              '使用面積': data['使用面積'],
              '所有權人': data['所有權人']
            }),
            '行為人基本資料': dumps({
              '行為人姓名': data['行為人姓名'],
              '行為人出生年月日': data['行為人出生年月日'],
              '行為人身分證': data['行為人身分證'],
              '行為人電話': data['行為人電話'],
              '行為人住址': data['行為人住址'],
              '行為人簽名': data['行為人簽名']
            }),
            '違規類別': data['違規類別'],
            '輔導類別': True if strtobool(data['輔導類別']) else False,
            '各單位意見': data['各單位意見'],
            '行為人意見': data['行為人意見'],
            '會勘結論': data['會勘結論'],
            '現場照片': data['現場照片'],
            '散會': data['散會'],
            '修改時間': now,
          })
          assert cursor.rowcount == 1, '修改會勘紀錄表失敗'

      resp = { 'status': 'success', 'msg': '修改會勘紀錄表成功' }
    except AssertionError as e:
      err_str = str(e)
      resp = { 'status': 'fail', 'msg': err_str }
    except DatabaseError as e:
      err_str = str(e)
      resp = { 'status': 'fail', 'msg': '資料庫連線錯誤' }
    except Exception as e:
      err_str = str(e)
      resp = { 'status': 'fail', 'msg': '修改會勘紀錄表 API 暫時無法服務' }
    finally:
      if 'err_str' in locals():
        if web.config['DEBUG']:
          print(err_str)

      return json(resp, ensure_ascii=False)
