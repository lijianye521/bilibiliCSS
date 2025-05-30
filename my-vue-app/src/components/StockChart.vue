<template>
  <div ref="chartContainer" class="stock-chart-container"></div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount, nextTick } from 'vue';
import * as echarts from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { CandlestickChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DataZoomComponent,
  LegendComponent,
  MarkLineComponent,
  MarkPointComponent,
  ToolboxComponent
} from 'echarts/components';
import axios from 'axios';
import dayjs from 'dayjs';

echarts.use([
  CanvasRenderer,
  CandlestickChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DataZoomComponent,
  LegendComponent,
  MarkLineComponent,
  MarkPointComponent,
  ToolboxComponent
]);

const props = defineProps({
  code: {
    type: String,
    default: '513180.SH', // 设置默认股票代码
  },
  timeframe: {
    type: String,
    default: 'D',
  },
  limit: {
    type: Number,
    default: 100,
  }
});

const chartContainer = ref(null);
let chartInstance = null;
const loading = ref(false);
const error = ref(null);

const fetchData = async () => {
  if (!props.code) return;
  loading.value = true;
  error.value = null;
  try {
    // 获取当前日期和一年前的日期
    const endDate = dayjs().format('YYYY-MM-DD');
    const startDate = dayjs().subtract(1, 'year').format('YYYY-MM-DD');

    // 使用Flask后端的historical接口
    const response = await fetch(`/api/historical?code=${props.code}&start_date=${startDate}&end_date=${endDate}&fields=open,high,low,close,volume`);
    const result = await response.json();

    if (result.success && result.data) {
      await nextTick(); // 确保容器已准备好
      if (chartInstance) {
        updateChart(result.data);
      } else {
        initChart(result.data);
      }
    } else {
      throw new Error(result.message || '获取K线数据失败');
    }
  } catch (err) {
    console.error('获取K线数据失败:', err);
    error.value = err.message;
    if (chartInstance) {
      chartInstance.clear(); // 出错时清空图表
    }
  } finally {
    loading.value = false;
  }
};

const processData = (rawData) => {
  if (!rawData || !Array.isArray(rawData.dates) || rawData.dates.length === 0) {
    return {
      categoryData: [],
      values: [],
      volumes: []
    };
  }

  const categoryData = rawData.dates;
  const values = [];
  const volumes = [];

  // 数据格式: data[i] = [open, high, low, close, volume]
  rawData.data.forEach((item, i) => {
    values.push([
      item[0], // 开盘价
      item[3], // 收盘价
      item[2], // 最低价
      item[1]  // 最高价
    ]);
    
    // 计算涨跌
    const isUp = item[3] >= item[0]; // 收盘价 >= 开盘价
    volumes.push([
      i,
      item[4], // 成交量
      isUp ? 1 : -1
    ]);
  });

  return { categoryData, values, volumes };
};


