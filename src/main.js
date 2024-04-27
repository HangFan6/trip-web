import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import * as filters from './utils/filters'
// VantUI组件库
import Vant from 'vant'
import 'vant/lib/index.css'

// 把VantUI当做一个插件，在Vue中使用（在about页面中查看）
Vue.use(Vant)

Vue.config.productionTip = false

// 注册过滤器
Object.keys(filters).forEach(k => Vue.filter(k, filters[k]))

// 添加Vue实例
window.app = new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
// new Vue({
//   router,
//   store,
//   render: h => h(App)
// }).$mount('#app')
