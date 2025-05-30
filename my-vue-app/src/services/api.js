import axios from 'axios'

// 创建axios实例
const api = axios.create({
//   baseURL: 'http://localhost:5000',  // 替换为你的Flask后端地址
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 响应拦截器
api.interceptors.response.use(
  response => {
    const data = response.data
    if (data.code === 500) {
      return Promise.reject(new Error(data.message))
    }
    return data
  },
  error => {
    console.error('API请求错误:', error)
    return Promise.reject(error)
  }
)

// 获取实时数据
export const getRealTimeData = async (code) => {
  try {
    const response = await api.get(`/api/realtime`, {
      params: {
        codes: code,
        fields: 'rt_last,rt_pct_chg'
      }
    })
    return {
      success: true,
      data: {
        fields: {
          RT_LAST: response.data.values?.[0] ?? [],
          RT_PCT_CHG: response.data.values?.[1] ?? []
        }
      }
    }
  } catch (error) {
    console.error('获取实时数据失败:', error)
    return {
      success: false,
      data: null,
      message: error.message
    }
  }
}

// 获取历史K线数据
export const getHistoricalData = async (code, startDate, endDate) => {
  try {
    const response = await api.get(`/api/historical`, {
      params: {
        code,
        start_date: startDate,
        end_date: endDate,
        fields: 'open,high,low,close,volume'
      }
    })
    return {
      success: true,
      data: {
        dates: response.data.dates,
        data: response.data.data,
        fields: response.fields
      }
    }
  } catch (error) {
    console.error('获取K线数据失败:', error)
    return {
      success: false,
      data: null,
      message: error.message
    }
  }
}

export default {
  getRealTimeData,
  getHistoricalData
} 