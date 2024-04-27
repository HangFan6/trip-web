const { defineConfig } = require('@vue/cli-service')
// Node.js中的模块
module.exports = {
  // http://localhost:8081/api/test
  // =>
  // http://localhost:8081/test

  // // eslint不建议子元素通过v-model修改父元素传的props值。可以尝试关闭eslint 语法检测
  // lintOneSave: false,

  devServer: {
    client:{overlay:false},
    proxy: {
      '/api': {
        // target: 'http://localhost:8081',
        // target: 'http://django.t.mukewang.com',
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''   // 需要重写的URL
        }
      },
      '/test': {
        // django中的url地址及端口号
        target: 'http://localhost:8000',
        changeOrigin: true,
        pathRewrite: {
          '^/test': ''   // 需要重写的URL
        }
      }
    }
  }
}

// module.exports = defineConfig({
//   transpileDependencies: true
// })
