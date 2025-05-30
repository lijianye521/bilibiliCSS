import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 响应拦截器
api.interceptors.response.use(
  response => {
    if (response.data.success) {
      return response.data
    }
    return Promise.reject(new Error(response.data.error || '请求失败'))
  },
  error => {
    console.error('API请求错误:', error)
    return Promise.reject(error)
  }
)

// 获取实时行情数据
export const getRealTimeData = (codes, fields = 'rt_last,rt_pct_chg') => {
  return api.get('/realtime', {
    params: { codes, fields }
  })
}

// 获取历史行情数据
export const getHistoricalData = (code, fields = 'open,high,low,close,volume') => {
  const today = new Date()
  const endDate = today.toISOString().split('T')[0]
  // 获取一年前的日期
  const startDate = new Date(today)
  startDate.setFullYear(today.getFullYear() - 1)
  
  return api.get('/historical', {
    params: {
      code,
      fields,
      start_date: startDate.toISOString().split('T')[0],
      end_date: endDate
    }
  })
}

export default {
  getRealTimeData,
  getHistoricalData
} 