/**
 * 项目中使用到的常量
 */
export const APP_VERSION = '1.0'
export const APP_PLATFORM = 'h5'

// 订单状态
export const ORDER_STATUS_ALL = 0
// 待支付
export const ORDER_STATUS_PAY = 11
// 已完成
export const ORDER_STATUS_DONE = 12
// 已取消
export const ORDER_STATUS_CANCEL = 13
export const ORDER_STATUS = {
  [ORDER_STATUS_ALL]: '全部',
  [ORDER_STATUS_PAY]: '待支付',
  [ORDER_STATUS_DONE]: '已完成',
  [ORDER_STATUS_CANCEL]: '已取消'
}
