<template>
  <div class="dashboard-editor-container">
    <!-- <github-corner class="github-corner" /> -->

    <panel-group @handleSetChartData="handleSetChartData" :panelData="panelData"/>


    <el-row :gutter="24">
      <el-col :xs="24" :sm="16" :lg="8">
        <div class="chart-wrapper">
          <line-chart :chart-data="lineChartData_browse" />
        </div>
      </el-col>
      <el-col :xs="24" :sm="16" :lg="8">
        <div class="chart-wrapper" >
          <pie-chart :chart-data="pieChartData_constitution"/>
        </div>
      </el-col>
      <el-col :xs="24" :sm="16" :lg="8">
        <div class="chart-wrapper">
          <line-chart :chart-data="lineChartData_execp" />
        </div>
      </el-col>
    </el-row>
<!-- 
    <el-row :gutter="8">
      <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 12}" :xl="{span: 12}" style="padding-right:8px;margin-bottom:30px;">
        <transaction-table />
      </el-col>
      <el-col :xs="{span: 24}" :sm="{span: 12}" :md="{span: 12}" :lg="{span: 6}" :xl="{span: 6}" style="margin-bottom:30px;">
        <todo-list />
      </el-col>
      <el-col :xs="{span: 24}" :sm="{span: 12}" :md="{span: 12}" :lg="{span: 6}" :xl="{span: 6}" style="margin-bottom:30px;">
        <box-card />
      </el-col>
    </el-row> -->
  </div>
</template>

<script>
import GithubCorner from '@/components/GithubCorner'
import PanelGroup from './components/PanelGroup'
import LineChart from './components/LineChart'
// import RaddarChart from './components/RaddarChart'
import PieChart from './components/PieChart'
// import BarChart from './components/BarChart'
import TransactionTable from './components/TransactionTable'
// import BoxCard from './components/BoxCard'

import admin from '@/utils/admin'

export default {
  name: 'DashboardAdmin',
  components: {
    GithubCorner,
    PanelGroup,
    LineChart,
    // RaddarChart,
    PieChart,
    // BarChart,
    TransactionTable,
    // BoxCard
  },
  data() {
    return {
      lineChartData_browse: {actualData:[], title:'近三天教师浏览监控次数'},
      lineChartData_execp:{actualData:[], title:'近三天异常记录数量'},
      pieChartData_constitution:{PieData:[],title:'近五百张异常帧各异常行为占比'},
      panelData:{teacher_num:0,class_num:0,student_num:0,
                browse_num_past_week:0,exception_num_past_week:0},
      response_data:{}
    }
  },
  mounted(){
    // var response = {
    //   data:{
    //     teacher_num:19,
    //     class_num:10,
    //     student_num:50,
    //     browse_num_past_week:12,
    //     exception_num_past_week:23,
    //     exception_data:{
    //       'day_before_yesterday':12,
    //       'yesterday':23,
    //       'today':63
    //     },
    //     browse_data:{
    //       'day_before_yesterday':10,
    //       'yesterday':12,
    //       'today':7          
    //     },
    //     exception_constitution:{
    //       'eating':15,
    //       'chatting':25,
    //       'bow_head':10,
    //       'enter_exit':35,
    //       'play_phone':15
    //     }
    //   }
    // }
    admin.show_statistics().then(response=>{
    this.response_data = response.data
    console.log('----> ', response.data)
    this.panelData['teacher_num'] = response.data['teacher_num']
    this.panelData['class_num'] = response.data['class_num']
    this.panelData['student_num'] = response.data['student_num']
    this.panelData['browse_num_past_week'] = response.data['browse_num_past_week']
    this.panelData['exception_num_past_week'] = response.data['exception_num_past_week']
    console.log(this.response_data)
    this.lineChartData_browse.actualData = [this.response_data.browse_data['day_before_yesterday'],
                                  this.response_data.browse_data['yesterday'],
                                  this.response_data.browse_data['today']]
    
    this.lineChartData_execp.actualData = [this.response_data.exception_data['day_before_yesterday'],
                                  this.response_data.exception_data['yesterday'],
                                  this.response_data.exception_data['today']]
    this.pieChartData_constitution.PieData = this.response_data['exception_constitution']
    console.log(this.pieChartData_constitution.PieData)

    })
        // })

  },
  methods: {
    handleSetChartData(type) {
      this.lineChartData_browse = lineChartData_browse[type]
      this.lineChartData_execp = lineChartData_execp[type]
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard-editor-container {
  padding: 32px;
  min-height: 100%;
  overflow: hidden;
  background-color: rgb(240, 242, 245);
  position: relative;

  .github-corner {
    position: absolute;
    top: 0px;
    border: 0;
    right: 0;
  }

  .chart-wrapper {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
  }
}

@media (max-width:1024px) {
  .chart-wrapper {
    padding: 15px;
  }
}
</style>
