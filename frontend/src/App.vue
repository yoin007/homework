<template>
  <div class="app-container">
    <el-container>
      <el-aside width="200px">
        <el-menu
          :router="true"
          class="el-menu-vertical"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
          <el-menu-item index="/">
            <el-icon><HomeFilled /></el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-menu-item index="/records">
            <el-icon><Document /></el-icon>
            <span>作业记录</span>
          </el-menu-item>
          <el-menu-item index="/subject-records">
            <el-icon><Reading /></el-icon>
            <span>学科作业记录</span>
          </el-menu-item>
          <el-menu-item index="/students">
            <el-icon><User /></el-icon>
            <span>学生信息</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header>
          <h2>学科作业管理系统</h2>
        </el-header>
        <el-main>
          <router-view />
        </el-main>
        <el-footer>
          <p>© 2023 学科作业管理系统</p>
        </el-footer>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { HomeFilled, Document, Reading, User } from '@element-plus/icons-vue'
</script>

<style>
.app-container {
  height: 100vh;
  width: 100%;
}

.el-header {
  background-color: #b3c0d1;
  color: #333;
  line-height: 60px;
  text-align: center;
}

.el-footer {
  background-color: #b3c0d1;
  color: #333;
  text-align: center;
  line-height: 60px;
}

.el-aside {
  background-color: #545c64;
  color: #333;
}

.el-menu-vertical {
  height: 100%;
  border-right: none;
}

.el-main {
  background-color: #e9eef3;
  color: #333;
  padding: 20px;
}
</style>