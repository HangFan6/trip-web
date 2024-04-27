<template>
  <!-- 用户登录 -->
  <div class="page-account-login">
    <!-- 导航条 -->
    <van-nav-bar title="用户登录"
      left-text="返回"
      left-arrow
      @click-left="goBack"
    />
    <!-- 表单输入 -->
    <van-form @submit="onSubmit">
      <van-cell-group inset>
        <van-field
          v-model="username"
          label="用户名"
          placeholder="用户名"
          maxlength="11"
          type="tel"
          clearable
          :rules="ruleName"
        />
        <van-field
          v-model="password"
          type="password"
          label="密码"
          placeholder="密码"
          :rules="[{ required: true, message: '请填写密码' }]"
        />
      </van-cell-group>
      <div style="margin: 16px;">
        <van-button round block type="primary" native-type="submit">
          登录
        </van-button>
      </div>
    </van-form>

    <!-- 文字提示 -->
    <div class="tips">
      登录表示同意 <a href="#">用户使用协议</a>及<a href="#">隐私条款</a>
    </div>
    <div class="tips">
      没有账号？ <router-link :to="{name: 'AccountRegister'}">点击注册</router-link>
    </div>
    <!-- 版权信息 -->
    <Copyright/>
  </div>
</template>

<script>
import Copyright from '@/components/common/CopyRight.vue'
import { AccountApis } from '@/utils/apis'
import { ajax } from '@/utils/ajax'
import * as types from '@/store/mutation-types'

export default {
  data () {
    return {
      // 用户名的验证规则
      ruleName: [{
        required: true,
        message: '请填写用户名'
      }, {
        // 正则验证
        pattern: /1\d{10}/,
        message: '请填正确的手机号'
      }],
      username: '',
      password: ''
    }
  },
  components: {
    Copyright
  },
  methods: {
    onSubmit () {
      // 提交表单
      // 1、调用接口
      ajax.post(AccountApis.loginUrl, {
        username: this.username,
        password: this.password
      }).then(({ data }) => {
        // 2、拿到用户信息，存储到Vuex
        this.$store.commit(types.UPDATE_USER_INFO, data)
        this.$toast('登录成功')
        // 跳转到个人中心
        this.$router.replace({ name: 'mine' })
      }).catch(({ response: { data } }) => {
        // 3、如果出现异常，需要给用户提示信息
        console.log(data)
        this.$toast(`${data.error_code},${data.error_msg}`)
      })
    },
    goBack () {
      // 返回上一个页面
      this.$router.go(-1)
    }
  }
}
</script>
<style lang="less">
</style>
