<template>
  <div class="record-edit-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>{{ isEdit ? '编辑作业记录' : '添加作业记录' }}</h3>
        </div>
      </template>
      
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
          <el-input v-model="recordForm.batch" placeholder="例如：第一批次" />
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
        
        <el-form-item>
          <el-button type="primary" @click="submitForm">保存</el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const recordId = route.params.id
const isEdit = computed(() => recordId !== 'new')

const recordFormRef = ref(null)
const students = ref([])
const teachers = ref([])
const subjects = ref([])

const recordForm = reactive({
  student_id: '',
  name: '',
  subject: '',
  score: 0,
  type: '日常作业',
  date: new Date().toISOString().split('T')[0],
  batch: '',
  teacher_id: ''
})

const rules = {
  student_id: [{ required: true, message: '请选择学生', trigger: 'change' }],
  subject: [{ required: true, message: '请选择学科', trigger: 'change' }],
  date: [{ required: true, message: '请选择日期', trigger: 'change' }],
  teacher_id: [{ required: true, message: '请选择教师', trigger: 'change' }]
}

// 获取学生列表
const fetchStudents = async () => {
  try {
    const response = await apiClient.get('/students')
    students.value = response.data
  } catch (error) {
    console.error('获取学生列表失败:', error)
    ElMessage.error('获取学生列表失败')
  }
}

// 获取教师列表
const fetchTeachers = async () => {
  try {
    const response = await apiClient.get('/teachers')
    teachers.value = response.data
  } catch (error) {
    console.error('获取教师列表失败:', error)
    ElMessage.error('获取教师列表失败')
  }
}

// 获取学科列表
const fetchSubjects = async () => {
  try {
    const response = await apiClient.get('/teachers/subjects/all')
    subjects.value = response.data
  } catch (error) {
    console.error('获取学科列表失败:', error)
    ElMessage.error('获取学科列表失败')
  }
}

// 获取记录详情
const fetchRecordDetail = async () => {
  if (!isEdit.value) return
  
  try {
    const response = await apiClient.get(`/records/${recordId}`)
    Object.assign(recordForm, response.data)
  } catch (error) {
    console.error('获取记录详情失败:', error)
    ElMessage.error('获取记录详情失败')
  }
}

// 学生选择变更处理
const handleStudentChange = () => {
  const selectedStudent = students.value.find(s => s.student_id === recordForm.student_id)
  if (selectedStudent) {
    recordForm.name = selectedStudent.name
  }
}

// 提交表单
const submitForm = async () => {
  if (!recordFormRef.value) return
  
  await recordFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (isEdit.value) {
          // 更新记录
          await apiClient.put(`/records/${recordId}`, recordForm)
          ElMessage.success('记录更新成功')
        } else {
          // 创建新记录
          await apiClient.post('/records', recordForm)
          ElMessage.success('记录创建成功')
        }
        router.push('/records')
      } catch (error) {
        console.error('保存记录失败:', error)
        ElMessage.error('保存记录失败: ' + (error.response?.data?.detail || error.message))
      }
    }
  })
}

onMounted(() => {
  fetchStudents()
  fetchTeachers()
  fetchSubjects()
  fetchRecordDetail()
})
</script>

<style scoped>
.record-edit-container {
  max-width: 800px;
  margin: 20px auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>