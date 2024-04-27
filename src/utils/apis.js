/**
 * 存放项目中所有的接口地址
 */

// 主机地址（需要解决跨域问题）
const apiHost = 'http://localhost:8081/api'
/**
 * 用户账户相关的接口
 */
const AccountApis = {
  // 用户登录
  loginUrl: apiHost + '/accounts/user/api/login/',
  // 用户退出登录
  logoutUrl: apiHost + '/accounts/user/api/logout/',
  // 用户信息
  userInfoUrl: apiHost + '/accounts/user/api/info/',
  // 用户注册
  registerUrl: apiHost + '/accounts/user/api/register/'
}

// 系统模块接口
const SystemApis = {
  // 轮播图列表
  sliderListUrl: apiHost + '/system/slider/list/',
  // 发送短信验证码
  sendSmsCodeUrl: apiHost + '/system/send/sms/'
}

// 景点模块接口
const SightApis = {
  // 景点列表
  sightListUrl: apiHost + '/sight/sight/list/',
  // 缓存优化后的景点列表URL
  sightListCacheUrl: apiHost + '/sight/sight/list/cache/',
  // 景点详情
  sightDetailtUrl: apiHost + '/sight/sight/detail/#{id}/',
  // 门票列表
  sightTicketUrl: apiHost + '/sight/ticket/list/#{id}/',
  // 评论列表
  sightCommentUrl: apiHost + '/sight/comment/list/#{id}/',
  // 景点介绍
  sightInfoUrl: apiHost + '/sight/sight/info/#{id}/',
  // 门票详情
  ticketDetailUrl: apiHost + '/sight/ticket/detail/#{id}/'
}

// 订单模块接口
const OrderApis = {
  // 订单列表
  orderListUrl: apiHost + '/order/order/list/',
  // 订单详情、支付、删除、取消
  orderDetailUrl: apiHost + '/order/order/detail/#{sn}/',
  // 订单提交
  ticketSubmitUrl: apiHost + '/order/ticket/submit/'
}

export {
  AccountApis,
  SystemApis,
  SightApis,
  OrderApis
}
