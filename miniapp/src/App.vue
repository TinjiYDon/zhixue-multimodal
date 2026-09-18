<script setup lang="ts">
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'

onLaunch(() => {
  console.log('智学多模态小程序启动')
})

onShow(() => {
  console.log('小程序显示')
})

onHide(() => {
  console.log('小程序隐藏')
})
</script>

<style lang="scss">
/* 全局样式 */
page {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
    'Helvetica Neue', Arial, sans-serif;
  font-size: 14px;
  color: #333;
  background-color: #f5f5f5;
}
</style>
