<template>
  <!-- 景点介绍 -->
  <div class="page-sight-info">
    <!-- 页面头部 -->
    <div class="bar">
      <van-nav-bar
        left-text="返回"
        title="景点介绍"
        left-arrow
        fixed
        @click-left="goBack"
      />
    </div>
    <div class="sight-info">
      <h3>入园参考</h3>
      <div class="tip1" v-html="sightInfo.entry_explain"></div>
      <h3>特色玩法</h3>
      <div class="tips" v-html="sightInfo.play_way"></div>
      <h3>温馨提示</h3>
      <div class="tips" v-html="sightInfo.tips"></div>
      <h3>交通到达</h3>
      <div class="tips" v-html="sightInfo.traffic"></div>
    </div>
  </div>
</template>

<script>
import { ajax } from '@/utils/ajax'
import { SightApis } from '@/utils/apis'

export default {
  data () {
    return {
      // 景点ID
      id: '',
      sightInfo: {}
    }
  },
  methods: {
    goBack () {
      // 返回上一个页面
      this.$router.go(-1)
    },
    /**
     * 获取景点介绍信息
     */
    getSightInfo () {
      const url = SightApis.sightInfoUrl.replace('#{id}', this.id)
      ajax.get(url).then(({ data }) => {
        this.sightInfo = data
        console.log(data)
      })
    }
  },
  created () {
    // 门票ID
    this.id = this.$route.params.id
    console.log(this.id)
    this.getSightInfo()
  }
}
</script>

<style lang="less">
.page-sight-info{
  background-color: white;
  .bar{
    height: 45px;
  }

  .sight-info{
    padding: 5px 15px;
    h3{
      text-align: center;
      line-height: 40px;
      margin: 10px auto;
      height: 40px;
      color: white;
      background-color:  rgb(45, 98, 211);
    }
    h4{
      margin: 5px auto;
    }
    .tip1{
      margin: 5px auto;
      p{
        margin: 0;
        text-align: left;
      }
    }
    img{
      width: 300px;
      height: 200px;
    }
    .tips p{
      text-align: left;
    }
  }
}
</style>
