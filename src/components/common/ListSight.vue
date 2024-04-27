<template>
  <!-- 景点列表 -->
  <router-link class="sight-item" :to="{name: 'SightDetail', params: {id: item.id}}">
    <!-- <img :src="item.img" alt=""> -->
    <!-- 子组件中调用接口数据 -->
    <img :src="item.main_img" :alt="item.name">
    <div class="right">
      <h5>{{ item.name }}</h5>
      <!-- 评分 -->
      <van-rate v-model="score" readonly allow-half />
      <!-- <van-rate v-model="item.score" readonly allow-half /> -->
      <div class="tips">{{ item.comment_count }}人点评 | 100%满意</div>
      <div class="tips light">{{ item.province }} - {{ item.city }} - {{ item.area }}</div>
      <div class="line-price">￥ {{ item.min_price }}起</div>
    </div>
  </router-link>
</template>
<script>
import { ref } from 'vue'

export default {
  setup (props) {
    const score = ref(props.item.score) // 创建本地变量score，并初始化为props.item.score的值
    return { score }
  },
  // 组件间数据的通信
  props: ['item']
}
</script>

<style lang="less">
  /** 景点列表*/
  .sight-item{
    display: flex;
    border-bottom: 1px solid #e6e6e6;
    padding-top: 10px;
    background-color: white;

    img{
      width: 100px;
      height: 150px;
    }
    h5{
      color: black;
      font-size: 14px;
      padding: 5px 0;
      margin: 0;
    }
    .right{
      text-align: left;
      flex-grow: 1;
      justify-content: left;
      padding-left: 5px;
      position: relative;
    }

    .line-price{
        position: absolute;
        right: 10px;
        top: 20px;
        display: inline-block;
        color: red;
        font-size: 16px;
        font-weight: bold;
      }

    .tips{
      font-size: 12px;
      color: #666;
      &.light{
        color: #999;
      }
    }
  }
</style>
