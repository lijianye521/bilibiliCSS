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
        <div class="logo-section">
          <div class="logo">股票行情系统</div>
        </div>
        <div class="nav-section">
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
  overflow-x: hidden;
}

.layout {
  min-height: 100vh;
}

.header {
  background: rgba(19, 23, 34, 0.8) !important;
  position: fixed;
  z-index: 1;
  width: 100%;
  padding: 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-content {
  max-width: 1800px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  height: 100%;
}

.logo-section {
  display: flex;
  align-items: center;
}

.logo {
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  margin-right: 32px;
  white-space: nowrap;
  letter-spacing: 0.5px;
}

.nav-section {
  flex: 1;
  display: flex;
  align-items: center;
}

.content {
  margin-top: 64px;
  min-height: calc(100vh - 64px);
  padding: 0 24px;
}

.content-wrapper {
  max-width: 1800px;
  margin: 0 auto;
  width: 100%;
  min-height: calc(100vh - 64px);
}

.nav-menu {
  background: transparent !important;
  border: none;
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
  margin: 0 4px !important;
  border-radius: 4px;
  transition: all 0.3s ease;
}

:deep(.ant-menu-item a) {
  color: rgba(255, 255, 255, 0.85) !important;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
}

:deep(.ant-menu-item-selected) {
  background-color: rgba(255, 255, 255, 0.08) !important;
}

:deep(.ant-menu-item-selected a) {
  color: #fff !important;
}

:deep(.ant-menu-item:hover) {
  background-color: rgba(255, 255, 255, 0.04) !important;
}

:deep(.ant-menu-horizontal) {
  line-height: 64px;
}

@media (max-width: 768px) {
  .header-content {
    padding: 0 16px;
  }
  
  .logo {
    font-size: 16px;
    margin-right: 16px;
  }
  
  .content {
    padding: 0 16px;
  }
  
  :deep(.ant-menu-item) {
    padding: 0 12px !important;
    margin: 0 2px !important;
  }
}
</style>
