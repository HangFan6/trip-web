<template>
  <!-- 热门景点 -->
  <div class="home-hot-box">
    <!-- 顶上导航 -->
    <van-cell title="热门推荐"
    icon="/static/home/hot/fire.png"
    is-link
    title-style="text-align:left"
    value="全部榜单"
    :to="{name: 'search', query: {isHot: 1}}"/>
    <!-- 景点列表 -->
    <div class="box-main">
      <router-link class="hot-item"
      v-for="item in dataList"
      :key="item.id"
      :to="{name: 'SightDetail', params: {id: item.id}}">
        <div class="img">
          <span></span>
          <!-- <img src="/static/home/hot/h1.jpg" alt=""> -->
          <img :src="item.main_img" alt="">
        </div>
        <h5 class="van-ellipsis">{{ item.name }}</h5>
        <div class="line-price">
          <span class="price">￥{{ item.min_price }}</span>起
        </div>
      </router-link>
    </div>
  </div>
</template>

<script>
import { ajax } from '@/utils/ajax'
import { SightApis } from '@/utils/apis'
export default {
  data () {
    return {
      dataList: []
    }
  },
  methods: {
    // 查询热门景点数据
    getDataList () {
      ajax.get(SightApis.sightListUrl, {
        params: {
          is_hot: 1
        }
      }).then(({ data }) => {
        this.dataList = data.objects
        console.log(this.dataList)
      })
    }
  },
  created () {
    // 查询接口数据
    this.getDataList()
    // this.dataList = [
    //   { id: 1, img: '/static/home/hot/h1.jpg', name: '景点名称景点名称景点名称', price: 50 },
    //   { id: 2, img: '/static/home/hot/h2.jpg', name: '景点名称', price: 65 },
    //   { id: 3, img: '/static/home/hot/h3.jpg', name: '景点名称景点名称景点名称', price: 69 },
    //   { id: 4, img: '/static/home/hot/h4.jpg', name: '景点名称', price: 90 },
    //   { id: 5, img: '/static/home/hot/h5.jpg', name: '景点名称', price: 80 },
    //   { id: 6, img: '/static/home/hot/h6.jpg', name: '景点名称景点名称', price: 75 },
    //   { id: 7, img: '/static/home/hot/h7.jpg', name: '景点名称', price: 68 },
    //   { id: 8, img: '/static/home/hot/h8.jpg', name: '景点名称', price: 65 },
    //   { id: 9, img: '/static/home/hot/h9.jpg', name: '景点名称景点名称景点名称', price: 92 },
    //   { id: 10, img: '/static/home/hot/h10.jpg', name: '景点名称景点名称', price: 65 }
    // ]
  }
}
</script>

<style lang="less">
.home-hot-box{
  padding: 0 10px;
  .van-cell{
    padding: 10px 0;
  }

  .box-main{
    width: 100%;
    display: flex;
    padding-top: 10px;
    overflow: scroll;
  }
  .hot-item{
    display: flex;
    flex-direction: column;
    width: 100px;
    margin-right: 10px;
    margin-bottom: 10px;

    .img{
      position: relative;

      span{
        position: absolute;
        left: 0;
        top: 0;
        display: inline-block;
        width: 42px;
        height: 20px;
        z-index: 10;
      }

      img{
        width: 100px;
        height: 100px;
      }
    }

    h5{
      color: black;
      padding: 2px 0;
      font-size: 12px;
      margin: 0;
    }

    .line-price{
      color: black;
      font-size: 12px;
      .price{
        color: red;
        font-size: 13px;
      }
    }

    /** &号代表上一级  &:nth-child(1)表示第一个 class="hot-item" 的标签 */
    &:nth-child(1) .img span{
      background: url(/public/static/home/hot/top1.png) no-repeat;
      background-size: 100% auto;
    }
    &:nth-child(2) .img span{
      background: url(/public/static/home/hot/top2.png) no-repeat;
      background-size: 100% auto;
    }
    &:nth-child(3) .img span{
      background: url(/public/static/home/hot/top3.png) no-repeat;
      background-size: 100% auto;
    }
  }
}
</style>
