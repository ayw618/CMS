<template>
  <el-row :gutter="40" class="panel-group">
    <el-col :xs="12" :sm="12" :lg="8" class="card-panel-col">
      <div class="card-panel" @click="turn_to_list_classes()">
        <div class="card-panel-icon-wrapper icon-message">
          <svg-icon icon-class="education" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            班级数量
          </div>
          <count-to :start-val="0" :end-val="panelData['class_num']" :duration="3600" class="card-panel-num" />
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="8" class="card-panel-col">
      <div class="card-panel" @click="turn_to_list_teachers()">
        <div class="card-panel-icon-wrapper icon-people">
          <svg-icon icon-class="peoples" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            教师人数
          </div>
          <count-to :start-val="0" :end-val="panelData['teacher_num']" :duration="2600" class="card-panel-num" />
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="8" class="card-panel-col">
      <div class="card-panel" @click="turn_to_list_students()">
        <div class="card-panel-icon-wrapper icon-money">
          <svg-icon icon-class="people" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            学生人数
          </div>
          <count-to :start-val="0" :end-val="panelData['student_num']" :duration="3200" class="card-panel-num" />
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="12" class="card-panel-col">
      <div class="card-panel" @click="turn_to_browsing_history()">
        <div class="card-panel-icon-wrapper icon-shopping">
          <svg-icon icon-class="eye-open" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            近一周监控浏览次数
          </div>
          <count-to :start-val="0" :end-val="panelData['browse_num_past_week']" :duration="3600" class="card-panel-num" />
        </div>
      </div>
    </el-col><el-col :xs="12" :sm="12" :lg="12" class="card-panel-col">
      <div class="card-panel" @click="turn_to_exception()">
        <div class="card-panel-icon-wrapper icon-shopping">
          <svg-icon icon-class="message" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            近一周异常帧数
          </div>
          <count-to :start-val="0" :end-val="panelData['exception_num_past_week']" :duration="3600" class="card-panel-num" />
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script>
import admin from '@/utils/admin';
import CountTo from 'vue-count-to'

export default {
  props: {
    panelData: {
      type: Object,
      required: true
    }
  },
  data(){
    return {
    }
  },
  components: {
    CountTo
  },
  watch: {
    panelData: {
      deep: true,
      handler(val) {
        console.log('000000 ---> ', val)
        this.panelData = val
      }
    }
  },
  methods: {
    handleSetLineChartData(type) {
      this.$emit('handleSetLineChartData', type)
    },
    turn_to_list_teachers(){
      this.$router.push({path:'../list/teachers_list'})
    },
    turn_to_list_classes(){      
      this.$router.push({path:'../list/classes'})
    },
    turn_to_list_students(){      
      this.$router.push({path:'../list/students_list'})
    },
    turn_to_browsing_history(){      
      this.$router.push({path:'../records/browsinghistory'})
    },
    turn_to_exception(){      
      this.$router.push({path:'../records/exception'})
    },
  }
}
</script>

<style lang="scss" scoped>
.panel-group {
  margin-top: 18px;

  .card-panel-col {
    margin-bottom: 32px;
  }

  .card-panel {
    height: 108px;
    cursor: pointer;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 40px rgba(0, 0, 0, .05);
    border-color: rgba(0, 0, 0, .05);

    &:hover {
      .card-panel-icon-wrapper {
        color: #fff;
      }

      .icon-people {
        background: #40c9c6;
      }

      .icon-message {
        background: #36a3f7;
      }

      .icon-money {
        background: #f4516c;
      }

      .icon-shopping {
        background: #34bfa3
      }
    }

    .icon-people {
      color: #40c9c6;
    }

    .icon-message {
      color: #36a3f7;
    }

    .icon-money {
      color: #f4516c;
    }

    .icon-shopping {
      color: #34bfa3
    }

    .card-panel-icon-wrapper {
      float: left;
      margin: 14px 0 0 14px;
      padding: 16px;
      transition: all 0.38s ease-out;
      border-radius: 6px;
    }

    .card-panel-icon {
      float: left;
      font-size: 48px;
    }

    .card-panel-description {
      float: right;
      font-weight: bold;
      margin: 26px;
      margin-left: 0px;

      .card-panel-text {
        line-height: 18px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-bottom: 12px;
      }

      .card-panel-num {
        font-size: 20px;
      }
    }
  }
}

@media (max-width:550px) {
  .card-panel-description {
    display: none;
  }

  .card-panel-icon-wrapper {
    float: none !important;
    width: 100%;
    height: 100%;
    margin: 0 !important;

    .svg-icon {
      display: block;
      margin: 14px auto !important;
      float: none !important;
    }
  }
}
</style>
