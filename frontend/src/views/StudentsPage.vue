<template>
  <div class="students-container">
    <h1>学生信息管理</h1>
    
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm" class="filter-form">
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
          <el-select v-model="filterForm.class_name" placeholder="选择班级" clearable>
            <el-option 
              v-for="className in classes" 
              :key="className" 
              :label="className" 
              :value="className" 
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="学号">
          <el-input v-model="filterForm.student_id" placeholder="输入学号" clearable />
        </el-form-item>
        
        <el-form-item label="姓名">
          <el-input v-model="filterForm.name" placeholder="输入姓名" clearable />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="searchStudents">查询</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card class="table-card">
      <div class="table-operations">
        <el-button type="primary" @click="showAddDialog">添加学生</el-button>
        <el-button type="success" @click="exportStudents">导出学生信息</el-button>
        <el-button type="warning" @click="showImportDialog">导入学生信息</el-button>
      </div>
      
      <el-table :data="students" border style="width: 100%">
        <el-table-column prop="student_id" label="学号" width="120" />
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="gender" label="性别" width="80">
          <template #default="scope">
            {{ scope.row.gender === 'M' ? '男' : '女' }}
          </template>
        </el-table-column>
        <el-table-column prop="grade" label="年级" width="100" />
        <el-table-column prop="class_name" label="班级" width="100" />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="showEditDialog(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="confirmDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 添加/编辑学生对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑学生' : '添加学生'"
      width="500px"
    >
      <el-form :model="studentForm" label-width="80px" :rules="rules" ref="studentFormRef">
        <el-form-item label="学号" prop="student_id">
          <el-input v-model="studentForm.student_id" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="studentForm.name" />
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="studentForm.gender">
            <el-radio label="M">男</el-radio>
            <el-radio label="F">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="年级" prop="grade">
          <el-select v-model="studentForm.grade" placeholder="选择年级" @change="loadClassesForForm">
            <el-option 
              v-for="grade in grades" 
              :key="grade" 
              :label="grade" 
              :value="grade" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="班级" prop="class_name">
          <el-select v-model="studentForm.class_name" placeholder="选择班级">
            <el-option 
              v-for="className in formClasses" 
              :key="className" 
              :label="className" 
              :value="className" 
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 导入学生信息对话框 -->
    <el-dialog
      v-model="importDialogVisible"
      title="导入学生信息"
      width="500px"
    >
      <el-upload
        class="upload-demo"
        drag
        action="/students/import"
        :on-success="handleImportSuccess"
        :on-error="handleImportError"
        accept=".xlsx"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          拖拽文件到此处或 <em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            请上传Excel文件(.xlsx)，包含学号、姓名、性别、年级、班级等信息
          </div>
        </template>
      </el-upload>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'
import apiClient from '../api'

// 数据列表
const students = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

// 筛选表单
const filterForm = reactive({
  grade: '',
  class_name: '',
  student_id: '',
  name: ''
})

// 年级和班级选项
const grades = ref([])
const classes = ref([])
const formClasses = ref([])

// 添加/编辑表单
const dialogVisible = ref(false)
const isEdit = ref(false)
const studentForm = reactive({
  student_id: '',
  name: '',
  gender: 'M',
  grade: '',
  class_name: ''
})

// 导入对话框
const importDialogVisible = ref(false)

// 表单验证规则
const rules = {
  student_id: [
    { required: true, message: '请输入学号', trigger: 'blur' },
    // { pattern: /^\d{10}$/, message: '学号必须为10位数字', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '姓名长度在2到20个字符之间', trigger: 'blur' }
  ],
  gender: [
    { required: true, message: '请选择性别', trigger: 'change' }
  ],
  grade: [
    { required: true, message: '请选择年级', trigger: 'change' }
  ],
  class_name: [
    { required: true, message: '请选择班级', trigger: 'change' }
  ]
}

const studentFormRef = ref(null)

// 初始化数据
onMounted(async () => {
  await loadGrades()
  await searchStudents()
})

// 加载年级数据
const loadGrades = async () => {
  try {
    const response = await apiClient.get('/students/grades/all/')
    grades.value = response.data
  } catch (error) {
    console.error('获取年级失败:', error)
    ElMessage.error('获取年级失败')
  }
}

// 根据年级加载班级
const loadClasses = async () => {
  if (!filterForm.grade) {
    classes.value = []
    return
  }
  
  try {
    const response = await apiClient.get(`/students/classes/by-grade/${filterForm.grade}`)
    classes.value = response.data
  } catch (error) {
    console.error('获取班级失败:', error)
    ElMessage.error('获取班级失败')
  }
}

// 为表单加载班级
const loadClassesForForm = async () => {
  if (!studentForm.grade) {
    formClasses.value = []
    return
  }
  
  try {
    const response = await apiClient.get(`/students/classes/by-grade/${studentForm.grade}`)
    formClasses.value = response.data
  } catch (error) {
    console.error('获取班级失败:', error)
    ElMessage.error('获取班级失败')
  }
}

// 查询学生
const searchStudents = async () => {
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      ...filterForm
    }
    
    const response = await apiClient.get('/students', { params })
    students.value = response.data.items
    total.value = response.data.total
  } catch (error) {
    console.error('获取学生信息失败:', error)
    ElMessage.error('获取学生信息失败')
  }
}

// 重置筛选表单
const resetForm = () => {
  Object.keys(filterForm).forEach(key => {
    filterForm[key] = ''
  })
  searchStudents()
}

// 分页处理
const handleSizeChange = (val) => {
  pageSize.value = val
  searchStudents()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  searchStudents()
}

// 显示添加对话框
const showAddDialog = () => {
  isEdit.value = false
  Object.keys(studentForm).forEach(key => {
    studentForm[key] = key === 'gender' ? 'M' : ''
  })
  dialogVisible.value = true
}

// 显示编辑对话框
const showEditDialog = async (row) => {
  isEdit.value = true
  Object.keys(studentForm).forEach(key => {
    studentForm[key] = row[key]
  })
  
  // 加载班级选项
  if (studentForm.grade) {
    await loadClassesForForm()
  }
  
  dialogVisible.value = true
}

// 提交表单
const submitForm = async () => {
  if (!studentFormRef.value) return
  
  await studentFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (isEdit.value) {
          // 编辑学生
          await apiClient.put(`/students/${studentForm.student_id}`, studentForm)
          ElMessage.success('更新学生信息成功')
        } else {
          // 添加学生
          await apiClient.post('/students', studentForm)
          ElMessage.success('添加学生成功')
        }
        
        dialogVisible.value = false
        searchStudents()
      } catch (error) {
        console.error('操作失败:', error)
        ElMessage.error(error.response?.data?.detail || '操作失败')
      }
    }
  })
}

// 确认删除
const confirmDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除学生 ${row.name} (${row.student_id}) 吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(async () => {
    try {
      await apiClient.delete(`/students/${row.student_id}`)
      ElMessage.success('删除成功')
      searchStudents()
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  })
}

// Add formatDate function
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}
</script>

<style scoped>
.students-container {
  padding: 20px;
}

.filter-card {
  margin-bottom: 20px;
}

.table-card {
  margin-bottom: 20px;
}

.table-operations {
  margin-bottom: 15px;
  display: flex;
  gap: 10px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.el-upload {
  width: 100%;
}
</style>
