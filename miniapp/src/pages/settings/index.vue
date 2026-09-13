<template>
  <view class="page">
    <view class="title">设置</view>

    <view class="card">
      <view class="row" @tap="doLogin">
        <text>登录 / 刷新会话</text>
        <text class="muted">{{ loggedIn ? '已登录' : '未登录' }}</text>
      </view>
      <view class="row" @tap="doLogout">
        <text>退出登录</text>
      </view>
      <view class="row danger" @tap="doDelete">
        <text>注销账号</text>
      </view>
    </view>

    <view class="card">
      <view class="row" @tap="goPrivacy"><text>隐私政策</text></view>
      <view class="row" @tap="goTerms"><text>用户协议</text></view>
    </view>

    <view class="card">
      <view class="row">
        <text>帮助改进智学（飞轮）</text>
        <switch :checked="flywheel" @change="onFlywheel" color="#4a6cf7" />
      </view>
      <text class="hint">默认关闭；提审通过并阅读隐私政策后再开启。</text>
    </view>

    <view class="hint">API：{{ apiBase }}</view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { deleteAccount, ensureLogin, logout } from '@/api/index'
import { FLYWHEEL_KEY, getBaseUrl, getToken } from '@/config'

const loggedIn = ref(false)
const flywheel = ref(false)
const apiBase = ref(getBaseUrl())

function refresh() {
  loggedIn.value = !!getToken()
  flywheel.value = !!uni.getStorageSync(FLYWHEEL_KEY)
  apiBase.value = getBaseUrl()
}

onMounted(() => refresh())

async function doLogin() {
  try {
    await ensureLogin()
    uni.showToast({ title: '已登录', icon: 'success' })
    refresh()
  } catch (e: any) {
    uni.showToast({ title: e.message || '登录失败', icon: 'none' })
  }
}

async function doLogout() {
  try {
    await logout()
  } catch {
    // ignore
  }
  refresh()
  uni.showToast({ title: '已退出', icon: 'none' })
}

function doDelete() {
  uni.showModal({
    title: '确认注销？',
    content: '将清除本机会话并调用服务端注销接口。',
    success: async (res) => {
      if (!res.confirm) return
      try {
        await ensureLogin()
        await deleteAccount()
        uni.showToast({ title: '已注销', icon: 'success' })
        refresh()
      } catch (e: any) {
        uni.showToast({ title: e.message || '注销失败', icon: 'none' })
      }
    },
  })
}

function onFlywheel(e: any) {
  const on = !!e.detail.value
  if (on) {
    uni.showModal({
      title: '开启使用反馈？',
      content: '仅在同意隐私政策后用于改进问答与转写质量，可随时关闭。',
      success: (res) => {
        if (res.confirm) {
          uni.setStorageSync(FLYWHEEL_KEY, '1')
          flywheel.value = true
        } else {
          flywheel.value = false
        }
      },
    })
  } else {
    uni.removeStorageSync(FLYWHEEL_KEY)
    flywheel.value = false
  }
}

function goPrivacy() {
  uni.navigateTo({ url: '/pages/legal/privacy' })
}

function goTerms() {
  uni.navigateTo({ url: '/pages/legal/terms' })
}
</script>

<style scoped>
.page { padding: 24rpx; background: #f5f5f5; min-height: 100vh; }
.title { font-size: 40rpx; font-weight: 700; margin-bottom: 24rpx; }
.card { background: #fff; border-radius: 16rpx; margin-bottom: 24rpx; overflow: hidden; }
.row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 28rpx 24rpx;
  border-bottom: 1px solid #f0f0f0;
  font-size: 30rpx;
}
.row:last-child { border-bottom: none; }
.danger { color: #ff4d4f; }
.muted { color: #999; font-size: 26rpx; }
.hint { color: #999; font-size: 24rpx; padding: 0 8rpx 16rpx; line-height: 1.5; }
</style>
