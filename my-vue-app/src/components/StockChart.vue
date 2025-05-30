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
    required: true,
  },
  timeframe: {
    type: String,
    default: 'D', // D for daily, W for weekly, M for monthly, or minute intervals like '60'
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
    const response = await axios.get('/api/stock/kline', {
      params: {
        code: props.code,
        timeframe: props.timeframe,
        limit: props.limit,
      },
    });

    if (response.data.success && response.data.data) {
      await nextTick(); // Ensure the container is ready
      if (chartInstance) {
        updateChart(response.data.data);
      } else {
        initChart(response.data.data);
      }
    } else {
      throw new Error(response.data.message || 'Failed to fetch K-line data');
    }
  } catch (err) {
    console.error('Error fetching K-line data:', err);
    error.value = err.message;
    if (chartInstance) {
      chartInstance.clear(); // Clear chart on error
    }
  } finally {
    loading.value = false;
  }
};

const processData = (rawData) => {
  if (!rawData || !Array.isArray(rawData.times) || rawData.times.length === 0) {
    return {
      categoryData: [],
      values: [],
      volumes: [],
    };
  }

  const categoryData = rawData.times.map(timeStr => {
    // Assuming timeStr is like "YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS"
    // ECharts can parse this directly, but ensure format consistency with API
    return timeStr.split(' ')[0]; // Use only date part for daily/weekly/monthly for simplicity
  });

  const values = [];
  const volumes = [];

  for (let i = 0; i < rawData.times.length; i++) {
    values.push([
      rawData.fields.OPEN[i],
      rawData.fields.CLOSE[i],
      rawData.fields.LOW[i],
      rawData.fields.HIGH[i],
    ]);
    volumes.push([i, rawData.fields.VOLUME[i], rawData.fields.CLOSE[i] > rawData.fields.OPEN[i] ? 1 : -1]);
  }
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
      data: ['K-Line', 'Volume'],
      textStyle: {
        color: '#ccc'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
      },
      backgroundColor: 'rgba(24,24,24,0.8)',
      borderColor: '#333',
      textStyle: { color: '#ccc' },
      position: function (pos, params, el, elRect, size) {
        const obj = { top: 10 };
        obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
        return obj;
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
          title: { zoom: 'Area Zoom', back: 'Restore Area Zoom' }
        },
        restore: { title: 'Restore' },
        saveAsImage: { title: 'Save as Image', backgroundColor: '#1f1f1f' }
      },
      iconStyle: {
        borderColor: '#ccc'
      },
      top: 0,
      right: 30,
    },
    grid: [
      { // K-line chart
        left: '10%',
        right: '8%',
        top: '15%',
        height: '50%',
        containLabel: false
      },
      { // Volume chart
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
        axisLabel: { color: '#ccc' },
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
        splitLine: { show: false },
        axisTick: { show: false },
        axisLabel: { show: false },
        min: 'dataMin',
        max: 'dataMax',
      }
    ],
    yAxis: [
      {
        scale: true,
        axisLine: { lineStyle: { color: '#555' } },
        splitLine: { lineStyle: { color: '#2a2a2a' } },
        axisLabel: { color: '#ccc', formatter: '{value}' }
      },
      {
        scale: true,
        gridIndex: 1,
        splitNumber: 2,
        axisLabel: { 
          show: true,
          color: '#ccc',
          formatter: function (value) {
            if (value >= 100000000) return (value / 100000000).toFixed(1) + '亿';
            if (value >= 10000) return (value / 10000).toFixed(1) + '万';
            return value;
          }
        },
        axisLine: { lineStyle: { color: '#555' } },
        splitLine: { show: false },
        axisTick: { show: false },
      }
    ],
    dataZoom: [
      {
        type: 'inside',
        xAxisIndex: [0, 1],
        start: 70,
        end: 100
      },
      {
        show: true,
        type: 'slider',
        xAxisIndex: [0, 1],
        bottom: 40,
        start: 70,
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
        name: 'K-Line',
        type: 'candlestick',
        data: values,
        itemStyle: {
          color: '#ef232a', // red for up
          color0: '#14b143', // green for down
          borderColor: '#ef232a',
          borderColor0: '#14b143',
          opacity: 0.8,
        },
        markPoint: {
          data: [
            { type: 'max', name: 'Max' },
            { type: 'min', name: 'Min' }
          ],
          itemStyle: { color: '#ddd'},
          label: {
            color: '#000',
            backgroundColor: '#ddd',
            borderColor: '#ddd',
            borderRadius: 4,
            padding: [4,6]
          }
        },
        markLine: {
            data: [
                { type: 'average', name: 'Avg' }
            ],
            label: {
                color: '#fff',
                backgroundColor: '#555',
                borderColor: '#555',
                borderRadius: 4,
                padding: [2,4]
            },
            lineStyle: {
                type: 'dashed',
                color: '#555'
            }
        }
      },
      {
        name: 'Volume',
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: volumes.map(item => [item[0], item[1], item[2]]), // item[2] is 1 for up, -1 for down
        itemStyle: {
          color: (params) => (params.data[2] > 0 ? '#ef232a' : '#14b143'), // red for up, green for down
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