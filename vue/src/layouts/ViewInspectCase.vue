<template >
  <div class="w-full h-full">
    <q-list class="h-full xl:px-90 lg:px-40 md:px-20 overflow-y-auto" bordered>
      <q-item-label class="text-2xl text-center text-bold p-3">新北市政府農業局違規使用山坡地案件現場會勘紀錄表</q-item-label>
      <q-item>
        <div class="w-full">
          <div class="grid grid-cols-[0.1fr,0.5fr,1.6fr] gap-5 flex items-center py-2">
            <span>
              <q-icon name="article" color="grey-7" size="sm" />
            </span>
            <span class="text-lg text-black text-bold">案由: </span>
            <span>
              <q-input v-model="inspectRecord['案由']" filled dense />
            </span>
          </div>
          <div class="grid grid-cols-[0.1fr,0.5fr,1.6fr] gap-5 flex items-center py-2">
            <span>
              <q-icon name="event" color="grey-7" size="sm" />
            </span>
            <span class="text-lg text-black text-bold">時間: </span>
            <span>
              <q-input v-model="inspectRecord['時間']" readonly filled dense>
                <template v-slot:append>
                  <q-icon name="event" class="cursor-pointer">
                    <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                      <div class="p-3">
                        <div class="q-gutter-md row items-start">
                          <q-date v-model="inspectRecord['時間']" mask="YYYY-MM-DD HH:mm" />
                          <q-time v-model="inspectRecord['時間']" mask="YYYY-MM-DD HH:mm" />
                        </div>
                        <div class="pt-3">
                          <div class="row items-center justify-end my-2">
                            <q-btn v-close-popup label="關閉" color="grey" flat />
                            <q-btn v-close-popup label="確定" color="positive" flat />
                          </div>
                        </div>
                      </div>
                    </q-popup-proxy>
                  </q-icon>
                </template>
              </q-input>
            </span>
          </div>
        </div>
      </q-item>
      <q-expansion-item class="text-lg text-bold my-2 px-4" header-class="bg-blue-1" expand-separator icon="supervisor_account" label="會勘單位與人員">
        <q-card>
          <q-card-section>
            <div v-for="_attendees, n of attendees" :key="n">
              <div class="grid grid-cols-[0.4fr,0.9fr,0.1fr] gap-5 flex items-center py-2">
                <span>{{ _attendees.name }}</span>
                <span>
                  <template v-if="_attendees.type === 'select'">
                    <q-select v-model="inspectRecord[_attendees.name].value" :options="_attendees.data" :label=_attendees.label filled dense />
                  </template>
                  <template v-else>
                    <q-input v-model="inspectRecord[_attendees.name].value" :label=_attendees.label filled dense />
                  </template>
                </span>
                <span>
                  <q-btn icon="draw" color="grey-3" class="text-grey-7" @click="isShowCanvas = !isShowCanvas; signTargetName = _attendees.name" dense />
                </span>
              </div>
              <div class="py-3" v-if="inspectRecord[_attendees.name].sign.length > 0">
                <q-carousel class="border-2" v-model="inspectRecord[_attendees.name].slide" ref="carousel" thumbnails infinite swipeable animated>
                  <template v-for="(v, k) in inspectRecord[_attendees.name].sign" :key="k">
                    <q-carousel-slide :name="k + 1" :img-src="v" />
                  </template>
                  <template v-slot:control>
                    <q-carousel-control position="top-left">
                      <q-btn class="absolute top-0 left-0" icon="delete" color="negative" @click="deletcSign(_attendees.name, $refs.carousel[0].modelValue)" flat round dense>
                        <q-tooltip>刪除此簽名</q-tooltip>
                      </q-btn>
                    </q-carousel-control>
                  </template>
                </q-carousel>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </q-expansion-item>
      <q-expansion-item class="text-lg text-bold my-2 px-4" header-class="bg-blue-1" expand-separator icon="place" label="土地基本資料">
        <q-card>
          <q-card-section>
            <div>
              <div class="grid grid-cols-[0.4fr,1fr] gap-5 flex items-center py-2">
                <span>定位座標(TWD97)</span>
                <span class="row">
                  <span class="col pr-2">
                    <q-input v-model="inspectRecord['TWD97_X']" label="請輸入X座標" filled dense />
                  </span>
                  <span class="col pl-2">
                    <q-input v-model="inspectRecord['TWD97_Y']" label="請輸入Y座標" filled dense />
                  </span>
                </span>
              </div>
            </div>
            <div v-for="_info, i of info" :key="i">
              <div class="grid grid-cols-[0.4fr,1fr] gap-5 flex items-center py-2">
                <span>{{ _info.name }}</span>
                <span>
                  <template v-if="_info.type === 'select_district'">
                    <q-select v-model="inspectRecord[_info.name]" :options="district" :label=_info.label @update:model-value="setLot()" filled dense/>
                  </template>
                  <template v-else-if="_info.type === 'select'">
                    <q-select v-model="inspectRecord[_info.name]" :options="lot" :label=_info.label filled dense />
                  </template>
                  <template v-else>
                    <q-input v-model="inspectRecord[_info.name]" :label=_info.label filled dense />
                  </template>
                </span>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </q-expansion-item>
      <q-expansion-item class="text-lg text-bold my-2 px-4" header-class="bg-blue-1" expand-separator icon="perm_identity" label="行為人基本資料">
        <q-card>
          <q-card-section>
            <div v-for="_infoPerson, i of infoPerson" :key="i">
              <div class="grid grid-cols-[0.4fr,1fr] gap-5 flex items-center py-2">
                <span>{{ _infoPerson.name }}</span>
                <span>
                  <template v-if="_infoPerson.type === 'select'">
                    <q-select v-model="inspectRecord[_infoPerson.name]" :options="_infoPerson.data" :label=_infoPerson.label filled dense />
                  </template>
                  <template v-else>
                    <q-input v-model="inspectRecord[_infoPerson.name]" :label=_infoPerson.label filled dense />
                  </template>
                </span>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </q-expansion-item>
      <q-item>
        <div class="w-full">
          <div class="grid grid-cols-[0.1fr,0.5fr,1.6fr] gap-5 flex items-center py-2">
            <span>
              <q-icon name="info" color="grey-7" size="sm" />
            </span>
            <span class="text-lg text-black text-bold">違規類別(可複選): </span>
            <span class="grid grid-cols-[1fr,1fr] gap-5">
              <span>
                <q-select v-model="inspectRecord['違規類別']" :options="violationType" label="請選擇違規項目" filled dense />
              </span>
              <span>
                <q-input v-model="inspectRecord['其他違規項目']" label="請輸入其他違規項目" filled dense />
              </span>
            </span>
          </div>
          <div class="grid grid-cols-[0.1fr,0.5fr,1.6fr] gap-5 flex items-center py-2">
            <span>
              <q-icon name="info_outline" color="grey-7" size="sm" />
            </span>
            <span class="text-lg text-black text-bold">輔導類別: </span>
            <span>
              <q-toggle v-model="inspectRecord['輔導類別']" checked-icon="check" color="green" label="移請水土保持服務團指導實施水土保持處理與維護" unchecked-icon="clear"/>
            </span>
          </div>
          <div class="grid grid-cols-[0.1fr,0.5fr,1.6fr] gap-5 flex items-center py-2">
            <span>
              <q-icon name="edit" color="grey-7" size="sm" />
            </span>
            <span class="text-lg text-black text-bold">各單位意見: </span>
            <span>
              <q-input v-model="inspectRecord['各單位意見']" type="textarea" filled dense/>
            </span>
          </div>
          <div class="grid grid-cols-[0.1fr,0.5fr,1.6fr] gap-5 flex items-center py-2">
            <span>
              <q-icon name="edit" color="grey-7" size="sm" />
            </span>
            <span class="text-lg text-black text-bold">請行為人陳述意見: </span>
            <span>
              <q-input v-model="inspectRecord['行為人意見']" type="textarea" filled dense/>
            </span>
          </div>
          <div class="grid grid-cols-[0.1fr,0.5fr,1.6fr] gap-5 flex items-center py-2">
            <span>
              <q-icon name="collections" color="grey-7" size="sm" />
            </span>
            <span class="text-lg text-black text-bold">會勘結論(可複選): </span>
            <span class="grid grid-cols-[1fr,1fr] gap-5">
              <span>
                <q-select v-model="inspectRecord['會勘結論']" :options="conclusionType" label="請選擇會勘結論項目" filled dense />
              </span>
              <span>
                <q-input v-model="inspectRecord['其他會勘結論']" label="請輸入其他會勘結論" filled dense />
              </span>
            </span>
          </div>
          <div class="grid grid-cols-[0.1fr,0.5fr,1.6fr] gap-5 flex items-center py-2">
            <span>
              <q-icon name="collections" color="grey-7" size="sm" />
            </span>
            <span class="text-lg text-black text-bold">現場照片: </span>
            <span>
              <q-input v-model="uploadImg" @update:model-value="getBase64Img(uploadImg)" type="file" accept=".jpg, .png" filled dense />
            </span>
          </div>
          <template v-if="inspectRecord['現場照片'].length > 0">
            <div class="pb-2" v-for="(v, k) in inspectRecord['現場照片']" :key="k">
              <div class="relative flex justify-end bg-grey-3">
                <q-btn class="absolute top-2 left-2" icon="delete" color="negative" @click="inspectRecord['現場照片'] = inspectRecord['現場照片'].filter((e, i) => i !== k)" flat round dense />
                <img :src="v" />
              </div>
            </div>
          </template>
          <div class="grid grid-cols-[0.1fr,0.5fr,1.6fr] gap-5 flex items-center py-2">
            <span>
              <q-icon name="watch_later" color="grey-7" size="sm" />
            </span>
            <span class="text-lg text-black text-bold">散會: </span>
            <span>
              <q-input v-model="inspectRecord['散會']" readonly filled dense>
                <template v-slot:append>
                  <q-icon name="event" class="cursor-pointer">
                    <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                      <div class="p-3">
                        <div class="q-gutter-md row items-start">
                          <q-date v-model="inspectRecord['散會']" mask="YYYY-MM-DD HH:mm" />
                          <q-time v-model="inspectRecord['散會']" mask="YYYY-MM-DD HH:mm" />
                        </div>
                        <div class="pt-3">
                          <div class="row items-center justify-end my-2">
                            <q-btn v-close-popup label="關閉" color="grey" flat />
                            <q-btn v-close-popup label="確定" color="positive" flat />
                          </div>
                        </div>
                      </div>
                    </q-popup-proxy>
                  </q-icon>
                </template>
              </q-input>
            </span>
          </div>
          <div class="grid grid-cols-[0.1fr,0.5fr,1.6fr] gap-5 flex items-center py-2">
            <span>
              <q-icon name="person" color="grey-7" size="sm" />
            </span>
            <span class="text-lg text-black text-bold">行為人簽名: </span>
            <span>
              <q-btn icon="draw" color="grey-3" class="text-grey-7" @click="isShowCanvas = !isShowCanvas; signTargetName = '行為人簽名'" dense />
            </span>
          </div>
          <div class="py-3" v-if="inspectRecord['行為人簽名'].sign.length > 0">
            <q-carousel class="border-2" v-model="inspectRecord['行為人簽名'].slide" ref="carousel" thumbnails infinite swipeable animated>
              <template v-for="(v, k) in inspectRecord['行為人簽名'].sign" :key="k">
                <q-carousel-slide :name="k + 1" :img-src="v" />
              </template>
              <template v-slot:control>
                <q-carousel-control position="top-left">
                  <q-btn class="absolute top-0 left-0" icon="delete" color="negative" @click="deletcSign('行為人簽名', $refs.carousel[0].modelValue)" flat round dense>
                    <q-tooltip>刪除此簽名</q-tooltip>
                  </q-btn>
                </q-carousel-control>
              </template>
            </q-carousel>
          </div>
        </div>
      </q-item>
      <q-item class="grid">
        <div class="q-pa-md q-gutter-sm justify-self-end">
          <q-btn color="negative" icon="delete" @click="cancel()" label="取消" />
          <q-btn color="primary" icon="send" @click="updateInspectCase()" label="確認修改" />
        </div>
      </q-item>
    </q-list>
    <div class="canvasContainer" v-show="isShowCanvas">
      <q-card class="xl:(w-1/2 h-1/2) lg:(w-3/4 h-3/4) md:(w-3/4 h-1/2) grid grid-rows-[0.1fr,1.9fr]">
        <q-btn class="absolute top-1 right-1 z-3" icon="close" flat rounded dense @click="isShowCanvas = false; signTargetName = ''; clearCanvas()" />
        <q-card-section class="p-0 m-0">
          <div class="flex justify-evenly px-3 py-1">
            <q-btn icon="auto_fix_off" size="lg" flat dense @click="clearCanvas()">
              <q-tooltip>清空畫布</q-tooltip>
            </q-btn>
            <q-btn icon="undo" size="lg" flat dense @click="undoCanvas()">
              <q-tooltip>上一步</q-tooltip>
            </q-btn>
            <q-btn icon="save_as" size="lg" flat dense @click="saveCanvas(); clearCanvas()">
              <q-tooltip>儲存</q-tooltip>
            </q-btn>
          </div>
        </q-card-section>
        <q-card-section class="w-full h-full p-0 border-2">
          <div class="w-full h-full">
            <canvas id="canvas" class="w-full h-full" />
          </div>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script>
