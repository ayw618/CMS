/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const tableRouter = {
  path: '/list',
  component: Layout,
  redirect: '/table',
  name: 'Table',
  meta: {
    title: '名单',
    icon: 'table'
  },
  children: [
    {
      hidden:true,
      path: 'dynamic-table',
      component: () => import('@/views/table/dynamic-table/index'),
      name: 'DynamicTable',
      meta: { title: 'Dynamic Table' }
    },
    {
      hidden:true,
      path: 'drag-table',
      component: () => import('@/views/table/drag-table'),
      name: 'DragTable',
      meta: { title: 'Drag Table' }
    },
    {
      hidden:true,
      path: 'inline-edit-table',
      component: () => import('@/views/table/inline-edit-table'),
      name: 'InlineEditTable',
      meta: { title: 'Inline Edit' }
    },
    {
      hidden:true,
      path: 'complex-table',
      component: () => import('@/views/table/complex-table'),
      name: 'ComplexTable',
      meta: { title: 'Complex Table' }
    },
    {
      path: 'classes',
      component: () => import('@/views/table/list_classes'),
      name: 'list_classes',
      meta: {title: '班级名单'}
    },
    {
      path: 'teachers_list',
      component: () => import('@/views/table/list_teachers'),
      name: 'list_teachers',
      meta: {title: '教师名单'}
    },
    {
      path: 'students_list',
      component: () => import('@/views/table/list_students'),
      name: 'list_students',
      meta: {title: '学生名单'}
    }
  ]
}
export default tableRouter
