<template>
  <div class="page-home">
    <div class="page-home-title">旅游网</div>
    <!-- <Button type="primary">主要按钮</Button>
    <v-button type="primary">主要按钮</v-button> -->

    <!-- Banner图 -->
    <Banner/>
    <!-- 热门推荐 -->
    <Hot/>
    <!-- 精选景点 -->
    <Fine/>
    <!-- <TripFooter/> -->
    <trip-footer/>
  </div>
</template>

<script>
// @ is an alias to /src
// import axios from 'axios'
// import { ajax } from '@/utils/ajax'

// ************ 手动按需引用组件 *******************
// // 引入按钮组件
// import Button from 'vant/lib/button'
// // 引入组件的相关样式
// import 'vant/lib/button/style'

// 引用Banner组件
import Banner from '@/components/home/BannerView'
// 引用Hot组件
import Hot from '@/components/home/HotView'
// 引用Fine组件
import Fine from '@/components/home/FineView'
import TripFooter from '@/components/common/FooterView'

export default {
  name: 'HomeView',
  components: {
    // 注册组件
    // Button: Button, 缩写形式如下
    // Button,
    // 'v-button': Button,

    // Banner图
    Banner,
    // 热门推荐
    Hot,
    // 精选景点
    Fine,
    // 底部导航
    TripFooter
  }
  // created () {
  //   // vue.js中的跨域（下面的网址可能不存在，无法使用）
  //   // ajax.get('http://django.t.mukewang.com/api/system/slider/list/?types=11').then(resp => {
  //   // ajax.get('http://localhost:8081/api/accounts/user/detail/').then(resp => {
  //   // ajax.get('http://localhost:8081/api/system/slider/list/?types=11').then(resp => {

  //   // Django中的跨域（端口号为Django中的端口号）
  //   // ajax.get('http://127.0.0.1:8000/hello/world/').then(resp => {
  //   // ajax.get('http://localhost:8000/hello/world/').then(resp => {
  //   // 在vue.js中解决Django的跨域（端口号为vue.js中的端口号）
  //   ajax.get('http://localhost:8081/test/hello/world/').then(resp => {
  //     console.log('返回的结果：', resp)
  //   }).catch(err => {
  //     console.log('请求出错：', err)
  //   })
  // }
}
</script>
<style lang="less" scoped>
.page-home-title{
  font-size: 25px;
  height: 50px;
  line-height: 50px;
  font-weight: bold;
}
</style>
