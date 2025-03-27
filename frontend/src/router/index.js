import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomePage.vue')
    },
    {
      path: '/records',
      name: 'records',
      component: () => import('../views/RecordsPage.vue')
    },
    {
      path: '/record/:id',
      name: 'record-edit',
      component: () => import('../views/RecordEditPage.vue'),
      props: true
    },
    {
      path: '/subject-records',
      name: 'subject-records',
      component: () => import('../views/SubjectRecordsPage.vue')
    },
    {
      path: '/students',
      name: 'students',
      component: () => import('../views/StudentsPage.vue')
    }
  ]
})

export default router