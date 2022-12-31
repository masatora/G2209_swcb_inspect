from __init__ import web
from sanic.views import HTTPMethodView
from sanic.response import file, json
from psycopg2 import connect, DatabaseError
from psycopg2.extras import RealDictCursor
from json import loads
from pdfkit import from_string
from os.path import join

class Get_inspect_case_pdf(HTTPMethodView):
  def __init__(self):
    self.violate_type = {
      '探礦、採礦、鑿青、採取土石、設置有關附屬設施': 1,
      '修建鐵路、公路、其他道路、溝渠': 2,
      '開發建築用地': 3,
      '設置公園': 4,
      '設置墳墓': 5,
      '設置遊憩用地': 6,
      '設置運動場地': 7,
      '設置軍事訓練場': 8,
      '堆積土石': 9,
      '處理廢棄物': 10,
      '其他開挖整地': 11,
      '修築農路或整坡作業': 12,
      '超限利用': 13
    }
    self.inspect_result = {
      '不當使用山坡地部份依據水土保持法相關法規辦理。': 1,
      '涉違反其他法令部份，請各有關單位逕依權責卓處。': 2,
      '現場立即停工。並作妥相關防災措施（現場如未停工，將施以連續處分。另如有裸露地應配合草蓆或塑膠布覆蓋以防止表土流失）。': 3,
      '已致生水土流失或毀損水土保持之處理與維護設施。': 4,
      '請依水土保持服務團輔導事項辦理。': 5,
      '其他。': 6
    }

  async def post(self, request):
    try:
      # assert request.content_type.find('multipart/form-data') != -1, '無法處理的 request'

      resp = {}
      case_id = request.form.get('caseId')
      assert type(case_id) is str and int(case_id) > 0, '案件編號格式錯誤'

      with connect(**loads(web.config['DATABASE_CONFIG_INSPECT'])) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
          cursor.execute('''
            SELECT
              案由, 會勘單位與人員, 土地基本資料, 行為人基本資料, 違規類別, 輔導類別, 各單位意見, 行為人意見, 會勘結論, 散會, 現場照片,
              TO_CHAR(時間, 'YYYY-MM-DD HH24:MI') AS 時間,
              TO_CHAR(散會, 'YYYY-MM-DD HH24:MI') AS 散會
            FROM hillside_inspect
            WHERE 案件編號 = %(case_id)s
          ''', {
            'case_id': case_id
          })
          assert cursor.rowcount > 0, '無相關會勘紀錄表資料'
          row = cursor.fetchone()

      file_name = '違規使用山坡地案件現場會勘紀錄表'
      filepath = join(web.config['STATIC_PATH'], file_name +'.pdf')
      with open(join(web.config['STATIC_PATH'], file_name +'.html'), encoding="utf-8") as html:
        violate_string, violate_arr = self.gen_data_list('violate', row['違規類別'])
        inspect_string, inspect_arr = self.gen_data_list('inspect', row['會勘結論'])
        from_string(html.read().format(args={
          '案由': row['案由'],
          '時間': row['時間'],
          '本市區公所': row['會勘單位與人員']['本市區公所'],
          '本市區公所簽名': self.gen_sign_img(row['會勘單位與人員']['本市區公所簽名']),
          '本府局處1': row['會勘單位與人員']['本府局處1'],
          '本府局處1簽名': self.gen_sign_img(row['會勘單位與人員']['本府局處1簽名']),
          '本府局處2': '  局' if row['會勘單位與人員']['本府局處2'] == '' else row['會勘單位與人員']['本府局處2'],
          '本府局處2簽名': self.gen_sign_img(row['會勘單位與人員']['本府局處2簽名']),
          '本府局處3': '  局' if row['會勘單位與人員']['本府局處3'] == '' else row['會勘單位與人員']['本府局處3'],
          '本府局處3簽名': self.gen_sign_img(row['會勘單位與人員']['本府局處3簽名']),
          '本府地政事務所': row['會勘單位與人員']['本府地政事務所'],
          '本府地政事務所簽名': self.gen_sign_img(row['會勘單位與人員']['本府地政事務所簽名']),
          '本府警察局': row['會勘單位與人員']['本府警察局'],
          '本府警察局簽名': self.gen_sign_img(row['會勘單位與人員']['本府警察局簽名']),
          '本府違章建築拆除大隊': row['會勘單位與人員']['本府違章建築拆除大隊'],
          '本府違章建築拆除大隊簽名': self.gen_sign_img(row['會勘單位與人員']['本府違章建築拆除大隊']),
          '其他1': '' if row['會勘單位與人員'].get('其他1') is None else row['會勘單位與人員']['其他1'],
          '其他1簽名': '' if row['會勘單位與人員'].get('其他1簽名') is None else self.gen_sign_img(row['會勘單位與人員']['其他1簽名']),
          '其他2': '' if row['會勘單位與人員'].get('其他2') is None else row['會勘單位與人員']['其他2'],
          '其他2簽名': '' if row['會勘單位與人員'].get('其他2簽名') is None else self.gen_sign_img(row['會勘單位與人員']['其他2簽名']),
          'TWD97_X': row['土地基本資料']['TWD97_X'],
          'TWD97_Y': row['土地基本資料']['TWD97_Y'],
          '行政區': row['土地基本資料']['行政區'],
          '地段': row['土地基本資料']['地段'],
          '小段': row['土地基本資料']['小段'],
          '地號': row['土地基本資料']['地號'],
          '使用面積': row['土地基本資料']['使用面積'],
          '所有權人': row['土地基本資料']['所有權人'],
          '行為人姓名': row['行為人基本資料']['行為人姓名'],
          '行為人出生年月日': row['行為人基本資料']['行為人出生年月日'],
          '行為人身分證': row['行為人基本資料']['行為人身分證'],
          '行為人電話': row['行為人基本資料']['行為人電話'],
          '行為人住址': row['行為人基本資料']['行為人住址'],
          '行為人簽名': self.gen_sign_img(row['行為人基本資料']['行為人簽名']),
          '違規類別編號': violate_string,
          '違規類別編號1': '✓' if 1 in violate_arr else '',
          '違規類別編號2': '✓' if 2 in violate_arr else '',
          '違規類別編號3': '✓' if 3 in violate_arr else '',
          '違規類別編號4': '✓' if 4 in violate_arr else '',
          '違規類別編號5': '✓' if 5 in violate_arr else '',
          '違規類別編號6': '✓' if 6 in violate_arr else '',
          '違規類別編號7': '✓' if 7 in violate_arr else '',
          '違規類別編號8': '✓' if 8 in violate_arr else '',
          '違規類別編號9': '✓' if 9 in violate_arr else '',
          '違規類別編號10': '✓' if 10 in violate_arr else '',
          '違規類別編號11': '✓' if 11 in violate_arr else '',
          '違規類別編號12': '✓' if 12 in violate_arr else '',
          '違規類別編號13': '✓' if 13 in violate_arr else '',
          '會勘結論編號': inspect_string,
          '會勘結論編號1': '✓' if 1 in inspect_arr else '',
          '會勘結論編號2': '✓' if 2 in inspect_arr else '',
          '會勘結論編號3': '✓' if 3 in inspect_arr else '',
          '會勘結論編號4': '✓' if 4 in inspect_arr else '',
          '會勘結論編號5': '✓' if 5 in inspect_arr else '',
          '輔導類別': '☑' if row['輔導類別'] == True else '☒',
          '各單位意見': row['各單位意見'],
          '行為人意見': row['行為人意見'],
          '散會': row['散會']
        }), filepath, options = { 'encoding': 'utf-8' })
    except DatabaseError as e:
      err_str = str(e)
      resp = { 'status': 'fail', 'msg': '資料庫連線錯誤' }
    except Exception as e:
      err_str = str(e)
      resp = { 'status': 'fail', 'msg': '取得會勘紀錄表暫時無法服務' }
    finally:
      if 'err_str' in locals():
        if web.config['DEBUG']:
          print(err_str)

      if len(resp) > 0:
        return json(resp, ensure_ascii=False)
      else:
        return await file(filepath, mime_type="application/pdf")


  def gen_sign_img(self, data):
    result = ''

    if type(data) is list and len(data) > 0:
      for i in data:
        result += f'<img src="{i}" width="110" />'

    return result

  def gen_data_list(self, data_type, data):
    result = ['', []]

    if data_type == 'violate':
      for i in data:
        result[0] += f'【 {self.violate_type[i]} 】'
        result[1].append(self.violate_type[i])
    else:
      for i in data:
        result[0] += f'【 {self.inspect_result[i]} 】'
        result[1].append(self.inspect_result[i])

    return result
