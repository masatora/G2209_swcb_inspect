<template>
  <div class="w-full h-full">
    <q-list class="h-full xl:px-90 lg:px-40 md:px-20">
      <q-item-label class='text-2xl text-center text-bold p-3'>新北市政府農業局違規使用山坡地案件現場會勘紀錄表</q-item-label>
      <q-item>
        <q-item-section />
        <q-item-section side>
          <q-btn color="primary" icon="post_add" @click="router.push({ path: '/form' })" label="新增表單" />
        </q-item-section>
      </q-item>
      <q-item class="bg-primary text-lg text-white text-bold text-center">
        <q-item-section>案件時間</q-item-section>
        <q-item-section>案由</q-item-section>
        <q-item-section>行政區</q-item-section>
        <q-item-section>行為人</q-item-section>
        <q-item-section>填寫人</q-item-section>
        <q-item-section>更新時間</q-item-section>
        <q-item-section>功能列表</q-item-section>
      </q-item>
      <q-separator />
      <q-item v-for="(value, key) in inspectCaseList" :key="key" class="text-center" clickable>
        <q-item-section>{{ value['案件時間'] }}</q-item-section>
        <q-item-section>{{ value['案由'] }}</q-item-section>
        <q-item-section>{{ value['行政區'] }}</q-item-section>
        <q-item-section>
          <div class="grid grid-cols-[1fr,1fr,1fr] flex justify-center items-center">
            <span>
              <q-btn icon="draw" color="grey-7" @click="isShowCanvas = true; canvasTargetKey = key" flat round dense>
                <q-tooltip>請行為人簽名確認</q-tooltip>
              </q-btn>
            </span>
            <span v-if="value['行為人簽名'] !== null">
              <q-btn icon="visibility" color="grey-7" @click="isShowSign = true; signSrc = value['行為人簽名']" flat round dense>
                <q-tooltip>檢視行為人簽名</q-tooltip>
              </q-btn>
            </span>
            <span>{{ value['行為人姓名'] }}</span>
          </div>
        </q-item-section>
        <q-item-section>{{ value['填寫人'] }}</q-item-section>
        <q-item-section>{{ value['更新時間'] }}</q-item-section>
        <q-item-section>
          <div class="flex justify-evenly">
            <q-btn icon="description" color="grey-7" flat round dense>
              <q-tooltip>詳細內容</q-tooltip>
            </q-btn>
            <q-btn-dropdown icon="file_download" color="primary" size="12px" dense>
              <q-list>
                <q-item v-for="_paper, i of paper" :key="i" v-close-popup @click="onItemClick" clickable bordered>
                  <q-item-section>
                    <div class="border-gray-500">
                      <q-item-label>{{ _paper.type }}</q-item-label>
                      <q-item-label caption>{{ _paper.data }}</q-item-label>
                    </div>
                  </q-item-section>
                </q-item>
              </q-list>
            </q-btn-dropdown>
          </div>
        </q-item-section>
      </q-item>
    </q-list>
    <div class="canvasContainer" v-show="isShowCanvas">
      <q-card class="xl:(w-1/2 h-1/2) lg:(w-2/3 h-2/3) md:(w-3/4 h-1/2) grid grid-rows-[0.1fr,1.9fr]">
        <q-btn class="absolute top-1 right-1 z-3" icon="close" flat rounded dense @click="isShowCanvas = false; signTargetName = ''; clearCanvas()" />
        <q-card-section class="p-0">
          <div class="flex justify-evenly px-3 py-1">
            <q-btn icon="auto_fix_off" size="lg" flat dense @click="clearCanvas()">
              <q-tooltip>清空畫布</q-tooltip>
            </q-btn>
            <q-btn icon="undo" size="lg" flat dense @click="undoCanvas()">
              <q-tooltip>上一動</q-tooltip>
            </q-btn>
            <q-btn icon="save_as" size="lg" flat dense @click="saveCanvas(); clearCanvas()">
              <q-tooltip>儲存</q-tooltip>
            </q-btn>
          </div>
        </q-card-section>
        <q-separator />
        <q-card-section class="p-0">
          <div class="w-full h-full">
            <canvas id="canvas" class="w-full h-full" />
          </div>
        </q-card-section>
      </q-card>
    </div>
    <div class="signContainer" v-show="isShowSign">
      <div class="relative">
        <q-btn class="absolute top-0 right-0" icon="close" color="grey-7" @click="isShowSign = false; signSrc = ''" flat round dense />
        <img :src="signSrc" />
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { paper } from './data'
import axios from 'axios'
import SmoothSignature from 'smooth-signature'
// import { forEachObjIndexed } from 'ramda'

export default defineComponent({
  name: 'InspectCaseList',
  components: {
  },
  setup () {
    const router = useRouter()
    const inspectCaseList = ref({})
    const getInspectCaseList = async () => {
      try {
        const response = await axios.get(process.env.API_URL + '/get_inspect_case_list')
        if (response.data.status === 'success') {
          inspectCaseList.value = response.data.row
        } else {
          throw new Error(response.data.msg)
        }
      } catch (err) {
        alert(String(err))
      }
    }
    let signature
    const isShowCanvas = ref(true)
    const isShowSign = ref(false)
    const signSrc = ref('')
    const canvasTargetKey = ref('')

    onMounted(() => {
      getInspectCaseList()
      const canvas = document.getElementById('canvas')
      signature = new SmoothSignature(canvas, {
        scale: 4,
        color: '#000000',
        bgColor: '#FFFFFF'
      })
      isShowCanvas.value = false
    })

    return {
      paper,
      router,
      inspectCaseList,
      isShowCanvas,
      isShowSign,
      signSrc,
      canvasTargetKey,
      clearCanvas () {
        signature.clear()
      },
      undoCanvas () {
        signature.undo()
      },
      saveCanvas () {
        const r = signature.getPNG()
        inspectCaseList.value[canvasTargetKey.value]['行為人簽名'] = r
        alert('已儲存簽名檔')
      }
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

.signContainer
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
