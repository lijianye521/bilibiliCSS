import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/market'
  },
  {
    path: '/market',
    name: 'Market',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 