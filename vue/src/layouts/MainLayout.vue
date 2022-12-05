<template>
  <q-list>
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
        <q-input readonly filled dense>
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
    <q-expansion-item class="text-lg text-bold" expand-separator icon="perm_identity" label="會勘單位與人員">
      <q-card>
        <q-card-section>
          <q-item>
            <q-item-section>
              <q-select v-model="inspectRecord['本府區公所']" :options="['中和區', '永和區', '板橋區']" label="請選擇本府區公所" filled dense />
            </q-item-section>
            <q-item-section side>
              <q-btn icon="edit" color="grey-3" class="text-grey-7" @click="isShowDialog.district = true" dense />
              <q-dialog v-model="isShowDialog.district">
                <q-card class="w-50vw h-50vh">
                  <q-card-section class="flex justify-end p-2">
                    <q-btn icon="close" flat round dense v-close-popup />
                  </q-card-section>
                  <q-card-section>
                    <p>請簽名於此處</p>
                  </q-card-section>
                </q-card>
              </q-dialog>
            </q-item-section>
          </q-item>
        </q-card-section>
      </q-card>
    </q-expansion-item>
  </q-list>
</template>

<script>
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'MainLayout',
  components: {
  },
  setup () {
    return {
      isShowDialog: ref({
        district: false
      }),
      inspectRecord: ref({
        案由: '',
        時間: '',
        本府區公所: ''
      })
    }
  }
})
</script>
