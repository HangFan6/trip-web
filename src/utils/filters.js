// 过滤器的定义

/**
 * 用户脱敏处理
 * @param {*} name 用户名
 */
function unameFormat (name) {
  if (!name) {
    return name
  }
  // 格式化显示1个字符
  return name.substr(0, 1) + '***'
}
export {
  unameFormat
}
