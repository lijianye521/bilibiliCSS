<script>
import StockChart from '@/components/StockChart.vue'

export default {
  components: {
    StockChart
  },
  data() {
    return {
      columns: [
        { title: '代码', dataIndex: 'code', key: 'code' },
        { title: '名称', dataIndex: 'name', key: 'name' },
        { title: '最新价', dataIndex: 'price', key: 'price' },
        { title: '涨跌幅', dataIndex: 'change', key: 'change' }
      ],
      data: [
        {
          key: '1',
          code: '513180',
          name: '恒生科技指数ETF',
          price: 0.716,
          change: 2.58
        },
        {
          key: '2',
          code: '159740',
          name: '恒生科技30ETF',
          price: 0.703,
          change: 2.18
        }
      ]
    }
  }
}
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
      <a-col :xs="24" :sm="24" :md="14" :lg="16">
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
  margin: 0 !important;  /* 移除 a-row 的默认外边距 */
}

.market-overview,
.chart-card,
.trade-list-card {
  width: 100%;  /* 确保卡片占满容器宽度 */
}

/* 移除 Ant Design 默认的 row 外边距 */
:deep(.ant-row) {
  margin-right: 0 !important;
  margin-left: 0 !important;
}

/* 调整卡片内边距 */
:deep(.ant-card) {
  margin: 0;
}

/* 调整表格宽度 */
:deep(.ant-table-wrapper) {
  width: 100%;
}

/* 确保内容区域有合适的内边距 */
.home {
  padding: 16px;
  box-sizing: border-box;
}
</style>

