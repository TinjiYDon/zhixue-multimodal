/**
 * API 服务层 - 对接智学多模态后端
 * 统一超时、错误 detail、Bearer 鉴权（Z0/Z1）
 */

import {
  API_PREFIX,
  REQUEST_TIMEOUT_MS,
  clearToken,
  getBaseUrl,
  getToken,
  setToken,
} from './config'

interface RequestOptions {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'
  data?: any
  header?: Record<string, string>
  auth?: boolean
}

function formatDetail(detail: unknown): string {
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail
      .map((d) => (typeof d === 'object' && d && 'msg' in d ? String((d as any).msg) : JSON.stringify(d)))
      .join('; ')
  }
  if (detail && typeof detail === 'object') return JSON.stringify(detail)
  return ''
}

function request<T = any>(options: RequestOptions): Promise<T> {
  const needAuth = options.auth !== false
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...options.header,
  }
  const token = getToken()
  if (needAuth && token) {
    headers.Authorization = `Bearer ${token}`
  }

  return new Promise((resolve, reject) => {
    uni.request({
      url: `${getBaseUrl()}${API_PREFIX}${options.url}`,
      method: options.method || 'GET',
      data: options.data,
      header: headers,
      timeout: REQUEST_TIMEOUT_MS,
      success: (res) => {
        const data: any = res.data
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(data as T)
          return
        }
        if (res.statusCode === 401) {
          clearToken()
        }
        const msg = formatDetail(data?.detail) || data?.message || `请求失败 (${res.statusCode})`
        reject(new Error(msg))
      },
      fail: (err) => {
        const raw = err.errMsg || ''
        if (/timeout/i.test(raw)) {
          reject(new Error('请求超时，请检查网络后重试'))
        } else {
          reject(new Error(raw || '网络请求失败'))
        }
      },
    })
  })
}

export interface Course {
  id: string
  title: string
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

export interface LoginResponse {
  access_token: string
  token_type: string
  expires_in: number
  user_id: string
}

export function healthCheck(): Promise<HealthResponse> {
  return new Promise((resolve, reject) => {
    uni.request({
      url: `${getBaseUrl()}/health`,
      method: 'GET',
      timeout: REQUEST_TIMEOUT_MS,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data as HealthResponse)
        } else {
          reject(new Error(`健康检查失败 (${res.statusCode})`))
        }
      },
      fail: (err) => reject(new Error(err.errMsg || '网络请求失败')),
    })
  })
}

/** 开发：用 dev code；正式：wx.login 取 code 再调本方法 */
export async function loginWithCode(code: string): Promise<LoginResponse> {
  const body = await request<LoginResponse>({
    url: '/auth/login',
    method: 'POST',
    data: { code },
    auth: false,
  })
  setToken(body.access_token)
  return body
}

export async function ensureLogin(): Promise<void> {
  if (getToken()) return
  // 微信环境优先 wx.login；失败则用本地 dev code（仅开发）
  try {
    const wxLogin = await new Promise<UniApp.LoginRes>((resolve, reject) => {
      uni.login({
        provider: 'weixin',
        success: resolve,
        fail: reject,
      })
    })
    if (wxLogin.code) {
      await loginWithCode(wxLogin.code)
      return
    }
  } catch {
    // fall through
  }
  await loginWithCode(`dev-${Date.now()}`)
}

export function logout(): Promise<{ status: string }> {
  return request({ url: '/auth/logout', method: 'POST' }).finally(() => clearToken())
}

export function deleteAccount(): Promise<{ status: string; message?: string }> {
  return request({ url: '/auth/me', method: 'DELETE' }).finally(() => clearToken())
}

export function getCourses(): Promise<Course[]> {
  return request<Course[]>({ url: '/courses', auth: false })
}

export function getCourse(courseId: string): Promise<Course> {
  return request<Course>({ url: `/courses/${courseId}`, auth: false })
}

export async function askCourse(courseId: string, question: string): Promise<AskResponse> {
  await ensureLogin()
  return request<AskResponse>({
    url: `/courses/${courseId}/ask`,
    method: 'POST',
    data: { question },
  })
}
