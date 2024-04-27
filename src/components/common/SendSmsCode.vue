<template>
  <!-- 短息验证码发送的相关逻辑 -->
  <van-button
    size="small"
    type="primary"
    @click.prevent="sendSmsCode"
    :disabled="isSmsSend">
    {{ sendBtnText }}
  </van-button>
</template>
<script>
import { ajax } from '@/utils/ajax'
import { SystemApis } from '@/utils/apis'

export default {
  data () {
    return {
      sendBtnText: '点击发送验证码',
      counter: 60,
      timer: null,
      // 是否已经发送验证码
      isSmsSend: false
    }
  },
  props: ['phoneNum'],
  methods: {
    /**
     * 发送验证码
     */
    sendSmsCode () {
      // 判断手机号是否已输入
      if (!this.phoneNum) {
        this.$notify('请输入手机号')
        return false
      }
      // TODO 调用接口，发送短信验证码
      ajax.post(SystemApis.sendSmsCodeUrl, {
        phone_num: this.phoneNum
      }).then(({ data }) => {
        // 提示用户验证码已经发送
        this.$notify({
          message: `验证码为： ${data.sms_code}, ${data.timeout / 60}分钟内有效`,
          // 提示时间10s=1000ms * 10
          duration: 1000 * 10,
          type: 'success'
        })
        // 验证码发送后，开启倒计时
        this.isSmsSend = true
        this.countDown()
      }).catch(err => {
        // 如果产生异常，提示用户重新操作
        this.isSmsSend = false
        this.sendBtnText = '点击发送验证码'
        console.log(err)
      })
      this.isSmsSend = true
      // 开启倒计时，1分钟后才可再次点击
      this.countDown()
    },
    /**
     * 倒计时
     */
    countDown () {
      // 每隔1s调用一次该函数
      this.timer = setInterval(() => {
        // ES6中新增的使用方法  ``
        this.sendBtnText = `(${this.counter}秒)后重新发送`
        this.counter--
        console.log(this.counter)
        if (this.counter < 0) {
          // 清除
          // clearInterval(this.timer)
          this.reset()
        }
      }, 1000)
    },
    reset () {
      this.isSmsSend = false
      this.sendBtnText = '点击发送验证码'
      if (this.timer) {
        clearInterval(this.timer)
        this.counter = 60
        this.timer = null
      }
    }
  }
}
</script>
