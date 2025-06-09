<template>
  <div class="app-container">
    <div class="filter-container">
      <!-- <el-input v-model="listQuery.title" placeholder="Title" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />

      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        Search
      </el-button> -->
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        添加老师
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

      <el-table-column label="账号" min-width="150px">
        <template slot-scope="{row}">
          <span >{{ row.user_account }}</span>
        </template>
      </el-table-column>
      <el-table-column label="姓名" min-width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="权限" min-width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.role==1 ?'班主任':'教导主任' }}</span>
        </template>
      </el-table-column>
      <el-table-column label="在线状态" class-name="status-col" min-width="100">
        <template slot-scope="{row}">
            {{ row.status == 0 ? '离线' : '在线' }}
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
        <el-form-item label="账号" prop="user_account">
          <el-input v-model="temp.user_account" />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="temp.password" />
        </el-form-item>
        <el-form-item label="权限" prop="role">
          <el-select v-model="temp.role" class="filter-item" placeholder="请选择">
            <el-option v-for="item in roleOptions" :key="item.key" :label="item.key" :value="item.value" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible_create = false">
          取消
        </el-button>
        <el-button type="primary" @click="createData()">
          确定
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :title="textMap['update']" :visible.sync="dialogFormVisible_update">
      <el-form  :model="temp" label-position="left" label-width="70px" style="width: 400px; margin-left:50px;">
        <el-form-item label="账号" prop="user_account">
          <span>{{ temp.user_account}}</span>          
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <span>{{ temp.name }}</span>
        </el-form-item>
        <el-form-item label="权限" prop="role">
          <el-select v-model="temp.role" class="filter-item" placeholder="请选择">
            <el-option v-for="item in roleOptions" :key="item.key" :label="item.key" :value="item.value" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible_update = false">
          取消
        </el-button>
        <el-button type="primary" @click="updateData()">
          确定
        </el-button>
      </div>
    </el-dialog>


  </div>
</template>

<script>
import { fetchList, fetchPv, createArticle, updateArticle } from '@/api/article'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import admin from '@/utils/admin'
const calendarTypeOptions = [
  { key: 'CN', display_name: 'China' },
  { key: 'US', display_name: 'USA' },
  { key: 'JP', display_name: 'Japan' },
  { key: 'EU', display_name: 'Eurozone' }
]

// arr to obj, such as { CN : "China", US : "USA" }
const calendarTypeKeyValue = calendarTypeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'ComplexTable',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
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
      type:1,
      listLoading: true,
      roleOptions: [{key:'班主任', value:1},{key:'教导主任',value:2}],
      listQuery: {
        page: 1,
        limit: 20,
        importance: undefined,
        title: undefined,
        type: 1,
        sort: '+id'
      },
      importanceOptions: [1, 2, 3],
      calendarTypeOptions,
      sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
      statusOptions: ['published', 'draft', 'deleted'],
      showReviewer: false,
      temp: {
        id: undefined,
        importance: 1,
        remark: '',
        timestamp: new Date(),
        user_account:'',
        password:'',
        name:'',
        role:1
      },
      rw:{
        user_account:'',
        password:'',
        name:'',
        role:1
      },
      dialogStatus: '',
      textMap: {
        update: '编辑',
        create: '添加老师'
      },
      dialogFormVisible_create : false,
      dialogFormVisible_update : false,
      pvData: [],
      rules: {
        type: [{ required: true, message: 'type is required', trigger: 'change' }],
        timestamp: [{ type: 'date', required: true, message: 'timestamp is required', trigger: 'change' }],
        title: [{ required: true, message: 'title is required', trigger: 'blur' }]
      },
      downloadLoading: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      if(typeof(data) != 'undefined') {
        this.listQuery.page = data.page
        this.listQuery.limit = data.limit
      }
      // console.log('1111111 ===> ', this.listQuery)
      var listdata = {
        page:this.listQuery.page,
        per_page:this.listQuery.limit,
        type:this.listQuery.type
      }
      admin.get_teacher_info(listdata).then(response=>{
      // })
      // fetchList(this.listQuery).then(response => {
        this.list = response.data['data']
        this.total = response.data['teacher_num']

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleModifyStatus(row, status) {
      this.$message({
        message: '操作成功',
        type: 'success'
      })
      row.status = status
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+id'
      } else {
        this.listQuery.sort = '-id'
      }
      this.handleFilter()
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        importance: 1,
        remark: '',
        timestamp: new Date(),
        title: '',
        status: 'published',
        type: ''
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible_create = true
    },
    createData() {
      // this.$refs['dataForm'].validate((valid) => {
      //   if (valid) {
          // this.temp.id = parseInt(Math.random() * 100) + 1024 // mock a id
          // this.temp.author = 'vue-element-admin'
          // createArticle(this.temp).then(() => {
      var data={
          user_account:this.temp.user_account,
          password:this.temp.password,
          name:this.temp.name,
          role:this.temp.role
      }
      admin.register(data).then(response=>{

      // })
            this.list.unshift(this.temp)
            this.dialogFormVisible_create = false
            this.$notify({
              title: '创建成功',
              // message: 'Created Successfully',
              type: 'success',
              duration: 2000
            })
          })
      //   }
      // })
    },
    handleUpdate(row) {
      this.rw = row
      this.temp = Object.assign({}, row) // copy obj
      // this.temp.timestamp = new Date(this.temp.timestamp)
      this.dialogStatus = 'update'
      this.dialogFormVisible_update = true
    },
    updateData() {
      var data={
        user_account:this.temp.user_account,
        role:this.temp.role
      }
      // this.$refs['dataForm'].validate((valid) => {
      //   if (valid) {
      //     const tempData = Object.assign({}, this.temp)
      //     tempData.timestamp = +new Date(tempData.timestamp) // change Thu Nov 30 2017 16:41:05 GMT+0800 (CST) to 1512031311464
      //     updateArticle(tempData).then(() => {
            // const index = this.list.findIndex(v => v.id === this.temp.id
        admin.set_power(data).then(response=>{
            // this.list.splice(index, 1, this.temp)
            this.rw.role = this.temp.role
            this.dialogFormVisible_update = false
            this.$notify({
              title: '修改成功',
              // message: 'Update Successfully',
              type: 'success',
              duration: 2000
            })
          })
    },
    handleDelete(row, index) {
      var data={
        user_account:row.user_account
      }
      admin.deregister(data).then(response=>{
        this.$notify({
          title: '删除成功',
          // message: 'Delete Successfully',
          type: 'success',
          duration: 2000
        })
        this.list.splice(index, 1)
      })
    },
    handleFetchPv(pv) {
      fetchPv(pv).then(response => {
        this.pvData = response.data.pvData
        this.dialogPvVisible = true
      })
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['timestamp', 'title', 'type', 'importance', 'status']
        const filterVal = ['timestamp', 'title', 'type', 'importance', 'status']
        const data = this.formatJson(filterVal)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: 'table-list'
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal) {
      return this.list.map(v => filterVal.map(j => {
        if (j === 'timestamp') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    },
    getSortClass: function(key) {
      const sort = this.listQuery.sort
      return sort === `+${key}` ? 'ascending' : 'descending'
    }
  }
}
</script>
