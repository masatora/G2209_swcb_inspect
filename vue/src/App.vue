<template>
  <router-view />
</template>

<script>
import 'virtual:windi.css'
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'App'
})
</script>

<style lang="sass">
html, body, #q-app
  width: 100%
  height: 100%
  padding: 0
  margin: 0
</style>
