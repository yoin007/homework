<template>
  <div class="records-container">
    <el-card class="filter-card">
      <template #header>
        <div class="card-header">
          <h3>作业记录筛选</h3>
        </div>
      </template>
      <el-form :model="filterForm" label-width="100px" inline>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            @change="handleDateChange"
          />
        </el-form-item>

        <el-form-item label="年级">
          <el-select 
            v-model="filterForm.grade" 
            placeholder="选择年级" 
            clearable 
            @change="handleGradeChange"
            :disabled="!dateRange || dateRange.length !== 2"
          >
            <el-option 
              v-for="grade in grades" 
              :key="grade" 
              :label="grade" 
              :value="grade" 
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="班级">
          <el-select 
            v-model="filterForm.class_name" 
            placeholder="选择班级" 
            clearable
            @change="handleClassChange"
            :disabled="!filterForm.grade"
          >
            <el-option 
              v-for="cls in classes" 
              :key="cls" 
              :label="cls" 
              :value="cls" 
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="批次">
          <el-select v-model="filterForm.batch" placeholder="选择批次" clearable>
            <el-option 
              v-for="batch in batches" 
              :key="batch" 
              :label="batch" 
              :value="batch" 
            />
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="searchRecords">查询</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-tabs v-model="activeTab" class="records-tabs">
      <el-tab-pane label="作业记录列表" name="records">
        <el-card>
          <template #header>
            <div class="card-header">
              <h3>作业记录列表</h3>
              <div>
                <el-upload
                  class="upload-demo"
                  :action="apiClient.defaults.baseURL + '/records/import'"
                  :on-success="handleUploadSuccess"
                  :on-error="handleUploadError"
                  :show-file-list="false"
                >
                  <el-button type="success">导入Excel</el-button>
                </el-upload>
                <el-button type="primary" @click="addRecord">添加记录</el-button>
              </div>
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
                <el-button 
                  size="small" 
                  type="danger" 
                  @click="deleteRecord(scope.row)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
      
      <el-tab-pane label="成绩汇总" name="summary">
        <el-card>
          <template #header>
            <div class="card-header">
              <h3>学生成绩汇总</h3>
              <el-button type="success" @click="exportSummary">导出Excel</el-button>
            </div>
          </template>
          
          <el-table :data="summaryData" style="width: 100%" v-loading="summaryLoading">
            <el-table-column prop="id" label="ID" width="60" />
            <el-table-column prop="student_id" label="学号" width="100" />
            <el-table-column prop="name" label="姓名" width="100" />
            <el-table-column prop="grade" label="年级" width="80" />
            <el-table-column prop="class_name" label="班级" width="100" />
            <el-table-column prop="group" label="小组" width="100" />
            <el-table-column 
              v-for="subject in subjectColumns" 
              :key="subject" 
              :prop="subject" 
              :label="subject" 
              width="80" 
            />
            <el-table-column prop="total_score" label="总分" width="80" />
          </el-table>
        </el-card>
      </el-tab-pane>
    </el-tabs>
    
    <!-- 添加/编辑记录对话框 -->
    <el-dialog 
      :title="dialogTitle" 
      v-model="dialogVisible" 
      width="500px"
    >
      <el-form :model="recordForm" label-width="100px" :rules="rules" ref="recordFormRef">
        <el-form-item label="学号" prop="student_id">
          <el-select 
            v-model="recordForm.student_id" 
            filterable 
            placeholder="请选择学生"
            @change="handleStudentChange"
          >
            <el-option 
              v-for="student in students" 
              :key="student.student_id" 
              :label="`${student.student_id} - ${student.name}`" 
              :value="student.student_id" 
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="姓名" prop="name">
          <el-input v-model="recordForm.name" disabled />
        </el-form-item>
        
        <el-form-item label="学科" prop="subject">
          <el-select v-model="recordForm.subject" placeholder="请选择学科">
            <el-option 
              v-for="subject in subjects" 
              :key="subject" 
              :label="subject" 
              :value="subject" 
            />
          </el-select>
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
import apiClient from '../api'
import { ref, onMounted, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()

// 筛选表单数据
const filterForm = ref({
  grade: '',
  class_name: '',
  batch: '',
  start_date: '',
  end_date: ''
})

// 日期范围选择器
const dateRange = ref([])

// 下拉选项数据
const grades = ref([])
const classes = ref([])
// 删除重复声明的batches变量，因为在页面底部已经声明过了
const students = ref([])
const teachers = ref([])

// 处理日期变化
const handleDateChange = async (val) => {
  if (val && val.length === 2) {
    filterForm.value.start_date = val[0]
    filterForm.value.end_date = val[1]
    // 重置其他筛选条件
    filterForm.value.grade = ''
    filterForm.value.class_name = ''
    filterForm.value.batch = ''
    // 加载年级数据
    await loadGrades()
    await searchRecords()
  } else {
    filterForm.value.start_date = ''
    filterForm.value.end_date = ''
    grades.value = []
    classes.value = []
    batches.value = []
    await searchRecords()
  }
}

// 处理年级变化
const handleGradeChange = async () => {
  filterForm.value.class_name = ''
  filterForm.value.batch = ''
  classes.value = []
  batches.value = []
  if (filterForm.value.grade) {
    await loadClasses()
  }
  await searchRecords()
}

// 处理班级变化
const handleClassChange = async () => {
  filterForm.value.batch = ''
  batches.value = []
  if (filterForm.value.class_name) {
    await loadBatches()
  }
  await searchRecords()
}

// 表格数据
const records = ref([])
const summaryData = ref([])
const loading = ref(false)
const summaryLoading = ref(false)

// 标签页控制
const activeTab = ref('records')

// 对话框控制
const dialogVisible = ref(false)
const dialogTitle = ref('添加作业记录')
const recordForm = ref({
  student_id: '',
  name: '',
  subject: '',
  score: null,
  type: '',
  date: new Date().toISOString().slice(0, 10),
  batch: '',
  teacher_id: ''
})
const recordFormRef = ref(null)

// 表单验证规则
const rules = {
  student_id: [{ required: true, message: '请选择学生', trigger: 'change' }],
  subject: [{ required: true, message: '请选择学科', trigger: 'change' }],
  date: [{ required: true, message: '请选择日期', trigger: 'change' }],
  teacher_id: [{ required: true, message: '请选择教师', trigger: 'change' }]
}

// 计算属性：获取汇总表格的学科列
const subjectColumns = computed(() => {
  const columns = new Set()
  summaryData.value.forEach(item => {
    Object.keys(item).forEach(key => {
      if (!['id', 'student_id', 'name', 'grade', 'class_name', 'group', 'total_score'].includes(key)) {
        columns.add(key)
      }
    })
  })
  return Array.from(columns)
})

// 加载年级数据
const loadGrades = async () => {
  try {
    // const params = {
    //   start_date: filterForm.value.start_date,
    //   end_date: filterForm.value.end_date
    // }
    // const response = await apiClient.get('/grades/all', { params })
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

// 加载批次数据
const loadBatches = async () => {
  try {
    const params = {
      grade: filterForm.value.grade || null,
      class_name: filterForm.value.class_name || null,
      start_date: filterForm.value.start_date ? filterForm.value.start_date.split('T')[0] : null,
      end_date: filterForm.value.end_date ? filterForm.value.end_date.split('T')[0] : null
    }
    const response = await apiClient.get('/records/batches', { params })
    batches.value = response.data
  } catch (error) {
    console.error('获取批次失败:', error)
    ElMessage.error('获取批次失败: ' + (error.response?.data?.detail || error.message))
  }
}

// 加载学科数据
const subjects = ref([])

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

// 加载学生数据
const loadStudents = async () => {
  try {
    const response = await apiClient.get('/students/')
    students.value = response.data.items || []
  } catch (error) {
    console.error('获取学生失败:', error)
    ElMessage.error('获取学生失败')
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

// 加载成绩汇总数据
const loadSummary = async () => {
  summaryLoading.value = true
  
  try {
    // 构建查询参数，确保与后端RecordFilter结构一致
    const params = {
      grade: filterForm.value.grade || null,
      class_name: filterForm.value.class_name || null,
      group: filterForm.value.group || null,
      subject: filterForm.value.subject || null,
      start_date: filterForm.value.start_date || null,
      end_date: filterForm.value.end_date || null
    }
    
    const response = await apiClient.post('/records/summary', params)
    summaryData.value = response.data
  } catch (error) {
    console.error('获取成绩汇总失败:', error)
    ElMessage.error('获取成绩汇总失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    summaryLoading.value = false
  }
}

// 导出成绩汇总
const exportSummary = async () => {
  try {
    const response = await apiClient.post('/records/export', filterForm.value, {
      responseType: 'blob'
    })
    
    // 创建下载链接
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `学生成绩汇总_${new Date().toISOString().slice(0, 10)}.xlsx`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    ElMessage.success('成绩汇总导出成功')
  } catch (error) {
    console.error('导出成绩汇总失败:', error)
    ElMessage.error('导出成绩汇总失败: ' + (error.response?.data?.detail || error.message))
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
}

// 添加记录
const addRecord = () => {
  dialogTitle.value = '添加作业记录'
  recordForm.value = {
    student_id: '',
    name: '',
    subject: '',
    score: null,
    type: '',
    date: new Date().toISOString().slice(0, 10),
    batch: '',
    teacher_id: ''
  }
  dialogVisible.value = true
}

// 编辑记录
const editRecord = (row) => {
  dialogTitle.value = '编辑作业记录'
  recordForm.value = { ...row }
  dialogVisible.value = true
}

// 删除记录
const deleteRecord = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除ID为 ${row.id} 的作业记录吗？`,
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await apiClient.delete(`/records/${row.id}`)
    ElMessage.success('删除成功')
    searchRecords()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除记录失败:', error)
      ElMessage.error('删除记录失败')
    }
  }
}

// 处理学生选择变化
const handleStudentChange = () => {
  const student = students.value.find(s => s.student_id === recordForm.value.student_id)
  if (student) {
    recordForm.value.name = student.name
  }
}

// 提交记录表单
const submitRecord = async () => {
  if (!recordFormRef.value) return
  
  await recordFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (recordForm.value.id) {
          // 更新记录
          await apiClient.put(`/records/${recordForm.value.id}`, recordForm.value)
          ElMessage.success('更新成功')
        } else {
          // 创建记录
          await apiClient.post('/records/', recordForm.value)
          ElMessage.success('添加成功')
        }
        
        dialogVisible.value = false
        searchRecords()
      } catch (error) {
        console.error('保存记录失败:', error)
        ElMessage.error('保存记录失败: ' + (error.response?.data?.detail || error.message))
      }
    }
  })
}

// 处理Excel上传成功
const handleUploadSuccess = (response) => {
  ElMessage.success(`导入成功，共导入 ${response.imported_count} 条记录`)
  searchRecords()
}

// 处理Excel上传失败
const handleUploadError = (error) => {
  console.error('导入失败:', error)
  ElMessage.error('导入失败: ' + (error.response?.data?.detail || error.message))
}

// 监听标签页变化
watch(activeTab, (newVal) => {
  if (newVal === 'summary') {
    loadSummary()
  }
})

// 页面加载时初始化数据
// 批次选项数据
const batches = ref([])

// 初始化数据
onMounted(async () => {
  await Promise.all([
    loadGrades(),
    loadSubjects(),
    loadStudents(),
    loadTeachers(),
    loadBatches()
  ])
  searchRecords()
})
</script>

<style scoped>
.records-container {
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