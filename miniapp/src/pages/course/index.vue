<!--
  课程详情页 - 对接 GET /api/v1/courses/{id} 和 POST /api/v1/courses/{id}/ask
  展示课程信息并提供问答功能
-->
<template>
  <view class="course-detail-page">
    <!-- 课程信息头 -->
    <view class="course-header">
      <view class="course-id">课程 {{ courseId }}</view>
      <view class="course-title">{{ courseTitle }}</view>
    </view>

    <!-- 问答区域 -->
    <view class="qa-section">
      <view class="qa-section-title">课程问答</view>

      <!-- 对话历史 -->
      <scroll-view class="qa-messages" scroll-y :scroll-top="scrollTop">
        <!-- 欢迎提示 -->
        <view v-if="messages.length === 0" class="welcome-tip">
          <text class="welcome-icon">💡</text>
          <text class="welcome-text">
            向我提问本课程相关问题，我会基于课程内容为你解答
          </text>
        </view>

        <!-- 消息列表 -->
        <view
          v-for="(msg, idx) in messages"
          :key="idx"
          :class="['message', msg.role === 'user' ? 'message-user' : 'message-ai']"
        >
          <view class="message-avatar">
            {{ msg.role === 'user' ? '我' : 'AI' }}
          </view>
          <view class="message-content">
            <text class="message-text">{{ msg.content }}</text>
            <!-- AI 回答的来源引用 -->
            <view v-if="msg.sources && msg.sources.length > 0" class="message-sources">
              <text class="sources-label">参考来源：</text>
              <text
                v-for="(src, si) in msg.sources"
                :key="si"
                class="source-item"
              >
                {{ src }}
              </text>
            </view>
          </view>
        </view>

        <!-- 加载指示器 -->
        <view v-if="asking" class="message message-ai">
          <view class="message-avatar">AI</view>
          <view class="message-content">
            <view class="typing-dots">
              <view class="dot"></view>
              <view class="dot"></view>
              <view class="dot"></view>
            </view>
          </view>
        </view>
      </scroll-view>

      <!-- 输入区域 -->
      <view class="qa-input-area">
        <input
          v-model="questionInput"
          class="qa-input"
          type="text"
          placeholder="输入你的问题..."
          confirm-type="send"
          :disabled="asking"
          @confirm="askQuestion"
        />
        <button
          class="qa-send-btn"
          :disabled="!questionInput.trim() || asking"
          @tap="askQuestion"
        >
          发送
        </button>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getCourse, askCourse, type AskResponse } from '@/api/index'

interface ChatMessage {
  role: 'user' | 'ai'
  content: string
  sources?: string[]
}

const courseId = ref('')
const courseTitle = ref('')
const questionInput = ref('')
const asking = ref(false)
const messages = ref<ChatMessage[]>([])
const scrollTop = ref(0)

onLoad((options: any) => {
  courseId.value = options.id || ''
  courseTitle.value = decodeURIComponent(options.title || '')

  // 加载课程详情
  if (courseId.value) {
    fetchCourseDetail()
  }
})

async function fetchCourseDetail() {
  try {
    const course = await getCourse(courseId.value)
    courseTitle.value = course.title
    uni.setNavigationBarTitle({ title: course.title })
  } catch {
    console.error('获取课程详情失败')
  }
}

async function askQuestion() {
  const question = questionInput.value.trim()
  if (!question || asking.value) return

  // 添加用户消息
  messages.value.push({ role: 'user', content: question })
  questionInput.value = ''
  asking.value = true

  // 滚动到底部
  scrollToBottom()

  try {
    const result: AskResponse = await askCourse(courseId.value, question)
    messages.value.push({
      role: 'ai',
      content: result.answer,
      sources: result.sources,
    })
  } catch (e: any) {
    messages.value.push({
      role: 'ai',
      content: `抱歉，问答服务暂时不可用：${e.message || '未知错误'}`,
    })
  } finally {
    asking.value = false
    scrollToBottom()
  }
}

function scrollToBottom() {
  nextTick(() => {
    scrollTop.value = 99999
  })
}
</script>

<style lang="scss" scoped>
.course-detail-page {
  min-height: 100vh;
  background: #f5f5f5;
  display: flex;
  flex-direction: column;
}

.course-header {
  background: linear-gradient(135deg, #4a6cf7 0%, #6c63ff 100%);
  padding: 16px 20px;
  color: #fff;

  .course-id {
    font-size: 12px;
    opacity: 0.75;
    margin-bottom: 4px;
  }

  .course-title {
    font-size: 18px;
    font-weight: 600;
  }
}

.qa-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;

  .qa-section-title {
    padding: 12px 20px;
    font-size: 14px;
    font-weight: 600;
    color: #666;
    background: #fff;
    border-bottom: 1px solid #f0f0f0;
  }
}

.qa-messages {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.welcome-tip {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;

  .welcome-icon {
    font-size: 40px;
    margin-bottom: 12px;
  }

  .welcome-text {
    font-size: 14px;
    color: #999;
    text-align: center;
    line-height: 1.6;
  }
}

.message {
  display: flex;
  margin-bottom: 16px;

  .message-avatar {
    width: 36px;
    height: 36px;
    line-height: 36px;
    text-align: center;
    border-radius: 50%;
    font-size: 12px;
    font-weight: 600;
    flex-shrink: 0;
    margin-top: 2px;
  }

  .message-content {
    max-width: 75%;
    padding: 10px 14px;
    border-radius: 12px;
    font-size: 14px;
    line-height: 1.6;
    word-break: break-all;
  }

  .message-text {
    white-space: pre-wrap;
  }

  .message-sources {
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid rgba(0, 0, 0, 0.06);

    .sources-label {
      font-size: 11px;
      color: #999;
    }

    .source-item {
      display: block;
      font-size: 11px;
      color: #666;
      margin-top: 2px;
      padding-left: 8px;
      border-left: 2px solid #ddd;
    }
  }
}

.message-user {
  flex-direction: row-reverse;

  .message-avatar {
    background: #4a6cf7;
    color: #fff;
    margin-left: 10px;
  }

  .message-content {
    background: #4a6cf7;
    color: #fff;
    border-bottom-right-radius: 4px;
  }
}

.message-ai {
  .message-avatar {
    background: #e8eaed;
    color: #555;
    margin-right: 10px;
  }

  .message-content {
    background: #fff;
    color: #333;
    border-bottom-left-radius: 4px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
  }
}

.typing-dots {
  display: flex;
  gap: 4px;
  padding: 4px 0;

  .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #ccc;
    animation: typing 1.4s infinite ease-in-out both;

    &:nth-child(1) {
      animation-delay: -0.32s;
    }

    &:nth-child(2) {
      animation-delay: -0.16s;
    }
  }
}

@keyframes typing {
  0%,
  80%,
  100% {
    transform: scale(0.6);
    opacity: 0.4;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.qa-input-area {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: #fff;
  border-top: 1px solid #f0f0f0;
  padding-bottom: calc(12px + env(safe-area-inset-bottom));

  .qa-input {
    flex: 1;
    height: 38px;
    padding: 0 14px;
    background: #f5f5f5;
    border-radius: 20px;
    font-size: 14px;
    border: 1px solid #eee;

    &:focus {
      border-color: #4a6cf7;
      background: #fff;
    }
  }

  .qa-send-btn {
    padding: 0 18px;
    height: 38px;
    line-height: 38px;
    background: #4a6cf7;
    color: #fff;
    border-radius: 20px;
    font-size: 14px;
    border: none;
    flex-shrink: 0;

    &[disabled] {
      background: #ccc;
      color: #fff;
    }
  }
}
</style>
