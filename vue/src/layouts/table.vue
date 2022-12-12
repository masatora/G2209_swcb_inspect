<template>
  <q-list>
    <q-item-label class='text-2xl text-center text-bold p-3'>新北市政府農業局違規使用山坡地案件現場會勘紀錄表</q-item-label>
    <q-item class="grid">
        <q-item-section class="justify-self-end">
            <q-btn color="primary" icon="post_add" @click.prevent="addForm" label="新增表單">
            </q-btn>
        </q-item-section>
    </q-item>
    <q-list bordered class="borders m-3">
      <q-item v-for="contact in contacts" :key="contact.id" class="bg-primary text-white shadow-2 grid grid-cols-12 text-center">
          <q-item-section>
          <q-item-label>{{ contact.projectDateTime }}</q-item-label>
          </q-item-section>
          <q-item-section class="col-span-4">
          <q-item-label>{{ contact.projectName }}</q-item-label>
        </q-item-section>
        <q-item-section>
          <q-item-label>{{ contact.district }}</q-item-label>
        </q-item-section>
        <q-item-section class="col-span-2">
          <q-item-label>{{ contact.mainPerson }}</q-item-label>
        </q-item-section>
        <q-item-section>
          <q-item-label>{{ contact.userName }}</q-item-label>
        </q-item-section>
        <q-item-section>
          <q-item-label>{{ contact.updateDateTime }}</q-item-label>
        </q-item-section>
        <q-item-section class="col-span-2">
          <q-item-label>{{ contact.tool }}</q-item-label>
        </q-item-section>
      </q-item>

      <q-separator />

      <q-item v-for="contact in test" :key="contact.id" class="grid grid-cols-12 border text-center p-5" clickable>
        <q-item-section>
          <q-item-label>{{ contact.projectDateTime }}</q-item-label>
        </q-item-section>
        <q-item-section class="col-span-4">
          <q-item-label>{{ contact.projectName }}</q-item-label>
        </q-item-section>
        <q-item-section>
          <q-item-label>{{ contact.district }}</q-item-label>
        </q-item-section>
        <q-item-section class="col-span-2">
            <q-btn class="gt-xs" size="15px" @click='isShowDialog.mainPerson = true' flat :label="contact.mainPerson" icon="draw">
              <q-dialog v-model='isShowDialog.mainPerson'>
                <q-card class='w-50vw h-50vh'>
                  <q-card-section class='flex justify-end p-2'>
                    <q-btn icon='close' flat round dense v-close-popup />
                  </q-card-section>
                  <q-card-section>
                    <p>請簽名於此處</p>
                  </q-card-section>
                </q-card>
              </q-dialog>
              <q-tooltip>請行為人簽名確認</q-tooltip>
          </q-btn>
        </q-item-section>
        <q-item-section>
          <q-item-label>{{ contact.userName }}</q-item-label>
        </q-item-section>
        <q-item-section>
          <q-item-label>{{ contact.updateDateTime }}</q-item-label>
        </q-item-section>
        <q-item-section class="col-span-2 items-center">
          <div class="text-grey-8 q-gutter-xs">
          <q-btn size="15px" flat round icon="visibility">
            <q-tooltip>檢視</q-tooltip>
          </q-btn>
        <q-btn size="15px" flat round icon="edit">
            <q-tooltip>編輯</q-tooltip>
          </q-btn>
            <q-btn-dropdown color="primary" icon="file_download">
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
  </q-list>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useRouter } from 'vue-router'
import { paper } from './data'
import { test } from './test'
export default defineComponent({
  name: 'MainPage',
  components: {
  },
  setup () {
    const router = useRouter()
    const addForm = () => {
      console.log('------gogo去填表單------')
      router.push({ path: '/form' })
    }
    const contacts = [{
      id: 0,
      projectDateTime: '案件時間',
      projectName: '案由',
      district: '行政區',
      mainPerson: '行為人',
      userName: '填寫者',
      updateDateTime: '更新時間',
      tool: '功能列表'
    }]
    return {
      paper,
      addForm,
      contacts,
      test,
      isShowDialog: ref({
        mainPerson: false
      })
    }
  }
})
</script>
