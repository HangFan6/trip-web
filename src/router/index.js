import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SearchView from '@/views/SearchView.vue'
import SightList from '@/views/sight/SightList.vue'
import SightInfo from '@/views/sight/SightInfo.vue'
import SightDetail from '@/views/sight/SightDetail.vue'
import SightComment from '../views/sight/SightComment.vue'
import SightImage from '@/views/sight/SightImage.vue'
import AccountLogin from '@/views/accounts/LoginView.vue'
import AccountRegister from '@/views/accounts/RegisterView.vue'
import MineView from '@/views/MineView.vue'
import OrderSubmit from '@/views/order/SubmitView.vue'
import OrderPay from '@/views/order/PayView.vue'
import OrderList from '@/views/order/OrderList.vue'

Vue.use(VueRouter)

const routes = [
  // 主页
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  // 景点搜索
  {
    path: '/search',
    name: 'search',
    component: SearchView
  },
  // 个人中心
  {
    path: '/mine',
    name: 'mine',
    component: MineView
  },
  // 景点列表
  {
    path: '/sight/list',
    name: 'SightList',
    component: SightList
  },
  // 景点详情
  {
    path: '/sight/detail/:id',
    name: 'SightDetail',
    component: SightDetail
  },
  // 景点介绍
  {
    path: '/sight/info/:id',
    name: 'SightInfo',
    component: SightInfo
  },
  // 景点评论
  {
    path: '/sight/comment/:id',
    name: 'SightComment',
    component: SightComment
  },
  // 景点图片
  {
    path: '/sight/image/:id',
    name: 'SightImage',
    component: SightImage
  },
  // 用户登录
  {
    path: '/account/login',
    name: 'AccountLogin',
    component: AccountLogin
  },
  // 用户注册
  {
    path: '/account/register',
    name: 'AccountRegister',
    component: AccountRegister
  },
  // 提交订单
  {
    path: '/order/submit/:id',
    name: 'OrderSubmit',
    component: OrderSubmit
  },
  // 确认订单并支付
  {
    path: '/order/pay/:sn',
    name: 'OrderPay',
    component: OrderPay
  },
  // 我的订单列表
  {
    path: '/order/list/:status',
    name: 'OrderList',
    component: OrderList
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    // 该写法，只有在访问的页面中，有相关组件的时候，才会被引入
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = new VueRouter({
  routes
})

// 解决重复点击导航时，控制台出现报错
const VueRouterPush = VueRouter.prototype.push
VueRouter.prototype.push = function push (to) {
  return VueRouterPush.call(this, to).catch(err => err)
}

export default router
