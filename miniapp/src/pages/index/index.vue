<!--
  课程列表页 - 对接 GET /api/v1/courses
  展示所有课程，点击进入课程详情问答页
-->
<template>
  <view class="course-list-page">
    <!-- 顶部状态栏 -->
    <view class="header">
      <view class="header-title">智学多模态</view>
      <view class="header-subtitle">课程列表</view>
    </view>

    <!-- 加载状态 -->
    <view v-if="loading" class="loading-container">
      <view class="loading-spinner"></view>
      <text class="loading-text">加载中...</text>
    </view>

    <!-- 错误状态 -->
    <view v-else-if="error" class="error-container">
      <text class="error-icon">!</text>
      <text class="error-text">{{ error }}</text>
      <button class="retry-btn" @tap="fetchCourses">重试</button>
    </view>

    <!-- 空状态 -->
    <view v-else-if="courses.length === 0" class="empty-container">
      <text class="empty-icon">📚</text>
      <text class="empty-text">暂无课程</text>
      <text class="empty-hint">请先在后端创建课程</text>
    </view>

    <!-- 课程列表 -->
    <view v-else class="course-list">
      <view
        v-for="course in courses"
        :key="course.id"
        class="course-card"
        @tap="goToCourse(course)"
      >
        <view class="course-card-id">课程 {{ course.id }}</view>
        <view class="course-card-title">{{ course.title }}</view>
        <view class="course-card-arrow">→</view>
      </view>
    </view>

    <!-- 底部提示 -->
    <view class="footer-hint">
      <text>健康状态：</text>
      <text :class="healthOk ? 'health-ok' : 'health-err'">
        {{ healthOk ? '正常' : '未连接' }}
      </text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getCourses, healthCheck, type Course } from '@/api/index'

const courses = ref<Course[]>([])
const loading = ref(true)
const error = ref('')
const healthOk = ref(false)

async function checkHealth() {
  try {
    await healthCheck()
    healthOk.value = true
  } catch {
    healthOk.value = false
  }
}

async function fetchCourses() {
  loading.value = true
  error.value = ''
  try {
    courses.value = await getCourses()
  } catch (e: any) {
    error.value = e.message || '获取课程列表失败'
  } finally {
    loading.value = false
  }
}

function goToCourse(course: Course) {
  uni.navigateTo({
    url: `/pages/course/index?id=${course.id}&title=${encodeURIComponent(course.title)}`,
  })
}

onMounted(() => {
  checkHealth()
  fetchCourses()
})
</script>

<style lang="scss" scoped>
.course-list-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 60px;
}

.header {
  background: linear-gradient(135deg, #4a6cf7 0%, #6c63ff 100%);
  padding: 40px 20px 24px;
  color: #fff;

  .header-title {
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 4px;
  }

  .header-subtitle {
    font-size: 13px;
    opacity: 0.85;
  }
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;

  .loading-spinner {
    width: 36px;
    height: 36px;
    border: 3px solid #e5e5e5;
    border-top-color: #4a6cf7;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  .loading-text {
    margin-top: 12px;
    color: #999;
    font-size: 14px;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;

  .error-icon {
    width: 48px;
    height: 48px;
    line-height: 48px;
    text-align: center;
    background: #ff4d4f;
    color: #fff;
    border-radius: 50%;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 12px;
  }

  .error-text {
    color: #666;
    font-size: 14px;
    margin-bottom: 16px;
  }

  .retry-btn {
    padding: 8px 24px;
    background: #4a6cf7;
    color: #fff;
    border-radius: 20px;
    font-size: 14px;
    border: none;
  }
}

.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 80px 20px;

  .empty-icon {
    font-size: 48px;
    margin-bottom: 12px;
  }

  .empty-text {
    font-size: 16px;
    color: #666;
    margin-bottom: 4px;
  }

  .empty-hint {
    font-size: 13px;
    color: #999;
  }
}

.course-list {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.course-card {
  background: #fff;
  border-radius: 12px;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  transition: all 0.2s;

  &:active {
    transform: scale(0.98);
    background: #f8f9ff;
  }

  .course-card-id {
    width: 40px;
    height: 40px;
    line-height: 40px;
    text-align: center;
    background: #eef0ff;
    color: #4a6cf7;
    border-radius: 10px;
    font-size: 12px;
    font-weight: 600;
    flex-shrink: 0;
  }

  .course-card-title {
    flex: 1;
    font-size: 16px;
    font-weight: 500;
    color: #333;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .course-card-arrow {
    color: #ccc;
    font-size: 18px;
    flex-shrink: 0;
  }
}

.footer-hint {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  text-align: center;
  padding: 12px;
  font-size: 12px;
  color: #999;
  background: #f5f5f5;

  .health-ok {
    color: #4cd964;
  }

  .health-err {
    color: #ff4d4f;
  }
}
</style>
