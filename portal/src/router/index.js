import { createRouter, createWebHistory } from 'vue-router'
import { checkPortalMaintenance } from './guards.js'

import HomePage from '../pages/Home.vue'
import List from '../pages/List.vue'
import Detail from '../pages/Detail.vue'
import MaintenancePage from '../pages/Maintenance.vue'
import MiPerfilView from '../views/MiPerfilView.vue'

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
      name: 'sites-list1',
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
    {
      path: '/maintenance',
      name: 'maintenance',
      component: MaintenancePage,
      props: true,
      beforeEnter: async (to, from, next) => {
        try {
          const { getPortalStatus } = await import('../services/featureFlags.js')
          const status = await getPortalStatus()
          if (status.enabled) {
            next({ name: 'home' })
          } else {
            next()
          }
        } catch (error) {
          next()
        }
      }
    },
    {
      path: '/mi-perfil',
      name: 'Profile',
      component: MiPerfilView  
    }
  ],
})
  
router.beforeEach(checkPortalMaintenance)

export default router