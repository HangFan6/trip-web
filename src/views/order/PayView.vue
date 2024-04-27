<template>
  <!-- 订单确认及支付 -->
  <div class="page-order-pay">
    <!-- 页面导航 -->
    <van-nav-bar title="订单支付"
      left-text="返回"
      right-text="取消订单"
      left-arrow
      @click-left="goBack"
      @click-right="goCancelOrder"
    />
    <!-- 订单号 -->
    <van-cell title="订单号"
      :value="sn"
      class="order-num"
    />
    <!-- 描述信息 -->
    <div class="order-info" v-for="item in orderDetail.items" :key="item.pk">
      <div class="left">
        <h3>{{ item.flash_name }}</h3>
        <div>
          <van-icon name="clock-o"/>{{ item.remark }}
        </div>
        <!-- <div class="tips">短信接收</div> -->
      </div>
      <div class="right">
        <van-icon name="arrow"/>
      </div>
    </div>
    <!-- 提交表单 -->
    <van-submit-bar :price="orderDetail.buy_amount * 100" button-text="立即支付" @submit="onSubmit" />
  </div>
</template>

<script>
import { ajax } from '@/utils/ajax'
import { OrderApis } from '@/utils/apis'
import * as constents from '@/utils/constants'

export default {
  data () {
    return {
      // 订单流水号
      sn: '',
      // 订单信息
      orderDetail: {}
      // 总价格（单位：分）
      // totalPrice: 25000
    }
  },
  methods: {
    /**
     * 获取订单详细信息
     */
    getOrderDetail () {
      const url = OrderApis.orderDetailUrl.replace('#{sn}', this.sn)
      ajax.get(url).then(({ data }) => {
        this.orderDetail = data
      })
    },
    // 确认支付
    onSubmit () {
      this.$dialog.confirm({
        title: '温馨提示',
        message: `确认支付 ${this.orderDetail.buy_amount} ？`
      }).then(() => {
        // 调用支付接口
        const url = OrderApis.orderDetailUrl.replace('#{sn}', this.sn)
        ajax.post(url).then(() => {
          // 提示语
          this.$notify({
            type: 'success',
            message: '支付成功，将为您跳转到支付列表'
          })
          // 跳转到我的订单列表
          this.$router.replace({ name: 'OrderList', params: { status: constents.ORDER_STATUS_ALL } })
        })
      })
    },
    // 取消支付
    goBack () {
      // 返回上一个页面
      this.$dialog.confirm({
        title: '温馨提示',
        message: '您还未支付，确认取消支付？'
      }).then(() => {
        this.$router.go(-1)
      })
    },
    // 取消订单
    goCancelOrder () {
      this.$dialog.confirm({
        title: '温馨提示',
        message: '确认取消该订单？'
      }).then(() => {
        // TODO 调用接口，取消订单
        const url = OrderApis.orderDetailUrl.replace('#{sn}', this.sn)
        // put方式调用接口
        ajax.put(url).then(res => {
          console.log('res：', res)
          // 给用户提示
          if (res.status === 201) {
            this.$notify({
              type: 'success',
              message: '订单已成功取消'
            })
          } else if (res.status === 200) {
            this.$notify({
              type: 'warning',
              message: '订单被取消，请勿重复操作'
            })
          }
          this.$router.go(-1)
        })
      })
    }
  },
  created () {
    // 订单流水号
    this.sn = this.$route.params.sn
    // 获取订单信息
    this.getOrderDetail()
  }
}
</script>

<style lang="less">
.page-order-pay{
  .order-num{
    .van-cell__title{
      text-align: left;
    }
    .van-cell__value{
      flex: 3;
    }
  }
  .order-info{
    display: flex;
    padding: 10px;
    background: white;
    margin-top: 10px;

    .left{
      flex: 1;
      text-align: left;
      h3{
        padding: 5px 0;
        margin: 0;
      }
    }
  }
}
</style>
