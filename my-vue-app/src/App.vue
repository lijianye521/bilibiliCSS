<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const selectedKeys = ref(['market'])
const router = useRouter()
</script>

<template>
  <a-layout class="layout">
    <a-layout-header class="header">
      <div class="header-content">
        <div class="logo">股票行情系统</div>
        <a-menu
          v-model:selectedKeys="selectedKeys"
          theme="dark"
          mode="horizontal"
          class="nav-menu"
        >
          <a-menu-item key="market">
            <router-link to="/market">行情中心</router-link>
          </a-menu-item>
          <a-menu-item key="about">
            <router-link to="/about">关于系统</router-link>
          </a-menu-item>
        </a-menu>
      </div>
    </a-layout-header>
    <a-layout-content class="content">
      <div class="content-wrapper">
        <router-view></router-view>
      </div>
    </a-layout-content>
  </a-layout>
</template>

<style>
body {
  margin: 0;
  min-height: 100vh;
  background-color: #141414;
}

.layout {
  min-height: 100vh;
}

.header {
  background: #1f1f1f !important;
  position: fixed;
  z-index: 1;
  width: 100%;
  padding: 0;
}

.header-content {
  padding: 0 16px;
  display: flex;
  align-items: center;
}

.logo {
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  margin-right: 24px;
  white-space: nowrap;
}

.content {
  margin-top: 64px;
  min-height: calc(100vh - 64px);
}

.content-wrapper {
  width: 100%;
  padding: 16px;
}

.nav-menu {
  flex: 1;
}

:deep(.ant-layout) {
  background: #141414;
}

:deep(.ant-menu) {
  background: transparent;
  border-bottom: none;
}

:deep(.ant-menu-item) {
  padding: 0 16px !important;
}

:deep(.ant-menu-item a) {
  color: rgba(255, 255, 255, 0.85) !important;
  text-decoration: none;
  font-size: 14px;
}

:deep(.ant-menu-item-selected) {
  background-color: #177ddc !important;
}

:deep(.ant-menu-item-selected a) {
  color: #fff !important;
}

:deep(.ant-menu-item:hover) {
  background-color: rgba(255, 255, 255, 0.08) !important;
}

:deep(.ant-card) {
  background: #1f1f1f;
  border: none;
  border-radius: 8px;
}

:deep(.ant-card-head) {
  border-bottom: 1px solid #303030;
}

:deep(.ant-card-head-title) {
  color: rgba(255, 255, 255, 0.85);
}

:deep(.ant-card-body) {
  color: rgba(255, 255, 255, 0.85);
}

@media (max-width: 768px) {
  .header-content {
    padding: 0 12px;
  }
  
  .logo {
    font-size: 16px;
    margin-right: 16px;
  }
  
  .content-wrapper {
    padding: 12px;
  }
  
  :deep(.ant-menu-item) {
    padding: 0 12px !important;
  }
}
</style>
