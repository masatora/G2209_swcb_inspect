export const attendees = [
  { name: '本市區公所', type: 'select', label: '請選擇本市區公所', data: ['無', '板橋區', '中和區', '新莊區', '土城區', '汐止區', '鶯歌區', '淡水區', '五股區', '林口區', '深坑區', '坪林區', '石門區', '萬里區', '雙溪區', '烏來區', '三重區', '永和區', '新店區', '蘆洲區', '樹林區', '三峽區', '瑞芳區', '泰山區', '八里區', '石碇區', '三芝區', '金山區', '平溪區'] },
  { name: '本府局處1', type: 'select', label: '請選擇本府局處', data: ['無', '秘書處', '民政局', '財政局', '教育局', '經濟發展局', '工務局', '水利局', '農業局', '城鄉發展局', '社會局', '地政局', '勞工局', '交通局', '觀光旅遊局', '法制局', '警察局', '衛生局', '環境保護局', '消防局', '文化局', '原住民族行政局', '新聞局', '人事處', '主計處', '政風處', '研究發展考核委員會', '客家事務局', '捷運工程局', '青年局'] },
  { name: '本府局處2', type: 'select', label: '請選擇本府局處', data: ['無', '秘書處', '民政局', '財政局', '教育局', '經濟發展局', '工務局', '水利局', '農業局', '城鄉發展局', '社會局', '地政局', '勞工局', '交通局', '觀光旅遊局', '法制局', '警察局', '衛生局', '環境保護局', '消防局', '文化局', '原住民族行政局', '新聞局', '人事處', '主計處', '政風處', '研究發展考核委員會', '客家事務局', '捷運工程局', '青年局'] },
  { name: '本府局處3', type: 'select', label: '請選擇本府局處', data: ['無', '秘書處', '民政局', '財政局', '教育局', '經濟發展局', '工務局', '水利局', '農業局', '城鄉發展局', '社會局', '地政局', '勞工局', '交通局', '觀光旅遊局', '法制局', '警察局', '衛生局', '環境保護局', '消防局', '文化局', '原住民族行政局', '新聞局', '人事處', '主計處', '政風處', '研究發展考核委員會', '客家事務局', '捷運工程局', '青年局'] },
  { name: '本府地政事務所', type: 'select', label: '請選擇地政事務所', data: ['無', '板橋地政事務所', '三重地政事務所', '中和地政事務所', '新莊地政事務所', '新店地政事務所', '樹林地政事務所', '淡水地政事務所', '汐止地政事務所', '瑞芳地政事務所'] },
  { name: '本府警察局', type: 'select', label: '請選擇本府警察局', data: ['無', '刑事警察大隊', '交通警察大隊', '保安警察大隊', '少年警察隊', '婦幼警察隊', '板橋分局', '海山分局', '三重分局', '新莊分局', '中和分局', '永和分局', '新店分局', '蘆洲分局', '土城分局', '樹林分局', '三峽分局', '淡水分局', '汐止分局', '金山分局', '瑞芳分局', '林口分局'] },
  { name: '本府違章建築拆除大隊', type: 'select', label: '請選擇本府違章建築拆除大隊', data: ['無', '新北市違章建築拆除大隊'] },
  { name: '其他1', type: 'input', label: '請輸入其他單位' },
  { name: '其他2', type: 'input', label: '請輸入其他單位' }
]
export const info = [
  { name: '行政區', type: 'select_district', label: '請選擇行政區' },
  { name: '地段', type: 'select', label: '請選擇地段' },
  { name: '小段', type: 'input', label: '請輸入小段' },
  { name: '地號', type: 'input', label: '請輸入地號' },
  { name: '使用面積', type: 'input', label: '請輸入使用面積' },
  { name: '所有權人', type: 'input', label: '請輸入所有權人姓名' }
]
export const infoPerson = [
  { name: '行為人姓名', type: 'input', label: '請輸入行為人姓名' },
  { name: '行為人出生年月日', type: 'input_date', label: '請輸入行為人出生年月日' },
  { name: '行為人身分證', type: 'input', label: '請輸入行為人身分證' },
  { name: '行為人電話', type: 'input', label: '請輸入行為人電話' },
  { name: '行為人住址', type: 'input', label: '請輸入行為人住址' }
]
export const violation = [
  { id: '0', data: '' },
  { id: '1', data: '探礦、採礦、鑿青、採取土石、設置有關附屬設施' },
  { id: '2', data: '修建鐵路、公路、其他道路、溝渠' },
  { id: '3', data: '開發建築用地' },
  { id: '4', data: '設置公園' },
  { id: '5', data: '設置墳墓' },
  { id: '6', data: '設置遊憩用地' },
  { id: '7', data: '設置運動場地' },
  { id: '8', data: '設置軍事訓練場' },
  { id: '9', data: '堆積土石' },
  { id: '10', data: '處理廢棄物' },
  { id: '11', data: '其他開挖整地' },
  { id: '12', data: '修築農路或整坡作業' },
  { id: '13', data: '超限利用' }
]
export const conclusion = [
  { id: '0', data: '' },
  { id: '1', data: '不當使用山坡地部份依據水土保持法相關法規辦理。' },
  { id: '2', data: '涉違反其他法令部份，請各有關單位逕依權責卓處。' },
  { id: '3', data: '現場立即停工。並作妥相關防災措施（現場如未停工，將施以連續處分。另如有裸露地應配合草蓆或塑膠布覆蓋以防止表土流失）。' },
  { id: '4', data: '已致生水土流失或毀損水土保持之處理與維護設施。' },
  { id: '5', data: '請依水土保持服務團輔導事項辦理。' },
  { id: '6', data: '其他。' }
]
export const paper = [
  { id: '1', type: '限改函', data: '拆牆' },
  { id: '2', type: '限改函', data: '植生' },
  { id: '3', type: '限改函', data: '植生+拆牆' },
  { id: '4', type: '移送函', data: '' },
  { id: '5', type: '移送後函知相關單位', data: '' },
  { id: '6', type: '移送簽', data: '' },
  { id: '7', type: '處分函', data: '有限改' },
  { id: '8', type: '處分函', data: '無限改' },
  { id: '9', type: '處分簽', data: '他人所有、有拆牆、有陳述' },
  { id: '10', type: '處分簽', data: '他人所有、有拆牆、無陳述' },
  { id: '11', type: '處分簽', data: '他人所有、有植生、有陳述' },
  { id: '12', type: '處分簽', data: '他人所有、有植生、無陳述' },
  { id: '13', type: '處分簽', data: '他人所有、有植生+拆牆、有陳述' },
  { id: '14', type: '處分簽', data: '他人所有、有植生+拆牆、無陳述' },
  { id: '15', type: '處分簽', data: '他人所有、無限改、有陳述' },
  { id: '16', type: '處分簽', data: '他人所有、無限改、無陳述' },
  { id: '17', type: '處分簽', data: '自有、有拆牆、有陳述' },
  { id: '18', type: '處分簽', data: '自有、有拆牆、無陳述' },
  { id: '19', type: '處分簽', data: '自有、有植生、有陳述' },
  { id: '20', type: '處分簽', data: '自有、有植生、無陳述' },
  { id: '21', type: '處分簽', data: '自有、有植生+拆牆、有陳述' },
  { id: '22', type: '處分簽', data: '自有、有植生+拆牆、無陳述' },
  { id: '23', type: '處分簽', data: '自有、無限改、有陳述' },
  { id: '24', type: '處分簽', data: '自有、無限改、無陳述' },
  { id: '25', type: '陳述', data: '地主未到' },
  { id: '26', type: '處分簽', data: '有土同、人未到' },
  { id: '27', type: '處分簽', data: '缺土同' },
  { id: '28', type: '無違規請公所加強巡查', data: '' }
]