import { defineComponent, onMounted, ref } from 'vue'
import { info, infoPerson, attendees, violation, conclusion } from './data'
import { useRouter } from 'vue-router'
import { forEach, forEachObjIndexed } from 'ramda'
import SmoothSignature from 'smooth-signature'
import axios from 'axios'
import jsonToFormData from 'json-form-data'

export default defineComponent({
  name: 'ViewInspectCase',
  setup () {
    let signature
    const router = useRouter()
    const isShowCanvas = ref(true)
    const signTargetName = ref('')
    const district = ref([])
    const lot = ref([])
    const inspectRecord = ref({
      案由: '',
      時間: '',
      本府局處1: { value: '', slide: 1, sign: [] },
      本府局處2: { value: '', slide: 1, sign: [] },
      本府局處3: { value: '', slide: 1, sign: [] },
      本府地政事務所: { value: '', slide: 1, sign: [] },
      本府警察局: { value: '', slide: 1, sign: [] },
      本府違章建築拆除大隊: { value: '', slide: 1, sign: [] },
      其他1: { value: '', slide: 1, sign: [] },
      其他2: { value: '', slide: 1, sign: [] },
      TWD97_X: '',
      TWD97_Y: '',
      行政區: '',
      地段: '',
      小段: '',
      地號: '',
      使用面積: '',
      所有權人: '',
      行為人姓名: '',
      行為人出生年月日: '',
      行為人身分證: '',
      行為人電話: '',
      行為人住址: '',
      違規類別: '',
      其他違規項目: '',
      輔導類別: false,
      各單位意見: '',
      行為人意見: '',
      會勘結論: '',
      現場照片: [],
      其他會勘結論: '',
      散會: '',
      行為人簽名: { slide: 1, sign: [] }
    })
    const imgToBase64 = (e) => {
      return new Promise((resolve) => {
        const reader = new FileReader()
        reader.readAsDataURL(e)
        reader.onload = () => {
          resolve(reader.result)
        }
      })
    }
    const getRegion = async () => {
      try {
        const response = await axios.get(process.env.API_URL + '/get_region')

        if (response.data.status === 'success') {
          forEach(v => {
            district.value.push({
              label: v.NAME,
              value: v.CODE
            })
          })(response.data.row.TOWN)
        } else {
          throw new Error(response.data.msg)
        }
      } catch (err) {
        alert(String(err))
      }
    }
    const setLot = async () => {
      try {
        const response = await axios.get(process.env.API_URL + '/get_section_list?district=' + inspectRecord.value['行政區'].value)

        if (response.data.status === 'success') {
          forEach(v => {
            lot.value.push({
              label: v.NAME,
              value: v.SEC
            })
          })(response.data.row.RESPONSE[0].SECTION)
        } else {
          throw new Error(response.data.msg)
        }
      } catch (err) {
        alert(String(err))
      }
    }
    const getInspectCase = async () => {
      try {
        const formData = new FormData()
        formData.append('caseId', router.currentRoute.value.params.caseId)
        const response = await axios.post(process.env.API_URL + '/get_inspect_case', formData)

        if (response.data.status === 'success') {
          forEachObjIndexed((value, key) => {
            if (key === '土地基本資料') {
              forEachObjIndexed((v, k) => {
                inspectRecord.value[k] = v
              })(value)
            } else if (key === '會勘單位與人員') {
              forEachObjIndexed((v, k) => {
                if (k.indexOf('簽名') > 0) {
                  inspectRecord.value[k.replace('簽名', '')].sign = v
                } else {
                  inspectRecord.value[k].value = v
                }
              })(value)
            } else if (key === '行為人基本資料') {
              forEachObjIndexed((v, k) => {
                inspectRecord.value[k] = v
              })(value)
            } else {
              inspectRecord.value[key] = value
            }
          })(response.data.row)
        } else {
          throw new Error(response.data.msg)
        }
      } catch (err) {
        alert(String(err))
      }
    }
    const toFormData = (obj) => {
      return jsonToFormData(obj, {
        initialFormData: new FormData(),
        showLeafArrayIndexes: true,
        includeNullValues: false,
        mapping: function (value) {
          if (typeof value === 'boolean') {
            return +value ? '1' : '0'
          }
          return value
        }
      })
    }
    const getObjData = () => {
      const result = {}
      try {
        forEachObjIndexed((v, k) => {
          console.log(v, k)
          if (v.value !== undefined) {
            if (['行政區', '地段'].includes(k)) {
              result[k] = v.label
            } else {
              result[k] = v.value
              result[k + '簽名'] = v.sign
            }
          } else {
            if (k === '現場照片') {
              if (v.length <= 8) {
                result[k] = v
              } else {
                throw new Error(k + '最多可上傳 8 張')
              }
            } else {
              if (!['其他1', '其他2', '其他違規項目', '其他會勘結論'].includes(k)) {
                if (v !== '') {
                  result[k] = v
                } else {
                  throw new Error(k + '不可為空值')
                }
              }
            }
          }
        })(inspectRecord.value)
      } catch (err) {
        alert(err)
      }
      return result
    }

    onMounted(() => {
      getRegion()
      getInspectCase()
      const canvas = document.getElementById('canvas')
      signature = new SmoothSignature(canvas, {
        scale: 4,
        color: '#000000',
        bgColor: '#FFFFFF'
      })
      isShowCanvas.value = false

      if ('onorientationchange' in window) {
        window.onorientationchange = (e) => {
          signature.getRotateCanvas(90)
        }
      } else if ('screen' in window && 'orientation' in window.screen) {
        window.screen.orientation.addEventListener('change', (e) => {
          signature.getRotateCanvas(90)
        }, false)
      }
    })

    return {
      clearCanvas () {
        signature.clear()
      },
      undoCanvas () {
        signature.undo()
      },
      saveCanvas () {
        const r = signature.getPNG()
        inspectRecord.value[signTargetName.value].sign.push(r)
        alert('已儲存簽名檔')
      },
      deletcSign (name, key) {
        const sign = []

        forEachObjIndexed((v, k) => {
          if (parseInt(k) !== (key - 1)) {
            sign.push(v)
          }
        })(inspectRecord.value[name].sign)

        inspectRecord.value[name].sign = sign
      },
      async updateInspectCase () {
        try {
          const data = getObjData()
          if (Object.keys(data).length > 0) {
            const formData = toFormData(data)
            formData.append('案件編號', router.currentRoute.value.params.caseId)
            const response = await axios.post(process.env.API_URL + '/update_inspect_case', formData)
            if (response.data.status === 'success') {
              alert(response.data.msg)
            } else {
              throw new Error(response.data.msg)
            }
          }
        } catch (err) {
          alert(String(err))
        }
      },
      async getBase64Img (element) {
        inspectRecord.value['現場照片'].push(await imgToBase64(element[0]))
      },
      cancel () {
        if (confirm('請確認是否要離開編輯表單頁面，您所填列的資料不會保存')) {
          router.push({ path: '/' })
        }
      },
      isShowCanvas,
      signTargetName,
      uploadImg: ref(''),
      attendees,
      info,
      infoPerson,
      violation,
      conclusion,
      violationType: violation.map(_V => _V.data),
      conclusionType: conclusion.map(_C => _C.data),
      inspectRecord,
      district,
      lot,
      setLot
    }
  }
})
</script>

<style lang="sass">
.canvasContainer
  display: flex
  justify-content: center
  align-items: center
  position: absolute
  top: 0
  left: 0
  width: 100%
  height: 100%
  background-color: rgba(0, 0, 0, 0.5)

</style>
