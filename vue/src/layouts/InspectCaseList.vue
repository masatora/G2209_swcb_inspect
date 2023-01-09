<template>
  <div class="w-full h-full">
    <q-list class="h-full xl:px-90 lg:px-30 md:px-10">
      <q-item-label class='text-2xl text-center text-bold p-3'>新北市政府農業局違規使用山坡地案件現場會勘紀錄表</q-item-label>
      <q-item>
        <q-item-section />
        <q-item-section side>
          <q-btn color="primary" icon="post_add" @click="router.push({ path: '/add' })" label="新增表單" />
        </q-item-section>
      </q-item>
      <q-item class="bg-primary text-lg text-white text-bold text-center">
        <q-item-section>案件時間</q-item-section>
        <q-item-section>案由</q-item-section>
        <q-item-section>行政區</q-item-section>
        <q-item-section>行為人姓名</q-item-section>
        <q-item-section>更新時間</q-item-section>
        <q-item-section>功能列表</q-item-section>
      </q-item>
      <q-separator />
      <q-item v-for="(value, key) in inspectCaseList" :key="key" class="text-center" clickable>
        <q-item-section>{{ value['案件時間'] }}</q-item-section>
        <q-item-section>{{ value['案由'] }}</q-item-section>
        <q-item-section>{{ value['行政區'] }}</q-item-section>
        <q-item-section>{{ value['行為人姓名'] }}</q-item-section>
        <q-item-section>{{ value['更新時間'] }}</q-item-section>
        <q-item-section>
          <div class="flex justify-evenly">
            <q-btn icon="description" color="grey-7" @click="router.push({ path: '/view/' + value['案件編號'] })" flat round dense>
              <q-tooltip>詳細內容</q-tooltip>
            </q-btn>
            <q-btn-dropdown icon="file_download" color="primary" size="12px" dense>
              <q-list>
                <q-item @click="getPdfFile(value['案件編號'])" v-close-popup clickable bordered>下載為 PDF</q-item>
                <q-item v-for="_paper, i of paper" :key="i" v-close-popup @click="getXmlFile(value['案件編號'], (_paper.type + (_paper.data === '' ? '' : `(${_paper.data})`)))" clickable bordered>
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
  </div>
</template>

<script>
import { defineComponent, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { paper } from './data'
import axios from 'axios'

export default defineComponent({
  name: 'InspectCaseList',
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

    onMounted(() => {
      getInspectCaseList()
    })

    return {
      caseId: ref(''),
      paper,
      router,
      inspectCaseList,
      async getXmlFile (caseId, fileName) {
        try {
          const formData = new FormData()
          formData.append('caseId', caseId)
          formData.append('fileName', fileName)
          const response = await axios.post(process.env.API_URL + '/get_xml_file', formData)

          if (response.data.msg === undefined && typeof response.data === 'string') {
            const link = document.createElement('a')
            link.href = window.URL.createObjectURL(new Blob([response.data], { type: 'text/plain' }))
            link.setAttribute('target', '_blank')
            link.setAttribute('download', fileName + '.xml')
            link.click()
            link.remove()
          } else {
            throw new Error(response.data.msg)
          }
        } catch (err) {
          alert(String(err))
        }
      },
      async getPdfFile (caseId) {
        try {
          const formData = new FormData()
          formData.append('caseId', caseId)
          const response = await axios.post(process.env.API_URL + '/get_inspect_case_pdf', formData, {
            responseType: 'blob'
          })

          if (response.data !== '') {
            const link = document.createElement('a')
            link.href = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }))
            link.setAttribute('target', '_blank')
            link.setAttribute('download', '違規使用山坡地案件現場會勘紀錄表.pdf')
            link.click()
            link.remove()
          } else {
            throw new Error(response.data.msg)
          }
        } catch (err) {
          alert(String(err))
        }
      }
    }
  }
})
</script>
