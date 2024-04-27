<template>
  <!-- 我的订单列表页面 -->
  <div class="page-order-list">
    <!-- 顶部导航 -->
    <van-nav-bar title="我的订单"
      left-text="返回"
      left-arrow
      @click-left="goBack"
    />
    <!-- 按钮状态切换 -->
    <van-tabs v-model="status" @click="tabChange">
      <van-tab
        v-for="(value, key, index) in constants.ORDER_STATUS"
        :title="value"
        :name="key"
        :key="index"></van-tab>
    </van-tabs>
    <!-- 订单记录 -->
    <div class="order-list">
      <div class="order-item" v-for="item in dataList" :key="item.sn" v-show="item.sn">
        <div class="order-head">
          <div class="order-num">订单号：{{ item.sn }}</div>
          <div class="order-status text-warning">{{ constants.ORDER_STATUS[item.status] }}</div>
        </div>
        <div class="order-body">
          <div class="order-left">
            <!-- src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg" -->
            <van-image
              width="100"
              height="100"
              :src="item.item_first.flash_img"
            />
          </div>
          <div class="order-right">
            <div class="title">{{ item.item_first.flash_name }}</div>
            <div class="remark">{{ item.item_first.remark }}</div>
          </div>
        </div>
        <div class="order-footer">
          <div>总共{{ item.buy_count }}件商品，合计{{ item.buy_amount }}元</div>
          <van-button plain hairline round size="small" type="danger"
            v-if="item.status == constants.ORDER_STATUS_PAY"
            @click="goPay(item)">
            去支付
          </van-button>
          <van-button plain hairline round size="small" type="danger"
            v-if="item.status == constants.ORDER_STATUS_DONE || item.status == constants.ORDER_STATUS_CANCEL"
            @click="deleteOrder(item)">
            删除订单
          </van-button>
          <van-button plain round size="small" type="info">订单详情</van-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ajax } from '@/utils/ajax'
import { OrderApis } from '@/utils/apis'
import * as constants from '@/utils/constants'

export default {
  data () {
    return {
      // 订单状态
      status: 0,
      // 订单列表
      dataList: [],
      constants
    }
  },
  watch: {
    /**
     * 监听路由：手动更改路由时，也发生响应页面跳转
     */
    $route () {
      this.loadData()
    }
  },
  methods: {
    goBack () {
      // 返回个人中心
      this.$router.push({ name: 'mine' })
    },
    /**
     * 加载订单列表
     */
    getDataList () {
      ajax.get(OrderApis.orderListUrl, {
        params: {
          status: this.status
        }
      }).then(({ data }) => {
        this.dataList = data.objects
      })
    },
    /**
     * 加载页面的数据
     */
    loadData () {
      // 获取订单状态（active类型需要字符串）
      this.status = this.$route.params.status.toString()
      // 清空数据
      this.dataList = []
      // 加载数据列表
      this.getDataList()
    },
    /**
     * 订单中的tab点击之后，重新获取数据
     */
    tabChange (name, value) {
      // 0 全部
      console.log(name, value)
      this.$router.push({ name: 'OrderList', params: { status: name } })
    },
    /**
     * 跳转到支付页面
     */
    goPay (item) {
      this.$router.push({ name: 'OrderPay', params: { sn: item.sn } })
    },
    /**
     * 删除订单
     */
    deleteOrder (item) {
      // 弹框确认删除
      this.$dialog.alert({
        title: '温馨提示',
        message: '删除订单将无法恢复，确认删除订单？'
      }).then(() => {
        // 调用接口
        const url = OrderApis.orderDetailUrl.replace('#{sn}', item.sn)
        ajax.delete(url).then(res => {
          // 告诉用户，删除成功
          if (res.status === 201) {
            this.$notify({
              type: 'success',
              message: '删除成功'
            })
            // 隐藏界面显示（使用v-show进行显示绑定）
            item.sn = ''
          }
        })
      })
    }
  },
  mounted () {
    this.loadData()
  }
}
</script>

<style lang="less">
.page-order-list{
  .order-list{
    padding: 10px;

    .order-item{
      background: white;
      padding: 10px;
      border-radius: 10px;
      margin-bottom: 10px;
    }

    .order-head{
      display: flex;
      justify-content: space-between;
      font-size: 12px;
    }
    .order-status{
      font-size: 13px;
    }
  }
  .order-body{
    padding: 10px 0;
    display: flex;
    .order-left{
      width: 100px;
      height: 100px;
    }
    .order-right{
      flex: 1;
      text-align: left;
      padding-left: 10px;

      .title{
        font-size: 16px;
        padding: 5px 0;
      }
      .remark{
        font-size: 12px;
        color: #999;
      }
    }
  }
  .order-footer{
    text-align: right;
    font-size: 12px;

    .van-button{
      margin-left: 5px;
      margin-top: 10px;
    }
  }
}
</style>
