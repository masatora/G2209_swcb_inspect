<template >
  <div class="w-full h-full lg:px-100 md:px-20 py-2">
    <q-list class="h-full overflow-y-auto" bordered>
      <q-item-label class="text-2xl text-center text-bold p-3">新北市政府農業局違規使用山坡地案件現場會勘紀錄表</q-item-label>
      <q-item>
        <q-item-section side>
          <q-icon name="article" />
        </q-item-section>
        <q-item-section class="text-lg text-black text-bold" side>案由: </q-item-section>
        <q-item-section>
          <q-input v-model="inspectRecord['案由']" filled dense />
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section side>
          <q-icon name="event_available" />
        </q-item-section>
        <q-item-section class="text-lg text-black text-bold" side>時間: </q-item-section>
        <q-item-section>
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
        </q-item-section>
      </q-item>
      <q-expansion-item class="text-lg text-bold my-2 px-4" header-class="bg-blue-1" expand-separator icon="supervisor_account" label="會勘單位與人員">
        <q-card>
          <q-card-section>
            <div v-for="_attendees, n of attendees" :key="n">
              <div class="grid grid-cols-[0.4fr,1.6fr,0.1fr] gap-5 flex items-center py-2">
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
                  <q-btn icon="edit" color="grey-3" class="text-grey-7" @click="isShowCanvas = !isShowCanvas; signTargetName = _attendees.name" dense />
                </span>
              </div>
              <div class="py-3" v-if="inspectRecord[_attendees.name].sign.length > 0">
                <q-carousel swipeable animated v-model="inspectRecord[_attendees.name].slide" thumbnails infinite>
                  <template v-for="(v, k) in inspectRecord[_attendees.name].sign" :key="k">
                    <q-carousel-slide :name="k + 1" :img-src="v" />
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
            <q-item>
              <q-item-section class="text-lg text-black text-bold" side>衛星定位座標(TWD97) </q-item-section>
              <q-item-section>
                <q-input v-model="inspectRecord['TWD97_X']" label="請輸入X座標" filled dense />
              </q-item-section>
              <q-item-section>
                <q-input v-model="inspectRecord['TWD97_Y']" label="請輸入Y座標" filled dense />
              </q-item-section>
            </q-item>
            <q-item v-for="_info, i of info" :key="i">
              <q-item-section class="text-lg text-black text-bold" side>{{ _info.name }}</q-item-section>
              <q-item-section>
                <q-select v-show="(_info.type === 'select')" v-model="inspectRecord[_info.name]" :options="_info.data" :label=_info.label filled dense/>
                <q-select v-show="(_info.type === 'select_district')" v-model="inspectRecord[_info.name]" @update:model-value="getSectionList()" :options="_info.data" :label=_info.label filled dense/>
                <q-input v-show="(_info.type === 'input')" v-model="inspectRecord[_info.name]" :label=_info.label filled dense />
              </q-item-section>
            </q-item>
          </q-card-section>
        </q-card>
      </q-expansion-item>
      <q-expansion-item class="text-lg text-bold my-2 px-4" header-class="bg-blue-1" expand-separator icon="perm_identity" label="行為人基本資料">
        <q-card>
          <q-card-section>
            <q-item v-for="_infoPerson, i of infoPerson" :key="i">
              <q-item-section class="text-lg text-black text-bold" side>{{ _infoPerson.name }}</q-item-section>
              <q-item-section>
                <q-select v-show="(_infoPerson.type === 'select')" v-model="inspectRecord[_infoPerson.name]" :options="_infoPerson.data" :label=_infoPerson.label filled dense/>
                <q-input v-show="(_infoPerson.type === 'input')" v-model="inspectRecord[_infoPerson.name]" :label=_infoPerson.label filled dense />
              </q-item-section>
            </q-item>
          </q-card-section>
        </q-card>
      </q-expansion-item>
      <q-item>
        <q-item-section side>
          <q-icon name="info" />
        </q-item-section>
        <q-item-section class="text-lg text-black text-bold" side>違規類別(可複選): </q-item-section>
        <q-item-section>
          <q-select v-model="inspectRecord['違規項目']" :options="violationType" label="請選擇違規項目" filled dense />
        </q-item-section>
        <q-item-section>
          <q-input v-model="inspectRecord['其他違規項目']" label="請輸入其他違規項目" filled dense />
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section side>
          <q-icon name="info_outline" />
        </q-item-section>
        <q-item-section class="text-lg text-black text-bold" side>輔導類別: </q-item-section>
        <q-item-section>
          <q-toggle v-model="inspectRecord['輔導類別']" checked-icon="check" color="green" label="移請水土保持服務團指導實施水土保持處理與維護" unchecked-icon="clear"/>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section side>
          <q-icon name="edit" />
        </q-item-section>
        <q-item-section class="text-lg text-black text-bold" side>各單位意見: </q-item-section>
        <q-item-section>
          <q-input v-model="inspectRecord['各單位意見']" type="textarea" filled dense/>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section side>
          <q-icon name="edit" />
        </q-item-section>
        <q-item-section class="text-lg text-black text-bold" side>請行為人陳述意見: </q-item-section>
        <q-item-section>
          <q-input v-model="inspectRecord['行為人意見']" type="textarea" filled dense/>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section side>
          <q-icon name="description" />
        </q-item-section>
        <q-item-section class="text-lg text-black text-bold" side>會勘結論(可複選): </q-item-section>
        <q-item-section>
          <q-select v-model="inspectRecord['會勘結論']" :options="conclusionType" label="請選擇會勘結論項目" filled dense />
        </q-item-section>
        <q-item-section>
          <q-input v-model="inspectRecord['其他會勘結論']" label="請輸入其他會勘結論" filled dense />
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section side>
          <q-icon name="collections" />
        </q-item-section>
        <q-item-section class="text-lg text-black text-bold" side>現場照片: </q-item-section>
        <q-item-section>
          <q-input @update:model-value="val => { files = val }" multiple type="file" hint="可選擇多個檔案" filled dense/>
        </q-item-section>
      </q-item>
      <q-item>
        <q-item-section side>
          <q-icon name="watch_later" />
        </q-item-section>
        <q-item-section class="text-lg text-black text-bold" side>散會: </q-item-section>
        <q-item-section>
          <q-input readonly filled dense>
            <template v-slot:append>
              <q-icon name="event" class="cursor-pointer">
                <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                  <div class="p-3">
                    <div class="q-gutter-md row items-start">
                      <q-time v-model="inspectRecord['時間']" mask="HH:mm" />
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
        </q-item-section>
      </q-item>
      <q-item class="grid">
        <div class="q-pa-md q-gutter-sm justify-self-end">
          <q-btn color="negative" icon="delete" @click.prevent="cancel" label="取消" />
          <q-btn color="primary" icon="send" @click.prevent="submit" label="確認送出" />
        </div>
      </q-item>
    </q-list>
    <div id="canvasContainer" v-show="isShowCanvas">
      <q-card class="lg:(w-1/2 h-1/2) md:(w-3/4 h-1/2) grid grid-rows-[0.1fr,1.9fr]">
        <q-btn class="absolute top-1 right-1 z-3" icon="close" flat rounded dense @click="isShowCanvas = false; signTargetName = ''; clearCanvas()" />
        <q-card-section class="p-0">
          <div class="flex justify-evenly px-3 py-1">
            <q-btn icon="auto_fix_off" size="lg" flat dense @click="clearCanvas()">
              <q-tooltip>清空畫布</q-tooltip>
            </q-btn>
            <q-btn icon="undo" size="lg" flat dense @click="undoCanvas()">
              <q-tooltip>上一動</q-tooltip>
            </q-btn>
            <q-btn icon="save_as" size="lg" flat dense @click="saveCanvas()">
              <q-tooltip>儲存</q-tooltip>
            </q-btn>
          </div>
        </q-card-section>
        <q-card-section class="p-0">
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
import axios from 'axios'
import { info, infoPerson, attendees, violation, conclusion } from './data'
import { useRouter } from 'vue-router'
import SmoothSignature from 'smooth-signature'

