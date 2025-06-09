<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from './mixins/resize'
import { date } from 'jszip/lib/defaults'
export default {
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '350px'
    },
    autoResize: {
      type: Boolean,
      default: true
    },
    chartData: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      chart: null
    }
  },
  watch: {
    chartData: {
      deep: true,
      handler(val) {
        this.setOptions(val)
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart()
    })
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    dateFormat(date){
      var year = date.getFullYear()
      var month = date.getMonth() < 9 ? '0' + (date.getMonth()+1)
                    : date.getMonth()+1
      var day = date.getDate() < 10 ? '0' + (date.getDate())
                    : date.getDate()
      alert(year + '-' + month + '-' +day)
      return year + '-' + month + '-' +day
    },
    initChart() {
      this.chart = echarts.init(this.$el, 'macarons')
      // console.log(this.chartData)
      this.setOptions(this.chartData)
    },
    setOptions({actualData, title } ) {
      this.chart.setOption({
        title:{

          text:title,
          left:'center'
        },
        xAxis: {
          data: [ '前天', '昨天', '今天'],
          boundaryGap: false,
          axisTick: {
            show: false
          }
        },
        grid: {
          left: 10,
          right: 10,
          bottom: 20,
          top: 30,
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          },
          padding: [5, 10]
        },
        yAxis: {
          axisTick: {
            show: false
          }
        },
        series: [
        {
          smooth: true,
          type: 'line',
          itemStyle: {
            normal: {
              color: '#3888fa',
              lineStyle: {
                color: '#3888fa',
                width: 2
              }
              // areaStyle: {
              //   color: '#f3f8ff'
              // }
            }
          },
          data: [actualData[0],actualData[1],actualData[2]],
          animationDuration: 2800,
          animationEasing: 'quadraticOut'
        }]
      })
    }
  }
}
</script>
