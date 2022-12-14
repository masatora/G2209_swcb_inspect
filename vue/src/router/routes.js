
const routes = [
  {
    path: '/',
    component: () => import('layouts/InspectCaseList.vue')
  },
  {
    path: '/add',
    component: () => import('layouts/AddInspectCase.vue')
  },
  {
    path: '/view/:caseId',
    component: () => import('layouts/ViewInspectCase.vue')
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
