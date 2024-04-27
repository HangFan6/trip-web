<template>
  <!-- 用户注册 -->
  <div class="page-account-register">
    <!-- 导航条 -->
    <van-nav-bar title="用户注册"
      left-text="返回"
      left-arrow
      @click-left="goBack"
    />
    <!-- 表单输入 -->
    <van-form @submit="onSubmit">
      <!-- 手机号 -->
      <van-cell-group inset>
        <van-field
          v-model="form.username"
          label="手机号码"
          placeholder="手机号码"
          maxlength="11"
          type="tel"
          clearable
          :rules="ruleName"
          @input="onPhoneChange"
        />
        <!-- 手机验证码 -->
        <van-field
          v-model="form.sms_code"
          center
          clearable
          label="短信验证码"
          placeholder="请输入短信验证码"
          :rules="[{ required: true, message: '请输入短信验证码' }]">
          <template #button>
            <send-sms-code ref="refSms" :phoneNum="form.username"/>
          </template>
        </van-field>
        <!-- 昵称 -->
        <van-field
          v-model="form.nickname"
          label="用户昵称"
          placeholder="用户昵称"
          maxlength="32"
          clearable
          :rules="[{ required: true, message: '请填写昵称' }]"
        />
        <van-field
          v-model="form.password"
          type="password"
          label="密码"
          placeholder="密码"
          :rules="[{ required: true, message: '请填写密码' }]"
        />
        <van-field
          v-model="form.passwordRepeat"
          type="password"
          label="确认密码"
          placeholder="确认密码"
          :rules="rulePassword"
        />
      </van-cell-group>
      <div style="margin: 16px;">
        <van-button round block type="primary" native-type="submit">
          注册
        </van-button>
      </div>
    </van-form>

    <!-- 文字提示 -->
    <div class="tips">
      注册表示同意 <a href="#">用户使用协议</a>及<a href="#">隐私条款</a>
    </div>
    <div class="tips">
      已有账号？ <router-link :to="{name: 'AccountLogin'}">点击登录</router-link>
    </div>
    <!-- 版权信息 -->
    <Copyright/>
  </div>
</template>

<script>
import Copyright from '@/components/common/CopyRight.vue'
import SendSmsCode from '@/components/common/SendSmsCode.vue'
import { ajax } from '@/utils/ajax'
import { AccountApis } from '@/utils/apis'
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
      // 重复密码验证
      rulePassword: [{
        required: true,
        message: '请重复密码'
      }, {
        validator: () => this.form.password === this.form.passwordRepeat,
        message: '请与上一次密码保持一致'
      }],
      form: {
        username: '',
        nickname: '',
        sms_code: '',
        password: '',
        passwordRepeat: ''
      }
    }
  },
  components: {
    Copyright,
    SendSmsCode
  },
  methods: {
    onSubmit () {
      // 提交表单
      // 1、调用接口
      ajax.post(AccountApis.registerUrl, {
        username: this.form.username,
        password: this.form.password,
        sms_code: this.form.sms_code,
        nickname: this.form.nickname
      }).then(({ data }) => {
        // 2、成功返回结果，用户信息写入Vuex
        this.$store.commit(types.UPDATE_USER_INFO, data)
        // 3、提示用户
        this.$notify({
          message: '注册成功',
          type: 'success'
        })
        // 4、跳转到个人中心（若写在下一行，注册成功后，需要进行登录）
        this.$router.replace({ name: 'mine' })
      })
    },
    goBack () {
      // 返回上一个页面
      this.$router.go(-1)
    },
    // 监听用户名（手机号）是否改变：重置验证码组件状态
    onPhoneChange () {
      this.$refs.refSms.reset()
    }
  }
}
</script>
