<template>
  <div class="stock-chart-container">
    <div ref="chartRef" class="chart-content"></div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { createChart } from 'lightweight-charts'

export default {
  name: 'StockChart',
  props: {
    stockCode: {
      type: String,
      default: '513180.SH'
    }
  },
  setup(props) {
    const chartRef = ref(null)
    let chart = null

    // 股票数据
    const stockData = {
      "data": {
        "data": [],
        "dates": [],
        "fields": [
          "OPEN",
          "HIGH",
          "LOW",
          "CLOSE",
          "VOLUME"
        ]
      },
      "message": "成功获取513180.SH从2024-05-30到2025-05-29的历史数据",
      "success": true
    }

    // 加载完整数据集
    const loadFullData = () => {
      // 日期数据
      stockData.data.dates = [
        "2024-05-30", "2024-05-31", "2024-06-03", "2024-06-04", "2024-06-05",
        "2024-06-06", "2024-06-07", "2024-06-11", "2024-06-12", "2024-06-13",
        "2024-06-14", "2024-06-17", "2024-06-18", "2024-06-19", "2024-06-20",
        "2024-06-21", "2024-06-24", "2024-06-25", "2024-06-26", "2024-06-27",
        "2024-06-28", "2024-07-01", "2024-07-02", "2024-07-03", "2024-07-04",
        "2024-07-05", "2024-07-08", "2024-07-09", "2024-07-10", "2024-07-11",
        "2024-07-12", "2024-07-15", "2024-07-16", "2024-07-17", "2024-07-18",
        "2024-07-19", "2024-07-22", "2024-07-23", "2024-07-24", "2024-07-25", 
        "2024-07-26", "2024-07-29", "2024-07-30", "2024-07-31", "2024-08-01",
        "2024-08-02", "2024-08-05", "2024-08-06", "2024-08-07", "2024-08-08",
        "2024-08-09", "2024-08-12", "2024-08-13", "2024-08-14", "2024-08-15"
      ]
      
      // K线数据
      stockData.data.data = [
        [0.511, 0.518, 0.508, 0.509, 4920627400],
        [0.518, 0.522, 0.506, 0.507, 4952652700],
        [0.51, 0.519, 0.508, 0.516, 4754706400],
        [0.512, 0.518, 0.511, 0.518, 3963360654],
        [0.517, 0.525, 0.515, 0.516, 3961281700],
        [0.523, 0.527, 0.518, 0.52, 4872252100],
        [0.523, 0.524, 0.51, 0.513, 4594029400],
        [0.507, 0.514, 0.503, 0.512, 4456641300],
        [0.508, 0.511, 0.505, 0.506, 3667084000],
        [0.511, 0.512, 0.505, 0.508, 3778626900],
        [0.508, 0.51, 0.505, 0.508, 3046735600],
        [0.503, 0.511, 0.501, 0.506, 3450623400],
        [0.508, 0.513, 0.504, 0.506, 2955734213],
        [0.511, 0.522, 0.509, 0.521, 4810698000],
        [0.524, 0.525, 0.514, 0.515, 3283477800],
        [0.511, 0.512, 0.503, 0.508, 3576645100],
        [0.504, 0.505, 0.496, 0.496, 3269864000],
        [0.503, 0.507, 0.496, 0.497, 3868559306],
        [0.498, 0.508, 0.497, 0.506, 3718939700],
        [0.501, 0.503, 0.491, 0.493, 4176463100],
        [0.488, 0.496, 0.488, 0.489, 3745279300],
        [0.486, 0.488, 0.483, 0.488, 1996347607],
        [0.486, 0.494, 0.484, 0.485, 3699713600],
        [0.489, 0.498, 0.488, 0.496, 4607522000],
        [0.504, 0.508, 0.498, 0.5, 3861179100],
        [0.5, 0.502, 0.49, 0.495, 3739950300],
        [0.493, 0.496, 0.486, 0.487, 3033091800],
        [0.488, 0.498, 0.486, 0.495, 4209932800],
        [0.499, 0.505, 0.493, 0.495, 3744739400],
        [0.499, 0.507, 0.497, 0.506, 4549321400],
        [0.512, 0.518, 0.51, 0.516, 3713606400],
        [0.512, 0.513, 0.503, 0.504, 3431653800],
        [0.499, 0.501, 0.495, 0.5, 3774040400],
        [0.502, 0.506, 0.498, 0.502, 3692351600],
        [0.496, 0.501, 0.491, 0.499, 4555318400],
        [0.492, 0.494, 0.489, 0.491, 4111636100],
        [0.491, 0.499, 0.488, 0.498, 5001667467],
        [0.501, 0.502, 0.488, 0.489, 4064770200],
        [0.488, 0.492, 0.478, 0.479, 4543509300],
        [0.477, 0.478, 0.468, 0.471, 4264384600],
        [0.474, 0.478, 0.47, 0.475, 5281981200],
        [0.48, 0.482, 0.475, 0.478, 4276607711.9999995],
        [0.476, 0.476, 0.468, 0.47, 3608511500],
        [0.47, 0.484, 0.468, 0.484, 5775043200],
        [0.48, 0.482, 0.475, 0.478, 4939943600],
        [0.47, 0.473, 0.461, 0.464, 5221842000],
        [0.457, 0.468, 0.448, 0.452, 8378976297],
        [0.462, 0.465, 0.454, 0.459, 6423879900],
        [0.46, 0.468, 0.458, 0.462, 5233562800],
        [0.458, 0.467, 0.454, 0.462, 4626626100],
        [0.469, 0.474, 0.467, 0.468, 4163030000],
        [0.468, 0.47, 0.462, 0.468, 3457852872],
        [0.469, 0.471, 0.464, 0.468, 3667261817],
        [0.469, 0.47, 0.46, 0.461, 3126100800]
      ]
    }

    // 格式化K线数据
    const formatCandlestickData = (rawData) => {
      if (!rawData || !rawData.data || !rawData.dates) return []

      return rawData.dates.map((date, index) => {
        const item = rawData.data[index]
        return {
          time: date,
          open: item[0],
          high: item[1],
          low: item[2],
          close: item[3]
        }
      })
    }

    // 格式化成交量数据
    const formatVolumeData = (rawData) => {
      if (!rawData || !rawData.data || !rawData.dates) return []

      return rawData.dates.map((date, index) => {
        const item = rawData.data[index]
        const isGreen = item[3] < item[0] // 收盘价小于开盘价为绿色（下跌）
        return {
          time: date,
          value: item[4] / 100000000, // 成交量转为亿
          color: isGreen ? 'rgba(239, 83, 80, 0.7)' : 'rgba(38, 166, 154, 0.7)'
        }
      })
    }

    // 初始化图表
    const initChart = () => {
      if (!chartRef.value) return

      try {
        // 加载数据
        loadFullData()

        // 创建图表
        chart = createChart(chartRef.value, {
          width: chartRef.value.clientWidth,
          height: 500,
          layout: {
            background: { color: '#ffffff' },
            textColor: '#333',
          },
          grid: {
            vertLines: { color: 'rgba(197, 203, 206, 0.5)' },
            horzLines: { color: 'rgba(197, 203, 206, 0.5)' },
          },
          timeScale: {
            timeVisible: true,
            secondsVisible: false,
          },
          crosshair: {
            mode: 1
          },
          rightPriceScale: {
            borderColor: 'rgba(197, 203, 206, 0.8)',
            autoScale: true,
          },
          localization: {
            locale: 'zh-CN',
            priceFormatter: (price) => {
              return price.toFixed(3)
            },
            timeFormatter: (time) => {
              return time
            },
          },
        })

        // 添加K线图
        const candlestickSeries = chart.addCandlestickSeries({
          upColor: '#26a69a',
          downColor: '#ef5350',
          borderUpColor: '#26a69a',
          borderDownColor: '#ef5350',
          wickUpColor: '#26a69a',
          wickDownColor: '#ef5350',
          priceScaleId: 'right',
          title: `${props.stockCode}`,
        })

        // 添加成交量图
        const volumeSeries = chart.addHistogramSeries({
          priceFormat: {
            type: 'volume',
            precision: 2,
          },
          priceScaleId: 'volume',
          scaleMargins: {
            top: 0.8,
            bottom: 0,
          },
          title: '成交量(亿)',
        })

        // 设置K线数据
        const candlestickData = formatCandlestickData(stockData.data)
        candlestickSeries.setData(candlestickData)

        // 设置成交量数据
        const volumeData = formatVolumeData(stockData.data)
        volumeSeries.setData(volumeData)

        // 添加图例提示
        chart.subscribeCrosshairMove((param) => {
          if (!param.time || param.point === undefined) {
            return
          }

          const candleData = param.seriesData.get(candlestickSeries)
          const volumeData = param.seriesData.get(volumeSeries)

          if (candleData && volumeData) {
            const tooltipEl = document.createElement('div')
            tooltipEl.className = 'tooltip'
            tooltipEl.innerHTML = `
              <div>日期: ${param.time}</div>
              <div>开: ${candleData.open.toFixed(3)}</div>
              <div>高: ${candleData.high.toFixed(3)}</div>
              <div>低: ${candleData.low.toFixed(3)}</div>
              <div>收: ${candleData.close.toFixed(3)}</div>
              <div>量: ${(volumeData.value * 100).toFixed(2)}亿</div>
            `
            // 这里可以添加自定义tooltip显示逻辑
          }
        })

        // 调整图表大小以适应容器
        chart.timeScale().fitContent()

        // 添加窗口大小变化的监听
        window.addEventListener('resize', handleResize)
      } catch (error) {
        console.error('加载K线图失败:', error)
      }
    }

    // 处理窗口大小变化
    const handleResize = () => {
      if (chart && chartRef.value) {
        chart.applyOptions({
          width: chartRef.value.clientWidth
        })
      }
    }

    // 组件挂载时初始化图表
    onMounted(() => {
      initChart()
    })

    // 组件卸载时清理资源
    onUnmounted(() => {
      if (chart) {
        chart.remove()
        chart = null
      }
      window.removeEventListener('resize', handleResize)
    })

    return {
      chartRef
    }
  }
}
</script>

<style scoped>
.stock-chart-container {
  width: 100%;
  display: flex;
  flex-direction: column;
}

.chart-content {
  width: 100%;
  min-height: 500px;
}
</style>
