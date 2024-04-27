# 旅游网的接口文档
RESTful风格接口
* 200 请求数据成功
* 201 请求提交数据
* 400 参数错误
* 401 未登录
* 403 没有权限
* 500 服务器正忙

## 接口请求地址
1. 测试环境
   http://test.xxx.com
2. 生产环境

## 错误代码及提示
```json
{
  "error_code": "400000",
  "error_message": "该字段不能为空",
  "error_list": {
    "password": ["该字段不能为空"]
  }
}
```

## 请求头添加内容

##分页
|字段|类型|说明|
|---|---|---|
|page|int|当前页（默认为第一页）|

## 分页响应的参数
|字段|类型|说明|
|---|---|---|
|meta| |分页元数据，解释如下|
|local_count|int|根据所传入的条件检索出来的就条数|
|current_page|int|当前第几页|
|page_count|int|总页数|
|objects|Array|objects为返回的对象列表|

## 接口列表
### 1. 系统模块
* [1.1 轮播图接口](./system/slider_list.md)
### 2. 景点模块
* 
