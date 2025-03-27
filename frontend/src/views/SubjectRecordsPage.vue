<template>
  <div class="subject-records-container">
    <el-card class="filter-card">
      <template #header>
        <div class="card-header">
          <h3>学科作业记录筛选</h3>
        </div>
      </template>
      <el-form :model="filterForm" label-width="100px" inline>
        <el-form-item label="学科" prop="subject">
          <el-select v-model="filterForm.subject" placeholder="选择学科" clearable @change="searchRecords">
            <el-option 
              v-for="subject in subjects" 
              :key="subject" 
              :label="subject" 
              :value="subject" 
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="年级">
          <el-select v-model="filterForm.grade" placeholder="选择年级" clearable @change="loadClasses">
            <el-option 
              v-for="grade in grades" 
              :key="grade" 
              :label="grade" 
              :value="grade" 
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="班级">
          <el-select v-model="filterForm.class_name" placeholder="选择班级" clearable @change="loadGroups">
            <el-option 
              v-for="cls in classes" 
              :key="cls" 
              :label="cls" 
              :value="cls" 
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="小组">
          <el-select v-model="filterForm.group" placeholder="选择小组" clearable>
            <el-option 
              v-for="group in groups" 
              :key="group" 
              :label="group" 
              :value="group" 
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="searchRecords">查询</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-tabs v-model="activeTab" class="records-tabs">
      <el-tab-pane label="学科作业记录列表" name="records">
        <el-card>
          <template #header>
            <div class="card-header">
              <h3>{{ filterForm.subject || '全部学科' }}作业记录列表</h3>
            </div>
          </template>
          
          <el-table :data="records" style="width: 100%" v-loading="loading">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="student_id" label="学号" width="100" />
            <el-table-column prop="name" label="姓名" width="100" />
            <el-table-column prop="subject" label="学科" width="100" />
            <el-table-column prop="score" label="分数" width="80" />
            <el-table-column prop="type" label="类型" width="100" />
            <el-table-column prop="date" label="日期" width="120" />
            <el-table-column prop="batch" label="批次" width="120" />
            <el-table-column label="操作" width="200">
              <template #default="scope">
                <el-button 
                  size="small" 
                  type="primary" 
                  @click="editRecord(scope.row)"
                >
                  编辑
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
      
      <el-tab-pane label="学科成绩汇总" name="summary">
        <el-card>
          <template #header>
            <div class="card-header">
              <h3>{{ filterForm.subject || '全部学科' }}成绩汇总</h3>
              <el-button type="success" @click="exportSummary">导出Excel</el-button>
            </div>
          </template>
          
          <el-alert
            v-if="!filterForm.subject"
            title="请选择一个学科以查看学科成绩汇总"
            type="warning"
            :closable="false"
          />
          
          <el-table 
            v-else 
            :data="summaryData" 
            style="width: 100%" 
            v-loading="summaryLoading"
          >
            <el-table-column prop="id" label="ID" width="60" />
            <el-table-column prop="student_id" label="学号" width="100" />
            <el-table-column prop="name" label="姓名" width="100" />
            <el-table-column prop="grade" label="年级" width="80" />
            <el-table-column prop="class_name" label="班级" width="100" />
            <el-table-column 
              v-for="date in dateColumns" 
              :key="date" 
              :prop="date" 
              :label="date" 
              width="100" 
            />
            <el-table-column prop="total_score" label="总分" width="80" />
            <el-table-column prop="count" label="次数" width="80" />
          </el-table>
        </el-card>
      </el-tab-pane>
    </el-tabs>
    
    <!-- 编辑记录对话框 -->
    <el-dialog 
      title="编辑作业记录" 
      v-model="dialogVisible" 
      width="500px"
    >
      <el-form :model="recordForm" label-width="100px" :rules="rules" ref="recordFormRef">
        <el-form-item label="学号" prop="student_id">
          <el-input v-model="recordForm.student_id" disabled />
        </el-form-item>
        
        <el-form-item label="姓名" prop="name">
          <el-input v-model="recordForm.name" disabled />
        </el-form-item>
        
        <el-form-item label="学科" prop="subject">
          <el-input v-model="recordForm.subject" disabled />
        </el-form-item>
        
        <el-form-item label="分数" prop="score">
          <el-input-number v-model="recordForm.score" :min="0" :max="100" />
        </el-form-item>
        
        <el-form-item label="类型" prop="type">
          <el-input v-model="recordForm.type" placeholder="例如：日常作业、期中考试" />
        </el-form-item>
        
        <el-form-item label="日期" prop="date">
          <el-date-picker 
            v-model="recordForm.date" 
            type="date" 
            placeholder="选择日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        
        <el-form-item label="批次" prop="batch">
          <el-input v-model="recordForm.batch" placeholder="例如：第一批、期中" />
        </el-form-item>
        
        <el-form-item label="教师ID" prop="teacher_id">
          <el-select v-model="recordForm.teacher_id" filterable placeholder="请选择教师">
            <el-option 
              v-for="teacher in teachers" 
              :key="teacher.teacher_id" 
              :label="`${teacher.teacher_id} - ${teacher.name}`" 
              :value="teacher.teacher_id" 
            />
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitRecord">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import apiClient from '../api'
import { ElMessage, ElMessageBox } from 'element-plus'

