<template>
  <!-- 个人中心 -->
  <div class="page-mine">
    <!-- 标题 -->
    <van-nav-bar title="个人中心" fixed/>
    <!-- 用户基本信息：头像、昵称 -->
    <div class="user-header">
      <div class="avatar" v-if="user.avatar">
        <van-image
          round
          fit="cover"
          width="100px"
          height="100px"
          :src="user.avatar"
        />
      </div>
      <div class="avatar" v-else>
        <van-image
          round
          width="10rem"
          height="10rem"
          src="/static/mine/avatar.png"
        />
      </div>
      <div>
        <p>欢迎您，{{ user.nickname }}！</p>
        <a class="btn-link" href="#" @click="logout">退出登录</a>
      </div>
    </div>
    <!-- 订单菜单列表 -->
    <van-row class="user-links">
      <van-col span="6">
        <router-link :to="{name: 'OrderList', params: {status: constents.ORDER_STATUS_ALL}}">
          <van-icon name="notes-o" />
          <span>全部订单</span>
        </router-link>
      </van-col>
      <van-col span="6">
        <router-link :to="{name: 'OrderList', params: {status: constents.ORDER_STATUS_PAY}}">
          <van-icon name="pending-payment" />
          <span>待支付</span>
        </router-link>
      </van-col>
      <van-col span="6">
        <router-link :to="{name: 'OrderList', params: {status: constents.ORDER_STATUS_DONE}}">
          <van-icon name="certificate" />
          <span>已完成</span>
        </router-link>
      </van-col>
      <van-col span="6">
        <router-link :to="{name: 'OrderList', params: {status: constents.ORDER_STATUS_CANCEL}}">
          <van-icon name="logistics" />
          <span>已取消</span>
        </router-link>
      </van-col>
    </van-row>
    <!-- 底部导航 -->
    <TripFooter/>
  </div>
</template>
<script>
import TripFooter from '@/components/common/FooterView.vue'
import { ajax } from '@/utils/ajax'
import { AccountApis } from '@/utils/apis'
import { mapState } from 'vuex'
import * as types from '@/store/mutation-types'
import * as constents from '@/utils/constants'

export default {
  data () {
    return {
      constents
    }
  },
  components: {
    TripFooter
  },
  methods: {
    /***
     * 查询用户信息
     */
    getUserInfo () {
      ajax.get(AccountApis.userInfoUrl).then(({ data }) => {
        console.log('mine-getUserInfo', data)
        this.$store.commit(types.UPDATE_USER_INFO, data)
      })
    },
    // /**
    //  * 更换头像
    //  */
    //  changeAvatar () {
    //   window.alert('头像点击')
    //  },
    /**
     * 退出登录
     */
    logout () {
      // 调用接口，退出登录
      ajax.get(AccountApis.logoutUrl).then(() => {
        // 提示用户
        this.$notify({
          message: '欢迎下次再来！',
          type: 'success'
        })
      })
      // 删除用户登录信息
      this.$store.commit(types.DELETE_USER_INFO)
      // 跳转到首页
      this.$router.push({ name: 'home' })
    }
  },
  computed: {
    ...mapState(['user'])
  },
  mounted () {
    this.getUserInfo()
  }
}
</script>
<style lang="less">
.page-mine{
  .van-nav-bar--fixed{
    background-color: transparent;
  }
  .van-nav-bar__title{
    color: white;
  }
  .user-header{
    background: url(../../public/static/mine/bg.jpg) no-repeat center;
    background-size: 100% auto;
    color: white;
    height: 280px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    // .avatar .van-image__img{
    //   width: 80px;
    //   height: 80px;
    // }
  }
  .btn-link{
    color: white;
  }
  .user-links{
    padding: 15px 0;
    font-size: 12px;
    text-align: center;
    background-color: white;
    .van-icon{
      display: block;
      /* 图标为字体图标 */
      font-size: 24px;
    }
  }
}
</style>
