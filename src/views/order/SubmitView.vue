<template>
  <div class="page-order-submit">
    <!-- 页面导航 -->
    <van-nav-bar title="订单"
      left-text="返回"
      left-arrow
      @click-left="goBack"
    />
    <!-- 描述信息 -->
    <div class="order-info">
      <div class="left">
        <h3>{{ticketDetail.name }}</h3>
        <div class="tips">{{ ticketDetail.desc }}</div>
        <div class="tags">
          <span>
            <van-icon name="clock-o"/>明日可定
          </span>
          <span>
            <van-icon name="clock-o"/>条件退
          </span>
        </div>
      </div>
      <div class="right">
        <div class="text-warning">￥{{ ticketDetail.sale_price }}/张</div>
        <van-button plain hairline type="info" size="mini" @click="showPopup=true">
          预定须知
        </van-button>
        <van-popup
          v-model="showPopup"
          round
          position="bottom"
          :style="{ height: '80%' }"
        >
          <TicketTips :ticketDetail="ticketDetail"/>
        </van-popup>
      </div>
    </div>
    <!-- 提交表单 -->
    <van-form @submit="onSubmit" class="form-box">
      <van-cell-group inset class="form-group">
        <van-cell title="选择出行日期"
          :value="form.play_date"
          @click="showCalendar = true"
        />
        <van-calendar v-model="showCalendar" @confirm="onConfirm" />
      </van-cell-group>
      <van-cell-group inset class="form-group">
        <van-field name="stepper" label="购买数量">
          <template #input>
            <van-stepper v-model="form.buy_count" />
          </template>
        </van-field>
      </van-cell-group>
      <van-cell-group inset class="form-group">
        <van-field
          v-model="form.to_user"
          type="text"
          label="收件人"
          placeholder="收件人"
          :rules="[{ required: true, message: '请填写收件人' }]"
        />
        <van-field
          v-model="form.to_phone"
          type="text"
          label="手机号码"
          placeholder="手机号码"
          :rules="[{ required: true, message: '请填写手机号码' }]"
        />
      </van-cell-group>
      <!-- 提交表单 -->
      <van-submit-bar :price="totalPrice" button-text="提交订单"/>
    </van-form>
  </div>
</template>

<script>
import { ajax } from '@/utils/ajax'
import { OrderApis, SightApis } from '@/utils/apis'
import { mapState } from 'vuex'
import TicketTips from '@/components/sight/TicketTips.vue'

export default {
  data () {
    return {
      // 门票ID
      id: '',
      // 预定须知弹框显示
      showPopup: false,
      // 日期选择弹框
      showCalendar: false,
      // price: 98,
      // 门票详细信息
      ticketDetail: {},
      form: {
        play_date: '',
        buy_count: 1,
        to_user: '',
        to_phone: ''
      }
    }
  },
  components: {
    TicketTips
  },
  methods: {
    goBack () {
      // 返回上一个页面
      this.$router.go(-1)
    },
    // 选择日期
    formatDate (date) {
      return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`
    },
    onConfirm (date) {
      // 隐藏日历弹框
      this.showCalendar = false
      // 保存数据
      this.form.play_date = this.formatDate(date)
    },
    /**
     * 门票详情
     */
    getTicketDetail () {
      const url = SightApis.ticketDetailUrl.replace('#{id}', this.id)
      ajax.get(url).then(({ data }) => {
        this.ticketDetail = data
      })
    },
    // 提交表单
    onSubmit () {
      console.log('提交表单')
      // ajax接口调用
      ajax.post(OrderApis.ticketSubmitUrl, {
        ticket_id: this.id,
        ...this.form
      }).then(({ data }) => {
        // 提示用户
        this.$notify({
          type: 'success',
          message: '提交成功，请支付'
        })
        // 跳转到支付页面
        this.$router.replace({ name: 'OrderPay', params: { sn: data.sn } })
      })
    }
  },
  created () {
    // 门票ID
    this.id = this.$route.params.id
    this.form.to_user = this.nickname || ''
    this.form.to_phone = this.phoneNum || ''
    // 获取门票信息
    this.getTicketDetail()
  },
  computed: {
    /**
     * 计算总价（单位为：分）
     */
    totalPrice () {
      // console.log(this.ticketDetail.sale_price * this.form.buy_count * 100, '~~~~')
      return this.ticketDetail.sale_price * this.form.buy_count * 100
    },
    /**
     * 从vuex读取手机号码
     */
    ...mapState({
      phoneNum: state => state.user.username,
      nickname: state => state.user.nickname
    })
  }
}
</script>

<style lang="less">
.page-order-submit{
  .order-info{
    display: flex;
    padding: 10px;
    background: white;
    .left{
      flex: 1;
      text-align: left;
      h3{
        padding: 5px 0;
        margin: 0 auto;
      }
      .tips{
        padding: 10px 0;
        color: #999;
        font-size: 12px;
      }
    }
    .right{
      width: 20%;
      text-align: right;
    }
  }
  /* 表单区域 */
  .form-box{
    .form-group{
      margin-top: 10px;
      background: white;
      .van-cell__title{
        text-align: left;
      }
    }
  }
}
</style>
