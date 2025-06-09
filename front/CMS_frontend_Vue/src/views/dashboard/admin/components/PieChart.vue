<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from './mixins/resize'

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
    initChart() {
      this.chart = echarts.init(this.$el, 'macarons')
      this.setOptions(this.chartData)
      
  },
  setOptions({PieData,title}){
    // console.log(PieData)
    this.chart.setOption({
        title:{
          text:title,
          left:'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          left: 'center',
          bottom: '10',
          data: ['吃东西', '交流', '低头', '进出教室', '玩手机']
        },
        series: [
          {
            name: 'WEEKLY WRITE ARTICLES',
            type: 'pie',
            // roseType: 'radius',
            radius: '45%',
            center: ['50%', '50%'],   
            itemStyle: {
              borderRadius: 10
            },
            data: [
              { value: PieData['eating'], name: '吃东西' },
              { value: PieData['chatting'], name: '交流' },
              { value: PieData['bow_head'], name: '低头' },
              { value: PieData['enter_exit'], name: '进出教室' },
              { value: PieData['play_phone'], name: '玩手机' }
            ],
            animationEasing: 'cubicInOut',
            animationDuration: 2600
          }
        ]
      })
    }
  }
}
</script>
