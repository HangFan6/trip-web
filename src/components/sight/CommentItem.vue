<template>
  <!-- 评论列表的每一项 -->
  <div class="comment-item-box">
    <div class="cmt-header">
      <div class="rate">
        <van-rate v-model="score"
          allow-half
          readonly
          color="#ffd21e"
          void-icon="star"
          void-color="#eee"
          size="small"
        />
      </div>
      <!-- 使用过滤器，脱敏处理姓名 -->
      <div class="user">{{ item.user.nickname || '匿名用户' | unameFormat }} {{ item.created_at }}</div>
    </div>
    <!-- 评论内容 -->
    <div class="cmt-content">
      <p>{{ item.content }}</p>
    </div>
    <!-- 评论图片 -->
    <div class="cmt-imgs" @click="show=item.images && item.images.length>0">
      <van-image width="100" height="100"
        :src="image.img"
        v-for="(image, index) in item.images" :key="index"
      />
      <!-- <van-image width="100" height="100" src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"/> -->
    </div>
    <!-- 图片预览 -->
    <van-image-preview v-model="show" :images="imageUrls" @change="onChange">
      <template v-slot:index>第{{ index + 1 }}页</template>
    </van-image-preview>
  </div>
</template>
<script>
import { ref } from 'vue'

export default {
  props: ['item'],
  setup (props) {
    const score = props.item.score
    const show = ref(false)
    const index = ref(0)
    // const images = [
    //   'https://fastly.jsdelivr.net/npm/@vant/assets/apple-1.jpeg',
    //   'https://fastly.jsdelivr.net/npm/@vant/assets/apple-2.jpeg'
    // ]
    return {
      score,
      show,
      index
      // images
    }
  },
  computed: {
    /**
     * 图片大图预览需要处理的数据
     */
    imageUrls () {
      return this.item.images.map(i => i.img)
    }
  },
  methods: {
    onChange (index) {
      this.index = index
    }
  }
}
</script>

<style lang="less">
.comment-item-box{
  padding: 5px 10px;
  border-bottom: 1px solid #f6f6f6;

  .cmt-header{
    display: flex;
    justify-content: space-between;

    .user{
      font-size: 12px;
    }
  }
  .cmt-content{
    color: #616161;
    padding: 5px 0;
    text-align: left;
    font-size: 12px;
    line-height: 2.0;
  }
  .cmt-imgs{
    padding: 5px;
    text-align: left;

    .van-image{
      margin-right: 5px;
    }
  }
}
</style>
