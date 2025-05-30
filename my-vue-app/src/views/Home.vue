<script setup>
import StockChart from '@/components/StockChart.vue'
import { ref, onMounted } from 'vue'

// 表格列定义
const columns = [
  { title: '代码', dataIndex: 'code', key: 'code' },
  { title: '名称', dataIndex: 'name', key: 'name' },
  { title: '最新价', dataIndex: 'price', key: 'price' },
  { title: '涨跌幅', dataIndex: 'change', key: 'change' }
]

// 股票数据
const stockData = ref([
  {
    key: '1',
    code: '513180.SH',
    name: '恒生科技指数ETF',
    price: 0.716,
    change: 2.58
  },
  {
    key: '2',
    code: '159740.SZ',
    name: '恒生科技30ETF',
    price: 0.703,
    change: 2.18
  }
])

// 当前选中的股票信息
const currentStock = ref({
  code: '513180.SH',
  price: 0.716,
  change: 2.58
})

// 初始化数据
const initializeData = async () => {
  try {
    // 获取第一支股票的实时数据
    const realtimeResponse = await fetch('/api/realtime?codes=513180.SH&fields=rt_last,rt_pct_chg')
    const realtimeData = await realtimeResponse.json()
    
    if (realtimeData.success) {
      // 更新当前股票信息
      currentStock.value = {
        code: '513180.SH',
        price: realtimeData.data.fields.RT_LAST[0],
        change: realtimeData.data.fields.RT_PCT_CHG[0]
      }
      
      // 更新表格中的数据
      stockData.value = stockData.value.map(item => {
        if (item.code === '513180.SH') {
          return {
            ...item,
            price: realtimeData.data.fields.RT_LAST[0],
            change: realtimeData.data.fields.RT_PCT_CHG[0]
          }
        }
        return item
      })
    }
  } catch (error) {
    console.error('获取实时数据失败:', error)
  }
}

// 组件挂载时获取数据
onMounted(() => {
  initializeData()
})
</script>

<template>
  <div class="home">
    <a-row :gutter="[16, 16]" class="full-width">
      <a-col :xs="24" :sm="24" :md="10" :lg="8">
        <a-card :bordered="false" class="market-overview">
          <template #title>
            <span class="card-title">市场概览</span>
          </template>
          <div class="statistics-wrapper">
            <a-statistic
              title="当前价格"
              :value="currentStock.price"
              :precision="3"
              :value-style="{ color: currentStock.change >= 0 ? '#3f8600' : '#cf1322' }"
            />
            <a-statistic
              title="涨跌幅"
              :value="currentStock.change"
              :precision="2"
              suffix="%"
              :value-style="{ color: currentStock.change >= 0 ? '#3f8600' : '#cf1322' }"
              class="second-statistic"
            />
          </div>
        </a-card>
      </a-col>
      <a-col :xs="24" :sm="24" :md="14" :lg="16">
        <a-card :bordered="false" class="chart-card">
          <StockChart />
        </a-card>
      </a-col>
    </a-row>
    <a-card title="交易列表" :bordered="false" class="trade-list-card">
      <a-table 
        :columns="columns" 
        :data-source="stockData" 
        :pagination="false"
        :scroll="{ x: 'max-content' }"
      >
        <template #bodyCell="{ column, text }">
          <span :style="{ color: text > 0 ? '#3f8600' : '#cf1322' }" v-if="column.dataIndex === 'change'">
            {{ text }}%
          </span>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<style scoped>
.home {
  width: 100%;
  min-width: 0;
}

.full-width {
  width: 100%;
  margin: 0 !important;
}

.market-overview,
.chart-card,
.trade-list-card {
  width: 100%;
}

:deep(.ant-row) {
  margin-right: 0 !important;
  margin-left: 0 !important;
}

:deep(.ant-card) {
  margin: 0;
}

:deep(.ant-table-wrapper) {
  width: 100%;
}

.home {
  padding: 16px;
  box-sizing: border-box;
}

.statistics-wrapper {
  display: flex;
  gap: 24px;
}

.second-statistic {
  margin-left: auto;
}
</style>