// 筛选表单数据
const filterForm = ref({
  grade: '',
  class_name: '',
  group: '',
  subject: '',
  start_date: '',
  end_date: ''
})

// 日期范围选择器
const dateRange = ref([])

// 监听日期范围变化，更新筛选表单
watch(dateRange, (newVal) => {
  if (newVal && newVal.length === 2) {
    filterForm.value.start_date = newVal[0]
    filterForm.value.end_date = newVal[1]
  } else {
    filterForm.value.start_date = ''
    filterForm.value.end_date = ''
  }
})

// 下拉选项数据
const grades = ref([])
const classes = ref([])
const groups = ref([])
const subjects = ref([])
const teachers = ref([])

// 表格数据
const records = ref([])
const summaryData = ref([])
const loading = ref(false)
const summaryLoading = ref(false)

// 标签页控制
const activeTab = ref('records')

// 对话框控制
const dialogVisible = ref(false)
const recordForm = ref({
  id: null,
  student_id: '',
  name: '',
  subject: '',
  score: null,
  type: '',
  date: '',
  batch: '',
  teacher_id: ''
})
const recordFormRef = ref(null)

// 表单验证规则
const rules = {
  score: [{ required: true, message: '请输入分数', trigger: 'blur' }],
  date: [{ required: true, message: '请选择日期', trigger: 'change' }],
  teacher_id: [{ required: true, message: '请选择教师', trigger: 'change' }]
}

// 计算属性：获取汇总表格的日期列
const dateColumns = computed(() => {
  const columns = new Set()
  summaryData.value.forEach(item => {
    Object.keys(item).forEach(key => {
      if (!['id', 'student_id', 'name', 'grade', 'class_name', 'total_score', 'count'].includes(key)) {
        columns.add(key)
      }
    })
  })
  return Array.from(columns).sort()
})

// 加载年级数据
const loadGrades = async () => {
  try {
    const response = await apiClient.get('/students/grades/all')
    grades.value = response.data
  } catch (error) {
    console.error('获取年级失败:', error)
    ElMessage.error('获取年级失败')
  }
}

// 加载班级数据
const loadClasses = async () => {
  try {
    const params = {
      grade: filterForm.value.grade || null
    }
    const response = await apiClient.get(`/students/classes/by-grade/${filterForm.value.grade}`)
    classes.value = response.data
  } catch (error) {
    console.error('获取班级失败:', error)
    ElMessage.error('获取班级失败')
  }
}

// 加载小组数据
const loadGroups = async () => {
  if (!filterForm.value.class_name) {
    groups.value = []
    filterForm.value.group = ''
    return
  }
  
  try {
    const response = await apiClient.get(`/students/groups/by-class/${filterForm.value.class_name}`)
    groups.value = response.data
  } catch (error) {
    console.error('获取小组失败:', error)
    ElMessage.error('获取小组失败')
  }
}

