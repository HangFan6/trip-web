<template>
  <!-- 精选景点 -->
  <div class="home-fine-box">
    <!-- 顶上导航 -->
    <van-cell title="精选景点"
    icon="location-o"
    is-link
    title-style="text-align:left"
    value="更多"
    :to="{name: 'search', query: {isTop: 1}}"/>
    <!-- 景点列表 -->
    <div class="box-main">
      <!-- <a href="#" class="sight-item" v-for="item in dataList" :key="item.id">
        <img :src="item.img" alt="">
        <div class="right">
          <h5>{{ item.name }}</h5>
          <van-rate v-model="item.score" readonly/>
          <div class="tips">4人点评 | 100%满意</div>
          <div class="tips light">广东-广州</div>
          <div class="line-price">￥ {{ item.price }}起</div>
        </div>
      </a> -->

      <!-- 使用组件 -->
      <!-- <SightItem v-for="item in dataList"
        :key="item.id"
        v-bind:item="item"/> -->
      <sight-item v-for="item in dataList" :key="item.id" :item="item"/>
    </div>
  </div>
</template>

<script>
// 引入组件
import SightItem from '@/components/common/ListSight'
import { ajax } from '@/utils/ajax'
import { SightApis } from '@/utils/apis'

export default {
  components: {
    // 注册组件
    SightItem
  },
  data () {
    return {
      dataList: []
    }
  },
  methods: {
    // 查询精选景点数据
    getDataList () {
      // ajax.get(SightApis.sightListUrl, {
      ajax.get(SightApis.sightListCacheUrl, {
        params: {
          is_top: 1
        }
      }).then(({ data }) => {
        this.dataList = data.objects
        console.log(this.dataList)
      })
    }
  },
  created () {
    this.getDataList()
    // this.dataList = [
    //   { id: 1, name: '景点名称景点名称景点名称', img: '/static/home/hot/h1.jpg', score: 4.5, price: 90 },
    //   { id: 2, name: '景点名称', img: '/static/home/hot/h2.jpg', score: 5, price: 98 },
    //   { id: 3, name: '景点名称景点名称景点名称', img: '/static/home/hot/h3.jpg', score: 4.5, price: 92 },
    //   { id: 4, name: '景点名称', img: '/static/home/hot/h4.jpg', score: 5, price: 88 },
    //   { id: 5, name: '景点名称景点名称', img: '/static/home/hot/h5.jpg', score: 3, price: 98 },
    //   { id: 6, name: '景点名称', img: '/static/home/hot/h6.jpg', score: 3.5, price: 86 }
    // ]
  }
}
</script>

<style lang="less">
.home-fine-box{
  padding: 0 10px;
  .van-cell{
    padding: 10px 0;
  }
  .box-main{
    padding-bottom: 50px;
  }
}
</style>
