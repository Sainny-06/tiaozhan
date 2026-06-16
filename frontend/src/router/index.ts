import { createRouter, createWebHistory } from 'vue-router'

import LearningPath from '../pages/LearningPath.vue'
import ProfileChat from '../pages/ProfileChat.vue'
import QuizResult from '../pages/QuizResult.vue'
import ResourceDetail from '../pages/ResourceDetail.vue'
import ResourceGenerate from '../pages/ResourceGenerate.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'ProfileChat',
      component: ProfileChat,
    },
    {
      path: '/generate',
      name: 'ResourceGenerate',
      component: ResourceGenerate,
    },
    {
      path: '/resources',
      name: 'ResourceDetail',
      component: ResourceDetail,
    },
    {
      path: '/path',
      name: 'LearningPath',
      component: LearningPath,
    },
    {
      path: '/quiz',
      name: 'QuizResult',
      component: QuizResult,
    },
  ],
})

export default router
