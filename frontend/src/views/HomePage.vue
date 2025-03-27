<template>
  <div class="home-container">
    <el-card class="welcome-card">
      <template #header>
        <div class="card-header">
          <h3>欢迎使用学科作业管理系统</h3>
        </div>
      </template>
      <div class="card-content">
        <p>本系统用于管理学生作业记录、学生信息和教师信息。</p>
        <p>主要功能包括：</p>
        <ul>
          <li>学生信息管理</li>
          <li>作业记录管理</li>
          <li>学科作业记录查询</li>
          <li>数据导入导出</li>
        </ul>
      </div>
    </el-card>

    <el-card class="template-card">
      <template #header>
        <div class="card-header">
          <h3>作业数据模板下载</h3>
        </div>
      </template>
      <div class="card-content">
        <p>您可以下载学生作业数据模板，填写后导入系统。</p>
        
        <el-form :model="templateForm" label-width="120px">
          <el-form-item label="年级">
            <el-select v-model="templateForm.grade" placeholder="请选择年级" @change="loadClasses">
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
              v-model="templateForm.classes" 
              multiple 
              collapse-tags 
              placeholder="请选择班级（可多选）"
              :disabled="!templateForm.grade"
            >
              <el-option 
                v-for="cls in classes" 
                :key="cls" 
                :label="cls" 
                :value="cls" 
              />
            </el-select>
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="downloadTemplate" :disabled="!templateForm.grade">下载模板</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>

    <el-card class="init-card">
      <template #header>
        <div class="card-header">
          <h3>系统初始化</h3>
        </div>
      </template>
      <div class="card-content">
        <p>如果您是首次使用系统，可以初始化示例数据。</p>
        <el-button type="warning" @click="initSampleData">初始化示例数据</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import apiClient from '../api'
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 年级和班级数据
const grades = ref([])
const classes = ref([])

// 模板表单数据
const templateForm = ref({
  grade: '',
  classes: []
})

// 获取所有年级
const loadGrades = async () => {
  try {
    const response = await apiClient.get('/students/grades/all')
    grades.value = response.data
  } catch (error) {
    console.error('获取年级失败:', error)
    ElMessage.error('获取年级失败')
  }
}

// 根据年级获取班级
const loadClasses = async () => {
  if (!templateForm.value.grade) return
  
  try {
    const response = await apiClient.get(`/students/classes/by-grade/${templateForm.value.grade}`)
    classes.value = response.data
    templateForm.value.classes = [] // 重置班级选择
  } catch (error) {
    console.error('获取班级失败:', error)
    ElMessage.error('获取班级失败')
  }
}

// 下载模板
const downloadTemplate = async () => {
  try {
    const response = await apiClient.post(
      '/records/export-template',
      {
        grade: templateForm.value.grade,
        class_name: templateForm.value.classes
      },
      { responseType: 'blob' }
    )
    
    // 创建下载链接
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `学生作业模板_${new Date().toISOString().slice(0, 10)}.xlsx`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    ElMessage.success('模板下载成功')
  } catch (error) {
    console.error('下载模板失败:', error)
    ElMessage.error('下载模板失败')
  }
}

// 初始化示例数据
const initSampleData = async () => {
  try {
    await ElMessageBox.confirm(
      '初始化将清空现有数据并生成示例数据，是否继续？',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    const response = await apiClient.post('/init-sample-data')
    ElMessage.success(`示例数据初始化成功，已生成 ${response.data.data.students} 名学生、${response.data.data.teachers} 名教师和 ${response.data.data.records} 条作业记录`)
    
    // 重新加载年级和班级数据
    loadGrades()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('初始化示例数据失败:', error)
      ElMessage.error('初始化示例数据失败')
    }
  }
}

// 页面加载时获取年级数据
onMounted(() => {
  loadGrades()
})
</script>

<style scoped>
.home-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.welcome-card {
  grid-column: 1 / 3;
}

.template-card, .init-card {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  padding: 10px 0;
}

ul {
  padding-left: 20px;
}
</style>