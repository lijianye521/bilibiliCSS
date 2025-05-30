<script setup>
import StockChart from '@/components/StockChart.vue'
import { ref } from 'vue'

const columns = [
  {
    title: '代码',
    dataIndex: 'code',
    key: 'code',
  },
  {
    title: '名称',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: '最新价',
    dataIndex: 'price',
    key: 'price',
  },
  {
    title: '涨跌幅',
    dataIndex: 'change',
    key: 'change',
  },
]

const data = [
  {
    key: '1',
    code: '513180',
    name: '恒生科技指数ETF',
    price: 0.716,
    change: 2.58,
  },
  {
    key: '2',
    code: '159740',
    name: '恒生科技30ETF',
    price: 0.703,
    change: 2.18,
  },
]
</script>

<template>
  <div class="home">
    <a-row :gutter="[16, 16]" class="full-width">
      <a-col :xs="24" :sm="24" :md="8" :lg="6">
        <a-card :bordered="false" class="market-overview">
          <template #title>
            <span class="card-title">市场概览</span>
          </template>
          <div class="statistics-wrapper">
            <a-statistic
              title="当前价格"
              :value="0.716"
              :precision="3"
              :value-style="{ color: '#3f8600' }"
            />
            <a-statistic
              title="涨跌幅"
              :value="2.58"
              :precision="2"
              suffix="%"
              :value-style="{ color: '#3f8600' }"
              class="second-statistic"
            />
          </div>
        </a-card>
      </a-col>
      <a-col :xs="24" :sm="24" :md="16" :lg="18">
        <a-card :bordered="false" class="chart-card">
          <StockChart />
        </a-card>
      </a-col>
    </a-row>
    <a-card title="交易列表" :bordered="false" class="trade-list-card">
      <a-table 
        :columns="columns" 
        :data-source="data" 
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

.market-overview {
  height: 100%;
}

.statistics-wrapper {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.chart-card {
  height: 100%;
  min-height: 400px;
}

.trade-list-card {
  margin-top: 16px;
}

:deep(.card-title) {
  color: rgba(255, 255, 255, 0.85);
  font-size: 16px;
  font-weight: 500;
}

:deep(.ant-statistic-title) {
  color: rgba(255, 255, 255, 0.45);
}

:deep(.ant-statistic-content) {
  color: rgba(255, 255, 255, 0.85);
}

:deep(.ant-card) {
  background: #1f1f1f;
}

:deep(.ant-table) {
  background: transparent;
}

:deep(.ant-table-thead > tr > th) {
  background: #262626;
  color: rgba(255, 255, 255, 0.85);
  border-bottom: 1px solid #303030;
}

:deep(.ant-table-tbody > tr > td) {
  border-bottom: 1px solid #303030;
  color: rgba(255, 255, 255, 0.85);
}

:deep(.ant-table-tbody > tr:hover > td) {
  background: #262626;
}

:deep(.ant-row) {
  margin-right: 0 !important;
  margin-left: 0 !important;
}

@media (max-width: 768px) {
  .chart-card {
    min-height: 300px;
  }
  
  .statistics-wrapper {
    gap: 12px;
  }
  
  :deep(.ant-card) {
    margin: 0 -8px;
  }
}
</style> 