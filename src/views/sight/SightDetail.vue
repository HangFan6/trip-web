<template>
  <!-- 景点详情 -->
  <div class="page-sight-detail">
    <!-- 页面头部 -->
    <div class="bar">
      <van-nav-bar
        left-text="返回"
        title="景点详情"
        left-arrow
        fixed
        @click-left="goBack"
      />
    </div>
    <!-- 大图 -->
    <div class="sight-banner">
      <van-image :src="sightDetail.img" width="100%" height="100%"/>
      <div class="tips">
        <router-link class="pic-sts" :to="{name: 'SightImage', params: {id:id}}">
          <van-icon name="video-o"/>
          <span>{{ sightDetail.image_count }} 图片</span>
        </router-link>
        <div class="title">{{ sightDetail.name }}</div>
      </div>
    </div>
    <!-- 评分、景点介绍 -->
    <div class="sight-info">
      <div class="left" @click="goComment()">
        <div class="info-title">
          <strong>{{ sightDetail.score }} 分</strong>
          <small>很棒</small>
        </div>
        <div class="info-tips">{{ sightDetail.comment_count }} 评论</div>
        <van-icon name="arrow"/>
      </div>
      <div class="right" @click="goIntroduce()">
        <div class="info-title">
          <span>景点介绍</span>
        </div>
        <div class="info-tips">开放时间、贴士</div>
        <van-icon name="arrow"/>
      </div>
    </div>
    <!-- 地址信息 -->
    <van-cell :title="fullArea"
    icon="location-o"
    is-link
    :title-style="{'text-align':'left'}">
      <!-- 使用 right-icon 插槽来自定义右侧图标 -->
      <template #right-icon>
        <van-icon name="arrow"/>
      </template>
    </van-cell>
    <!-- 门票列表 -->
    <div class="sight-ticket">
      <van-cell title="门票" icon="bookmark-o" title-style="text-align: left"/>
      <div class="ticket-item" v-for="item in ticketList" :key="item.pk">
        <div class="left">
          <div class="title">{{ item.name }}</div>
          <div class="tips">
            <van-icon name="clock-o" />
            <span>{{ item.desc }}</span>
          </div>
          <div class="tags">
            <van-tag mark type="primary">标签1</van-tag>
          </div>
        </div>
        <div class="right">
          <div class="right-box">
            <div class="price">
              <span>￥</span>
              <strong>{{ item.sale_price }}</strong>
            </div>
            <!-- 订单支付接口 -->
            <router-link :to="{name: 'OrderSubmit', params: {id: item.pk}}">
              <van-button size="small" color="linear-gradient(to right, #ff6034, #ee0a24)">
                预定
              </van-button>
            </router-link>
          </div>
        </div>
      </div>
    </div>
    <!-- 用户评价 -->
    <div class="sight-comment">
      <van-cell title="热门评论" icon="comment-o" title-style="text-align: left"/>
      <comment-item v-for="item in commentList" :key="item.pk" :item="item"/>
      <router-link class="link-more" :to="{name: 'SightComment', params: {id: id}}">查看更多</router-link>
    </div>
  </div>
</template>

<script>
// 评论项组件
import CommentItem from '@/components/sight/CommentItem.vue'
import { ajax } from '@/utils/ajax'
import { SightApis } from '@/utils/apis'

export default {
  data () {
    return {
      id: '',
      // 景点详细信息
      sightDetail: {},
      // 门票列表
      ticketList: [],
      // 评论列表
      commentList: []
    }
  },
  components: {
    CommentItem
  },
  computed: {
    /**
     * 地址的全部信息：处理area和town可能为空的情况
     */
    fullArea () {
      let area = this.sightDetail.province + this.sightDetail.city
      if (this.sightDetail.area) {
        area += this.sightDetail.area
      }
      if (this.sightDetail.town) {
        area += this.sightDetail.town
      }
      return area
    }
  },
  watch: {
    $route () {
      // 监听路由，重载数据
      this.loadData()
    }
  },
  methods: {
    // 跳转到景点介绍
    goIntroduce () {
      this.$router.push({ name: 'SightInfo', params: { id: this.id } })
    },
    // 跳转到评论列表
    goComment () {
      this.$router.push({ name: 'SightComment', params: { id: this.id } })
    },
    loadData () {
      this.id = this.$route.params.id
      // 获取景点信息
      this.getSightDetail()
      // 门票列表
      this.getTicketList()
      // 评论列表
      this.getCommentList()
    },
    goBack () {
      // 返回上一个页面
      this.$router.go(-1)
    },
    /**
     * 获取详细信息
     */
    getSightDetail () {
      const url = SightApis.sightDetailtUrl.replace('#{id}', this.id)
      ajax.get(url).then(({ data }) => {
        this.sightDetail = data
      })
    },
    /**
     * 获取门票列表
     */
    getTicketList () {
      const url = SightApis.sightTicketUrl.replace('#{id}', this.id)
      ajax.get(url).then(({ data: { objects } }) => {
        this.ticketList = objects
      })
    },
    /**
     * 评论列表
     */
    getCommentList () {
      const url = SightApis.sightCommentUrl.replace('#{id}', this.id)
      ajax.get(url).then(({ data: { objects } }) => {
        this.commentList = objects
      })
    }
    // /**
    //  * 获取景点介绍信息
    //  */
    // getSightInfo () {
    //   const url = SightApis.sightInfoUrl.replace('#{id}', this.id)
    //   ajax.get(url).then(({ data }) => {
    //     this.sightDetail = data
    //   })
    // }
  },
  created () {
    this.loadData()
  }
}
</script>

<style lang="less">
.page-sight-detail{
  .bar{
    height: 45px;
  }
  /*景点大图*/
  .sight-banner{
    position: relative;
    .tips{
      position: absolute;
      left: 10px;
      bottom: 10px;
      font-size: 16px;
      color: white;

      .pic-sts{
        color: white;
        border-radius: 30px;
        font-size: 14px;
        /* 设置背景透明度*/
        background-color: rgba(0, 0, 0, 0.6);
      }
    }
  }
  /*评分、景点介绍*/
  .sight-info {
    display: flex;
    background-color: white;
    border-bottom: 1px solid #f6f6f6;

    & > div{
      flex: 1;
      position: relative;
    }
    .right{
      border-left: 1px solid #f6f6f6;
    }
    .info-title{
      text-align: left;
      padding: 5px 10px;
      strong{
        color: #ff8300;
      }
    }
    .info-tips{
      color: #999;
      font-size: 12px;
      text-align: left;
      padding: 5px 10px;
    }
    .van-icon{
      position: absolute;
      right: 5px;
      top: 5px;
    }
  }
  /*门票列表*/
  .sight-ticket{
    margin-top: 10px;
    background-color: white;

    .ticket-item{
      display: flex;
      border-bottom: 1px solid #f6f6f6;
      padding-bottom: 10px;

      .left{
        flex: 1;
        text-align: left;
        padding: 5px 10px;

        .title{
          padding: 5px 0;
        }
        .tips{
          font-size: 12px;
        }
      }
      .right{
        width: 100px;

        .right-box{
          margin: 10px auto;
          .price{
            color: #ff8300;
            strong{
              font-size: 20px;
            }
          }
        }
      }
    }
  }
  /*评论列表*/
  .sight-comment{
    margin-top: 10px;
    background-color: white;
  }
  /*查看更多*/
  .link-more{
    display: block;
    color: #666;
    padding: 10px;
  }
}
</style>
