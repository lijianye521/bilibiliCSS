import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Antd from 'ant-design-vue'
import { ConfigProvider } from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'
import './style.css'
import { darkTheme } from './theme'

const app = createApp(App)
app.use(router)
app.use(Antd)

// 配置全局主题
app.component('a-config-provider', ConfigProvider)
app.provide('theme', darkTheme)

app.mount('#app')
