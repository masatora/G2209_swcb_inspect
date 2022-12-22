from __init__ import web
from sanic.views import HTTPMethodView
from sanic.response import text, json
from psycopg2 import connect, DatabaseError
from psycopg2.extras import RealDictCursor
from json import loads
from os.path import exists, join

class Get_xml_file(HTTPMethodView):
  async def post(self, request):
    try:
      resp = {}
      case_id = request.json.get('caseId')
      file_name = request.json.get('fileName')
      assert type(case_id) is int and case_id > 0, '案件編號格式錯誤'
      assert type(file_name) is str and file_name != '', '檔名格式錯誤'

      with connect(**loads(web.config['DATABASE_CONFIG_INSPECT'])) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
          cursor.execute('''
            SELECT
              案由, 違規類別, 輔導類別, 各單位意見, 行為人意見, 會勘結論, 填寫人,
              會勘單位與人員 ->> '本市區公所' AS 本市區公所, 會勘單位與人員 ->> '本府局處' AS 本府局處, 會勘單位與人員 ->> '本府地政事務所' AS 本府地政事務所, 會勘單位與人員 ->> '本府警察局' AS 本府警察局, 會勘單位與人員 ->> '本府違章建築拆除大隊' AS 本府違章建築拆除大隊, 會勘單位與人員 ->> '其他1' AS 其他1, 會勘單位與人員 ->> '其他2' AS 其他2,
              土地基本資料 ->> 'TWD97_X' AS "TWD97_X", 土地基本資料 ->> 'TWD97_Y' AS "TWD97_Y", 土地基本資料 ->> '行政區' AS 行政區, 土地基本資料 ->> '地段' AS 地段, 土地基本資料 ->> '小段' AS 小段, 土地基本資料 ->> '地號' AS 地號, 土地基本資料 ->> '使用面積' AS 使用面積, 土地基本資料 ->> '所有權人' AS 所有權人,
              行為人基本資料 ->> '行為人姓名' AS 行為人姓名, 行為人基本資料 ->> '行為人出生年月日' AS 行為人出生年月日, 行為人基本資料 ->> '行為人身分證' AS 行為人身分證, 行為人基本資料 ->> '行為人電話' AS 行為人電話, 行為人基本資料 ->> '行為人住址' AS 行為人住址,
              TO_CHAR(時間, 'YYYY年MM月DD日 HH24時MI分') AS 時間,
              TO_CHAR(散會, 'YYYY年MM月DD日 HH24時MI分') AS 散會,
              TO_CHAR(修改時間, 'YYYY年MM月DD日 HH24時MI分') AS 修改時間,
              TO_CHAR(建立時間, 'YYYY年MM月DD日 HH24時MI分') AS 建立時間
            FROM hillside_inspect
            WHERE 案件編號 = %(case_id)s
          ''', {
            'case_id': case_id
          })
          assert cursor.rowcount == 1, '無法取得案件資料'
          row = cursor.fetchone()

      filepath = join(web.config['STATIC_PATH'], 'xml', file_name +'.xml')
      assert exists(filepath), '檔案不存在'

      with open(filepath, encoding="utf-8") as xml:
        xml_content = xml.read().format(args={
          '案由': row['案由'],
          '違規類別': row['違規類別'],
          '輔導類別': row['輔導類別'],
          '各單位意見': row['各單位意見'],
          '行為人意見': row['行為人意見'],
          '會勘結論': row['會勘結論'],
          '填寫人': row['填寫人'],
          '行政區': row['行政區'],
          '地段': row['地段'],
          '小段': row['小段'],
          '地號': row['地號'],
          'TWD97_X': row['TWD97_X'],
          'TWD97_Y': row['TWD97_Y'],
          '區公所': row['本市區公所'],
          '本府局處': row['本府局處'],
          '本府地政事務所': row['本府地政事務所'],
          '本府警察局': row['本府警察局'],
          '本府違章建築拆除大隊': row['本府違章建築拆除大隊'],
          '其他1': row['其他1'],
          '其他2': row['其他1'],
          '使用面積': row['使用面積'],
          '所有權人': row['所有權人'],
          '行為人姓名': row['行為人姓名'],
          '行為人出生年月日': row['行為人出生年月日'],
          '行為人身分證': row['行為人身分證'],
          '行為人電話': row['行為人電話'],
          '行為人住址': row['行為人住址'],
          '時間': row['時間'],
          '散會': row['散會'],
          '修改時間': row['修改時間'],
          '建立時間': row['建立時間']
        })
    except AssertionError as e:
      err_str = str(e)
      resp = { 'status': 'fail', 'msg': err_str }
    except DatabaseError as e:
      err_str = str(e)
      resp = { 'status': 'fail', 'msg': err_str }
    except Exception as e:
      err_str = str(e)
      resp = { 'status': 'fail', 'msg': '取得案件資料暫時無法服務' }
    finally:
      if 'err_str' in locals():
        if web.config['DEBUG']:
          print(err_str)

      if len(resp) > 0:
        return json(resp, ensure_ascii=False)
      else:
        return text(xml_content, content_type="application/xml")
