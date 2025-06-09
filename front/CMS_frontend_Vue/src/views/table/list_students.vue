<template>
  <div class="app-container">
    <div class="filter-container">
      <!-- <el-input v-model="listQuery.name" placeholder="姓名" style="width: 200px;margin-right:20px;" class="filter-item" @keyup.enter.native="handleFilter" /> -->
      <el-input v-model="listQuery.class_id" placeholder="班级" style="width: 200px;margin-right:20px;" class="filter-item" @keyup.enter.native="handleFilter" />
    
      <!-- <el-select v-model="listQuery.class_id" placeholder="班级" clearable class="filter-item" style="width: 130px;margin-right:20px;">
        <el-option v-for="item in list_classes" :key="item.key" :label="item.display_name+'('+item.key+')'" :value="item.key" />
      </el-select> -->
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        搜索
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        新增学生
      </el-button>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
    >
      <el-table-column label="班级" min-width="150px">        
        <template slot-scope="{row}">
          <span>{{row.class_id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="姓名" min-width="150px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="学号" align="center" min-width="160">
        <template slot-scope="{row}">
          <span>{{ row.student_id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="性别" align="center" min-width="120">
        <template slot-scope="{row}">
          <span>{{ row.gender }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" min-width="230" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">
            编辑
          </el-button>
          <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleDelete(row,$index)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog :title="textMap['create']" :visible.sync="dialogFormVisible_create">
      <el-form  :model="temp" label-position="left" label-width="70px" style="width: 400px; margin-left:50px;">
        <!-- <el-form-item label="班级" prop="class">
          <el-select v-model="temp.class" class="filter-item" placeholder="请选择">
            <el-option v-for="item in list_classes" :key="item.key" :label="item.display_name" :value="item.key" />
          </el-select>
        </el-form-item> -->
        <el-form-item label="班级" prop="class">
          <el-input v-model="temp.class_id" />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="temp.name" />
        </el-form-item>
        
        <el-form-item label="学号" prop="student_id">
          <el-input v-model="temp.student_id" />
        </el-form-item>
        <el-form-item label="性别">
          <el-select v-model="temp.gender" class="filter-item" placeholder="请选择">
            <el-option v-for="item in genderOptions" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          取消
        </el-button>
        <el-button type="primary" @click="createData()">
          确定
        </el-button>
      </div>
    </el-dialog>

    
    <el-dialog :title="textMap['update']" :visible.sync="dialogFormVisible_update">
      <el-form  :model="temp" label-position="left" label-width="70px" style="width: 400px; margin-left:50px;">
        <!-- <el-form-item label="班级" prop="class">
          <el-select v-model="temp.class" class="filter-item" placeholder="请选择">
            <el-option v-for="item in list_classes" :key="item.key" :label="item.display_name" :value="item.key" />
          </el-select>
        </el-form-item> -->
        <el-form-item label="班级" prop="class">
          <el-input v-model="temp.class_id" />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <!-- <el-input v-model="temp.name" /> -->
          {{ temp.name }}
        </el-form-item>
        
        <el-form-item label="学号" prop="student_id">
          <!-- <el-input v-model="temp.student_id" /> -->
          {{ temp.student_id }}
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <!-- <el-select v-model="temp.gender" class="filter-item" placeholder="请选择">
            <el-option v-for="item in genderOptions" :key="item" :label="item" :value="item" />
          </el-select> -->
          {{ temp.gender }}
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          取消
        </el-button>
        <el-button type="primary" @click="updateData()">
          确定
        </el-button>
      </div>
    </el-dialog>
    <!-- <el-dialog :visible.sync="dialogPvVisible" title="Reading statistics">
      <el-table :data="pvData" border fit highlight-current-row style="width: 100%">
        <el-table-column prop="key" label="Channel" />
        <el-table-column prop="pv" label="Pv" />
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogPvVisible = false">Confirm</el-button>
      </span>
    </el-dialog> -->
  </div>
</template>

<script>
import { fetchList, fetchPv, createArticle, updateArticle } from '@/api/article'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import admin from '@/utils/admin'
import data from '../pdf/content'

const list_classes = [
  { key: 'CN', display_name: 'China' },
  { key: 'US', display_name: 'USA' },
  { key: 'JP', display_name: 'Japan' },
  { key: 'EU', display_name: 'Eurozone' }
]

// arr to obj, such as { CN : "China", US : "USA" }
// const calendarTypeKeyValue = list_classes.reduce((acc, cur) => {
//   acc[cur.key] = cur.display_name
//   return acc
// }, {})

export default {
  name: 'ComplexTable',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        deleted: 'danger'
      }
      return statusMap[status]
    },
    typeFilter(type) {
      return calendarTypeKeyValue[type]
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        importance: undefined,
        name: '',
        class_id: '',
      },
      importanceOptions: [1, 2],
      list_classes,
      genderOptions: ['男', '女'],
      showReviewer: false,
      temp: {
        // id: undefined,
        // importance: 1,
        class_id: '',
        name: '',
        student_id: '',
        gender: ''
      },
      dialogFormVisible_create: false,
      dialogFormVisible_update: false,
      dialogStatus: '',
      textMap: {
        update: '编辑',
        create: '新建'
      },
      dialogPvVisible: false,
      downloadLoading: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList(data) {
      this.listLoading = true
      if(typeof(data) != 'undefined') {
        this.listQuery.page = data.page
        this.listQuery.limit = data.limit
      }
      // console.log('1111111 ===> ', this.listQuery)
      var listdata = {
        page: this.listQuery.page,
        per_page: this.listQuery.limit
      }
      // console.log(listdata)
      admin.show_all_students(listdata).then(response=>{
        // console.log(response.data)
        this.list = response.data['data']
        this.total = response.data['student_num']
      })
      // fetchList(this.listQuery).then(response => {

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      // })
    },
    handleFilter() {
      this.listQuery.page = 1
      var data = {
        class_id:this.listQuery.class_id,
        page:this.page,
        per_page:this.limit
      }
      admin.show_class_students(data).then(response=>{
        var rdata = response.data
        this.list = rdata['data']
        this.total = rdata['student_num']
      })
    },
    resetTemp() {
      this.temp = {
        class_id: '',
        name: '',
        student_id: '',
        gender: ''
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible_create = true
      // this.$nextTick(() => {
      //   this.$refs['dataForm'].clearValidate()
      // })
    },
    createData() {
      // this.$refs['dataForm'].validate((valid) => {
        // if (valid) {
          // this.temp.class
          // this.temp.id = parseInt(Math.random() * 100) + 1024 // mock a id
          // this.temp.author = 'vue-element-admin'
          var data={
            class_id:this.temp.class_id,
            name:this.temp.name,
            student_id:this.temp.student_id,
            gender:this.temp.gender
          }
          admin.create_student(data).then(response=>{
            
            this.list.unshift(this.temp)
          // })
          // createArticle(this.temp).then(() => {
            // this.list.unshift(this.temp)
            this.dialogFormVisible_create = false
            this.$notify({
              title: '创建成功',
              // message: 'Created Successfully',
              type: 'success',
              duration: 2000
            })
          })
        // }
      // })
    },
    handleUpdate(row) {
      this.row_temp = row
      // this.temp = Object.assign({}, row) // copy obj
      // this.temp.timestamp = new Date(this.temp.timestamp)
      // console.log(row)
      this.temp = {
        class_id: row.class_id,
        name: row.name,
        student_id: row.student_id,
        gender: row.gender        
      }
      this.dialogStatus = 'update'
      this.dialogFormVisible_update = true
      // this.$nextTick(() => {
      //   this.$refs['dataForm'].clearValidate()
      // })
    },
    updateData() {
      var data={
        class_id:this.temp.class_id,
        student_id:this.temp.student_id,
      }
      
      admin.change_student_info(data).then(response=>{
            this.row_temp.class_id = this.temp.class_id
            // const index = this.list.findIndex(v => v.id === this.temp.id)
            // this.list.splice(index, 1, this.temp)
            this.dialogFormVisible_update = false
            this.$notify({
              title: '更新成功',
              // message: 'Update Successfully',
              type: 'success',
              duration: 2000
            })
      })
          // })
        // }
      // })
    },
    handleDelete(row, index) {
      var data={
        student_id:row.student_id
      }
      admin.delete_student(data).then(response=>{
        this.$notify({
          title: '删除成功',
          // message: '删除成功',
          type: 'success',
          duration: 2000
        })
        this.list.splice(index, 1)
      })
    }
  }
}
</script>
