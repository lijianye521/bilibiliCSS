<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { darkTheme } from './theme'

const selectedKeys = ref(['market'])
const router = useRouter()
</script>

<template>
  <a-config-provider :theme="darkTheme">
    <a-layout class="layout">
      <a-layout-header class="header">
        <div class="header-content">
          <div class="logo-section">
            <div class="logo">股票行情系统</div>
          </div>
          <div class="nav-section">
            <a-menu
              v-model:selectedKeys="selectedKeys"
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
  </a-config-provider>
</template>

<style>
body {
  margin: 0;
  min-height: 100vh;
  background-color: #131722;
  overflow-x: hidden;
}

.layout {
  min-height: 100vh;
}

.header {
  position: fixed;
  z-index: 1;
  width: 100%;
  padding: 0;
  height: 48px;
  line-height: 48px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
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
  font-size: 16px;
  font-weight: 600;
  margin-right: 32px;
  white-space: nowrap;
}

.nav-section {
  flex: 1;
  display: flex;
  align-items: center;
}

.content {
  margin-top: 48px;
  min-height: calc(100vh - 48px);
  padding: 0 24px;
}

.content-wrapper {
  max-width: 1800px;
  margin: 0 auto;
  width: 100%;
  min-height: calc(100vh - 48px);
}

.nav-menu {
  background: transparent;
  border: none;
  flex: 1;
  line-height: 48px;
}

:deep(.ant-menu-item) {
  padding: 0 12px !important;
  margin: 0 4px !important;
}

:deep(.ant-menu-item a) {
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
}

:deep(.ant-menu-horizontal) {
  border-bottom: none;
  line-height: 48px;
}

@media (max-width: 768px) {
  .header-content {
    padding: 0 16px;
  }
  
  .logo {
    font-size: 14px;
    margin-right: 16px;
  }
  
  .content {
    padding: 0 16px;
  }
}
</style>
