/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const recordsRouter = {
  path: '/records',
  component: Layout,
  redirect: '/records',
  name: 'records',
  meta: {
    title: '记录表',
    icon: 'table'
  },
  children: [
    {
      path: 'browsinghistory',
      component: () => import('@/views/records/browsinghistory'),
      name: 'browsinghistory',
      meta: {title: '教师浏览记录表'}
    },
    {
      path: 'exception',
      component: () => import('@/views/records/exception'),
      name: 'exception',
      meta: {title: '异常帧记录表'}
    }
  ]
}
export default recordsRouter
