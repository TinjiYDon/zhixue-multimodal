/**
 * 小程序运行时配置
 * - 开发：默认 localhost；微信工具勾选「不校验合法域名」
 * - 正式：构建时注入 VITE_API_BASE，或后台合法域名 HTTPS
 */
// @ts-expect-error import.meta.env injected by Vite
const ENV_BASE = (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_BASE) || ''

export const API_PREFIX = '/api/v1'
export const REQUEST_TIMEOUT_MS = 15000

export function getBaseUrl(): string {
  const stored = uni.getStorageSync('zhixue_api_base') as string
  if (stored) return stored.replace(/\/$/, '')
  if (ENV_BASE) return String(ENV_BASE).replace(/\/$/, '')
  return 'http://localhost:8000'
}

export const TOKEN_KEY = 'zhixue_access_token'
export const FLYWHEEL_KEY = 'zhixue_flywheel_opt_in'

export function getToken(): string {
  return (uni.getStorageSync(TOKEN_KEY) as string) || ''
}

export function setToken(token: string) {
  uni.setStorageSync(TOKEN_KEY, token)
}

export function clearToken() {
  uni.removeStorageSync(TOKEN_KEY)
}