const getOption = (processedData) => {
  const { categoryData, values, volumes } = processedData;

  return {
    backgroundColor: 'transparent',
    animation: true,
    legend: {
      bottom: 10,
      left: 'center',
      data: ['K线', '成交量'],
      textStyle: {
        color: '#ccc'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      },
      backgroundColor: 'rgba(24,24,24,0.8)',
      borderColor: '#333',
      textStyle: { color: '#ccc' },
      formatter: function(params) {
        const candlestick = params[0];
        const volume = params[1];
        return `
          <div style="font-size: 14px; color: #ccc;">
            <div style="margin: 5px 0;">日期：${candlestick.name}</div>
            <div>开盘：${candlestick.data[0]}</div>
            <div>收盘：${candlestick.data[1]}</div>
            <div>最低：${candlestick.data[2]}</div>
            <div>最高：${candlestick.data[3]}</div>
            <div>成交量：${volume ? (volume.data[1] / 10000).toFixed(2) + '万' : '-'}</div>
          </div>
        `;
      }
    },
    axisPointer: {
      link: [{ xAxisIndex: 'all' }],
      label: {
        backgroundColor: '#777'
      }
    },
    toolbox: {
      show: true,
      feature: {
        dataZoom: {
          yAxisIndex: false,
          title: { zoom: '区域缩放', back: '区域还原' }
        },
        restore: { title: '还原' },
        saveAsImage: { title: '保存为图片', backgroundColor: '#1f1f1f' }
      },
      iconStyle: {
        borderColor: '#ccc'
      },
      top: 0,
      right: 30
    },
    grid: [
      {
        left: '10%',
        right: '8%',
        top: '15%',
        height: '50%',
        containLabel: false
      },
      {
        left: '10%',
        right: '8%',
        top: '70%',
        height: '16%',
        containLabel: false
      }
    ],
    xAxis: [
      {
        type: 'category',
        data: categoryData,
        boundaryGap: false,
        axisLine: { lineStyle: { color: '#555' } },
        axisLabel: {
          color: '#ccc',
          formatter: function(value) {
            return value.substring(5); // 只显示月-日
          }
        },
        min: 'dataMin',
        max: 'dataMax',
        axisPointer: {
          show: true
        }
      },
      {
        type: 'category',
        gridIndex: 1,
        data: categoryData,
        boundaryGap: false,
        axisLine: { lineStyle: { color: '#555' } },
        axisLabel: { show: false },
        splitLine: { show: false },
        axisTick: { show: false },
        min: 'dataMin',
        max: 'dataMax'
      }
    ],
    yAxis: [
      {
        scale: true,
        position: 'right',
        splitLine: { lineStyle: { color: '#2a2a2a' } },
        axisLabel: {
          color: '#ccc',
          formatter: '{value}'
        },
        axisLine: { lineStyle: { color: '#555' } }
      },
      {
        scale: true,
        gridIndex: 1,
        splitNumber: 2,
        axisLabel: {
          show: true,
          color: '#ccc',
          formatter: function(value) {
            if (value >= 100000000) return (value / 100000000).toFixed(1) + '亿';
            if (value >= 10000) return (value / 10000).toFixed(1) + '万';
            return value;
          }
        },
        axisLine: { lineStyle: { color: '#555' } },
        splitLine: { show: false },
        axisTick: { show: false },
        position: 'right'
      }
    ],
    dataZoom: [
      {
        type: 'inside',
        xAxisIndex: [0, 1],
        start: 80,
        end: 100
      },
      {
        show: true,
        type: 'slider',
        xAxisIndex: [0, 1],
        bottom: 40,
        start: 80,
        end: 100,
        height: 20,
        borderColor: '#333',
        fillerColor: 'rgba(120, 120, 120, 0.3)',
        handleIcon: 'path://M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
        handleSize: '100%',
        handleStyle: {
          color: '#aaa',
          shadowBlur: 3,
          shadowColor: 'rgba(0, 0, 0, 0.6)',
          shadowOffsetX: 2,
          shadowOffsetY: 2
        },
        textStyle: {
          color: '#ccc'
        }
      }
    ],
    series: [
      {
        name: 'K线',
        type: 'candlestick',
        data: values,
        itemStyle: {
          color: '#ef232a',
          color0: '#14b143',
          borderColor: '#ef232a',
          borderColor0: '#14b143',
          opacity: 0.8
        },
        markPoint: {
          data: [
            { type: 'max', name: '最高值', valueDim: 'highest' },
            { type: 'min', name: '最低值', valueDim: 'lowest' }
          ],
          label: {
            color: '#000',
            backgroundColor: '#ddd',
            borderColor: '#ddd',
            borderRadius: 4,
            padding: [4, 6]
          }
        },
        markLine: {
          data: [
            { type: 'average', name: '平均值' }
          ],
          label: {
            color: '#fff',
            backgroundColor: '#555',
            borderColor: '#555',
            borderRadius: 4,
            padding: [2, 4]
          },
          lineStyle: {
            type: 'dashed',
            color: '#555'
          }
        }
      },
      {
        name: '成交量',
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: volumes,
        itemStyle: {
          color: (params) => (params.data[2] > 0 ? '#ef232a' : '#14b143'),
          opacity: 0.7
        }
      }
    ]
  };
};


const initChart = (apiData) => {
  if (!chartContainer.value) return;
  const processedData = processData(apiData);
  if (processedData.categoryData.length === 0) {
    console.warn('No data to display in chart.');
    if(chartInstance) chartInstance.clear();
    // Optionally display a message in the chart container
    chartContainer.value.innerHTML = '<p style="color: #ccc; text-align: center; padding-top: 20px;">暂无数据</p>';
    return;
  }
  chartContainer.value.innerHTML = ''; // Clear any 'no data' message

  chartInstance = echarts.init(chartContainer.value, 'dark'); // 'dark' theme can be applied here
  chartInstance.setOption(getOption(processedData));
};

const updateChart = (apiData) => {
  if (!chartInstance) {
    initChart(apiData); // Initialize if not already
    return;
  }
  const processedData = processData(apiData);
   if (processedData.categoryData.length === 0) {
    console.warn('No data to display in chart for update.');
    chartInstance.clear();
    chartContainer.value.innerHTML = '<p style="color: #ccc; text-align: center; padding-top: 20px;">暂无数据</p>';
    return;
  }
  chartContainer.value.innerHTML = ''; // Clear any 'no data' message

  chartInstance.setOption(getOption(processedData), { notMerge: false }); // notMerge: false is important for dynamic data
};

let resizeObserver;

onMounted(() => {
  fetchData();
  if (chartContainer.value) {
    resizeObserver = new ResizeObserver(() => {
      if (chartInstance) {
        chartInstance.resize();
      }
    });
    resizeObserver.observe(chartContainer.value);
  }
});

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.dispose();
    chartInstance = null;
  }
  if (resizeObserver && chartContainer.value) {
    resizeObserver.unobserve(chartContainer.value);
  }
});

watch(() => [props.code, props.timeframe, props.limit], () => {
  fetchData();
}, { immediate: false }); // 'immediate: false' to avoid double fetch on mount if fetchData is already called in onMounted


// Expose fetchData for parent component to trigger refresh if needed
defineExpose({
  refreshChart: fetchData
});

</script>

<style scoped>
.stock-chart-container {
  width: 100%;
  height: 500px; /* Default height, can be overridden by parent */
  min-height: 300px;
}
</style> 