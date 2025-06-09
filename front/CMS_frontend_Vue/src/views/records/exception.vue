<template>
  <div class="app-container">
    <!-- <div class="filter-container">
      <el-input v-model="listQuery.title" placeholder="Title" style="width: 200px;margin-right:20px;" class="filter-item" @keyup.enter.native="handleFilter" />

       <el-select v-model="listQuery.type" placeholder="Type" clearable class="filter-item" style="margin-right:20px;width: 130px">
        <el-option v-for="item in calendarTypeOptions" :key="item.key" :label="item.display_name+'('+item.key+')'" :value="item.key" />
      </el-select> 
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        Search
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        Add
      </el-button>
    </div> -->

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
    >
       <!-- @sort-change="sortChange"  -->
      <el-table-column label="序号" prop="id" align="center" min-width="80" :class-name="getSortClass('id')">
        <template slot-scope="{row}">
          <span>{{ row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="时间" min-width="180px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.time | parseTime('{y}-{m}-{d} {h}:{i}:{s}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="班级" min-width="150px"  align="center">
        <template slot-scope="{row}">
          <span>
            {{row.class_id}}
            <!-- {{ row.class_id }} -->
          </span>
        </template>
      </el-table-column>
      <el-table-column label="动作标签" min-width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ tag_convert[row.tag] }}</span>
        </template>
      </el-table-column>
      <el-table-column label="图片链接" min-width="150px"  align="center">
        <template slot-scope="{row}">   
          <span style="color:blue;font-style: italic;text-decoration: underline;" > 
            <a v-bind:href=row.link target="_blank">
            链接 
            </a>
          </span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" min-width="230" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <!-- <template>
          <el-popconfirm
          confirm-button-text='好的'
          cancel-button-text='不用了'
          icon="el-icon-info"
          icon-color="red"
          title="确定删除吗？"
          > -->
          <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleDelete(row,$index)">
            删除
          </el-button>
        <!-- </el-popconfirm> -->

          <!-- </template> -->
          

        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

  </div>
</template>

<script>
import { fetchList, fetchPv, createArticle, updateArticle } from '@/api/article'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import admin from '@/utils/admin'
// const calendarTypeOptions = [
//   { key: 'CN', display_name: 'China' },
//   { key: 'US', display_name: 'USA' },
//   { key: 'JP', display_name: 'Japan' },
//   { key: 'EU', display_name: 'Eurozone' }
// ]

// arr to obj, such as { CN : "China", US : "USA" }
// const calendarTypeKeyValue = calendarTypeOptions.reduce((acc, cur) => {
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
      tag_convert : {
        'bow_head':'低头',
        'enter_exit':'进出教室',
        'chatting':'聊天',
        'play_phone':'玩手机',
        'eating':'吃东西'
      },
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true, 
      listQuery: {
        page: 1,
        limit: 20,
        importance: undefined,
        title: undefined,
        type: undefined,
        sort: '+id'
      },
      // calendarTypeOptions,
      sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList(data) {
      // console.log('-----000000----- ', data)
      this.listLoading = true
      if(typeof(data) != 'undefined') {
        this.listQuery.page = data.page
        this.listQuery.limit = data.limit
      }
      // console.log('1111111 ===> ', this.listQuery)
      var listdata = {
        page:this.listQuery.page,
        per_page:this.listQuery.limit
      }
      admin.show_exceptions(listdata).then(response=>{
      // fetchList(this.listQuery).then(response => {
        this.list = response.data['data']
        this.total = response.data['exception_num']
        // this.listQuery.page = data.page
        // this.listQuery.limit = data.limit

        // console.log('444444444 ===> ', response.data)

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    handleDelete(row, index) {
      var data = {
        id:row.id
      }
      admin.delete_exception(data).then(response=>{
        
        // admin.delete_exception()
        this.$notify({
          title: '删除成功',
          // message: '删除成功',
          type: 'success',
          duration: 2000
        })
        this.list.splice(index, 1)
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