let districtData
async function getVillage () {
  try {
    const district = await axios.get('https://www.ntpcswc.ntpc.gov.tw/ntpcagr-api/get_region')
    districtData = district.data.TOWN
    districtData = districtData.map((_district) => {
      return {
        districtCode: _district.CODE,
        districtName: _district.NAME
      }
    })
  } catch (error) {
    districtData = []
    throw new Error(error)
  }
}
getVillage()
const violationType = violation.map(_V => _V.data)
const conclusionType = conclusion.map(_C => _C.data)
export default defineComponent({
  name: 'MainLayout',
  components: {
  },
  setup () {
    const router = useRouter()
    const getSectionList = () => {
      console.log('-------------------')
    }
    const cancel = () => {
      confirm('請確認是否要離開編輯表單頁面，您所填列的資料不會保存')
      router.push({ path: '/' })
    }
    const submit = () => {
      console.log('-------送出表單 1.打API到資料庫以及2.製作PDF------')
      router.push({ path: '/' })
    }
    let signature
    const isShowCanvas = ref(true)
    const signTargetName = ref('')
    const inspectRecord = ref({
      案由: '',
      時間: '',
      本市區公所: { value: ref(''), slide: ref(1), sign: ref([]) },
      本府局處: { value: ref(''), slide: ref(1), sign: ref([]) },
      本府地政事務所: { value: ref(''), slide: ref(1), sign: ref([]) },
      本府警察局: { value: ref(''), slide: ref(1), sign: ref([]) },
      本府違章建築拆除大隊: { v: ref(''), slide: ref(1), sign: ref([]) },
      其他1: { value: ref(''), slide: ref(1), sign: ref([]) },
      其他2: { value: ref(''), slide: ref(1), sign: ref([]) },
      TWD97_X: '',
      TWD97_y: '',
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
      輔導類別: ref(false),
      各單位意見: '',
      行為人意見: '',
      會勘結論: '',
      其他會勘結論: '',
      散會: ''
    })

    onMounted(() => {
      const canvas = document.getElementById('canvas')
      signature = new SmoothSignature(canvas, {
        scale: 4,
        color: '#000000',
        bgColor: '#efefef'
      })
      // console.log(canvas, signature)
      isShowCanvas.value = false
      console.log('efeeeff', navigator.geolocation)
      navigator.geolocation.getCurrentPosition(pos => {
        console.log(pos)
      })
    })

    return {
      isShowCanvas,
      signTargetName,
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
      attendees,
      info,
      infoPerson,
      violation,
      violationType,
      conclusion,
      conclusionType,
      getSectionList,
      cancel,
      submit,
      isShowDialog: ref({
        district: false
      }),
      inspectRecord
    }
  }
})
</script>

<style lang="sass">
#canvasContainer
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
