import { createRouter, createWebHistory } from 'vue-router'

import HomePage from '../pages/Home.vue'
import List from '../pages/List.vue'
import Detail from '../pages/Detail.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage,
    },
    {
      path: '/sites',
      name: 'sites-list',
      component: List,
    },
    {
      path: '/sites/:id',
      name: 'site-detail',
      component: Detail,
      props: true,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/sites-list',
      name: 'sites-list',
      component: () => import('../views/SitesList.vue'),
    },

  ],
})

export default router
