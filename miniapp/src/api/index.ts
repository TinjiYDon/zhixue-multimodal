/**
 * API 服务层 - 对接智学多模态后端
 *
 * 后端地址配置：开发时可在微信开发者工具中勾选"不校验合法域名"
 * 正式环境需在小程序后台配置 request 合法域名
 */

// 后端基地址 - 开发环境使用本地地址
// 正式环境替换为实际域名
const BASE_URL = 'http://localhost:8000'

// API 版本前缀
const API_PREFIX = '/api/v1'

interface RequestOptions {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'
  data?: any
  header?: Record<string, string>
}

/**
 * 统一请求封装
 */
function request<T = any>(options: RequestOptions): Promise<T> {
  return new Promise((resolve, reject) => {
    uni.request({
      url: `${BASE_URL}${API_PREFIX}${options.url}`,
      method: options.method || 'GET',
      data: options.data,
      header: {
        'Content-Type': 'application/json',
        ...options.header,
      },
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data as T)
        } else {
          reject(new Error(res.data?.detail || `请求失败 (${res.statusCode})`))
        }
      },
      fail: (err) => {
        reject(new Error(err.errMsg || '网络请求失败'))
      },
    })
  })
}

// ============================================================
// 类型定义
// ============================================================

export interface Course {
  id: string
  title: string
}

export interface AskRequest {
  question: string
}

export interface AskResponse {
  course_id: string
  answer: string
  sources: string[]
}

export interface HealthResponse {
  status: string
  service: string
}

// ============================================================
// API 方法
// ============================================================

/** 健康检查 */
export function healthCheck(): Promise<HealthResponse> {
  return uni.request({
    url: `${BASE_URL}/health`,
    method: 'GET',
  }).then((res: any) => res.data as HealthResponse)
}

/** 获取课程列表 */
export function getCourses(): Promise<Course[]> {
  return request<Course[]>({ url: '/courses' })
}

/** 获取单个课程 */
export function getCourse(courseId: string): Promise<Course> {
  return request<Course>({ url: `/courses/${courseId}` })
}

/** 向课程提问（RAG 问答） */
export function askCourse(courseId: string, question: string): Promise<AskResponse> {
  return request<AskResponse>({
    url: `/courses/${courseId}/ask`,
    method: 'POST',
    data: { question },
  })
}