// 加载学科数据
const loadSubjects = async () => {
  try {
    const response = await apiClient.get('/teachers/subjects/')
    subjects.value = response.data
  } catch (error) {
    console.error('获取学科列表失败:', error)
    ElMessage.error('获取学科列表失败')
  }
}

// 加载教师数据
const loadTeachers = async () => {
  try {
    const response = await apiClient.get('/teachers/')
    teachers.value = response.data
  } catch (error) {
    console.error('获取教师失败:', error)
    ElMessage.error('获取教师失败')
  }
}

// 搜索作业记录
const searchRecords = async () => {
  loading.value = true
  
  try {
    // 构建查询参数
    const params = {}
    if (filterForm.value.grade) params.grade = filterForm.value.grade
    if (filterForm.value.class_name) params.class_name = filterForm.value.class_name
    if (filterForm.value.group) params.group = filterForm.value.group
    if (filterForm.value.subject) params.subject = filterForm.value.subject
    if (filterForm.value.start_date) params.start_date = filterForm.value.start_date
    if (filterForm.value.end_date) params.end_date = filterForm.value.end_date
    
    const response = await apiClient.get('/records/', { params })
    records.value = response.data
    
    // 如果当前是汇总标签页，也更新汇总数据
    if (activeTab.value === 'summary') {
      loadSummary()
    }
  } catch (error) {
    console.error('搜索作业记录失败:', error)
    ElMessage.error('搜索作业记录失败')
  } finally {
    loading.value = false
  }
}

// 加载学科成绩汇总数据
const loadSummary = async () => {
  if (!filterForm.value.subject) return
  
  summaryLoading.value = true
  
  try {
    const response = await apiClient.post('/records/subject-summary', filterForm.value)
    summaryData.value = response.data
  } catch (error) {
    console.error('获取学科成绩汇总失败:', error)
    ElMessage.error('获取学科成绩汇总失败')
  } finally {
    summaryLoading.value = false
  }
}

// 导出学科成绩汇总
const exportSummary = async () => {
  if (!filterForm.value.subject) {
    ElMessage.warning('请先选择一个学科')
    return
  }
  
  try {
    const response = await apiClient.post(
      'http://localhost:8080/records/export-subject-summary',
      filterForm.value,
      { responseType: 'blob' }
    )
    
    // 创建下载链接
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${filterForm.value.subject}学科作业汇总_${new Date().toISOString().slice(0, 10)}.xlsx`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    ElMessage.success('学科成绩汇总导出成功')
  } catch (error) {
    console.error('导出学科成绩汇总失败:', error)
    ElMessage.error('导出学科成绩汇总失败')
  }
}

// 重置筛选条件
const resetFilter = () => {
  filterForm.value = {
    grade: '',
    class_name: '',
    group: '',
    subject: '',
    start_date: '',
    end_date: ''
  }
  dateRange.value = []
  classes.value = []
  groups.value = []
  
  // 清空汇总数据
  summaryData.value = []
}

// 编辑记录
const editRecord = (row) => {
  recordForm.value = { ...row }
  dialogVisible.value = true
}

// 提交记录表单
const submitRecord = async () => {
  if (!recordFormRef.value) return
  
  await recordFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        // 更新记录
        await axios.put(`http://localhost:8080/records/${recordForm.value.id}`, recordForm.value)
        ElMessage.success('更新成功')
        
        dialogVisible.value = false
        searchRecords()
      } catch (error) {
        console.error('保存记录失败:', error)
        ElMessage.error('保存记录失败: ' + (error.response?.data?.detail || error.message))
      }
    }
  })
}

// 监听标签页变化
watch(activeTab, (newVal) => {
  if (newVal === 'summary' && filterForm.value.subject) {
    loadSummary()
  }
})

// 页面加载时初始化数据
onMounted(() => {
  loadGrades()
  loadSubjects()
  loadTeachers()
})
</script>

<style scoped>
.subject-records-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.filter-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.records-tabs {
  margin-top: 20px;
}

.el-table {
  margin-top: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>