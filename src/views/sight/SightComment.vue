<template>
  <!-- 景点评论 -->
  <div class="page-sight-comment">
    <!-- 页面头部 -->
    <div class="bar">
      <van-nav-bar
        left-text="返回"
        title="景点评论"
        left-arrow
        fixed
        @click-left="goBack"
      />
    </div>
    <!-- 评论加载及刷新 -->
    <van-pull-refresh class="sight-comment" v-model="refreshing" @refresh="onRefresh">
      <van-list
        v-model="loading"
        :finished="finished"
        finished-text="没有更多了"
        :error.sync="error"
        error-text="请求失败，点击重新加载"
        @load="getCommentList">
        <!-- <van-cell v-for="item in list" :key="item" :title="item" /> -->
        <comment-item v-for="item in commentList" :key="item.pk" :item="item"/>
      </van-list>
    </van-pull-refresh>
  </div>
</template>

<script>
// 评论项组件
import CommentItem from '@/components/sight/CommentItem.vue'
import { ajax } from '@/utils/ajax'
import { SightApis } from '@/utils/apis'

export default {
  components: {
    CommentItem
  },
  data () {
    return {
      // 评论列表
      commentList: [],
      // 当前第几页
      currentPage: 1,
      // 正在加载评论
      loading: false,
      // 所有评论加载完成
      finished: false,
      // 评论请求（默认成功）
      error: false,
      // 是否正在下拉刷新中
      refreshing: false
    }
  },
  methods: {
    goBack () {
      // 返回上一个页面
      this.$router.go(-1)
    },
    /**
     * 下拉刷新执行
     */
    onRefresh () {
      // 清空数据
      this.commentList = []
      this.currentPage = 1

      this.finished = true
      this.error = false

      // 重新加载数据
      this.getCommentList()
    },
    /**
     * 评论列表
     */
    // getCommentList () {
    //   const url = SightApis.sightCommentUrl.replace('#{id}', this.id)
    //   ajax.get(url).then(({ data: { objects } }) => {
    //     this.commentList = objects
    //   })
    // },
    /* 进行分页处理 */
    getCommentList () {
      const url = SightApis.sightCommentUrl.replace('#{id}', this.id)
      const loadPage = this.refreshing ? 1 : this.currentPage // 判断是否为刷新操作
      ajax.get(url, {
        params: {
          // page: this.currentPage
          page: loadPage
        }
      }).then(({ data: { meta, objects } }) => {
        if (this.refreshing) {
          this.commentList = objects // 刷新时，替换评论列表
        } else {
          if (loadPage === 1) {
            this.commentList = objects// 若是第一页，则直接替换当前评论列表
          } else {
            // 拼接评论列表
            this.commentList = this.commentList.concat(objects)
          }
        }
        // 加载状态结束
        this.loading = false
        // 加载下一页的评论
        this.currentPage = meta.current_page + 1
        // 数据全部加载完成：当前页码 == 总页数
        if (meta.current_page === meta.page_count) {
          this.finished = true
        }
        // 请求刷新完成后停止刷新
        this.refreshing = false
      }).catch(() => {
        // 停止加载
        this.loading = false
        // 请求失败
        this.error = true
        this.refreshing = false
      })
    }
  },
  mounted () {
    this.id = this.$route.params.id
    // this.getCommentList()  评论加载组件会自动加载
  }
}
</script>

<style lang="less">
.page-sight-comment{
  background-color: white;

  .bar{
    height: 45px;
  }
}
</style>
