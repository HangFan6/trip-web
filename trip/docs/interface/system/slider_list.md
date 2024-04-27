## 首页轮播图的接口
### 请求地址
/system/slider/list/
### 调用方式
GET
### 请求参数
|字段|必选|类型|说明|
|---|---|---|---|
|type|true|int|轮播图类型（10：首页轮播）|

### 返回结果
```json
{
  "meta": {
    "total_count": 1,
    "page_count": 1,
    "current_count": 1
  },
  "object": [
    {
      "id": 1,
      "name": "广州长隆",
      "main_img": "/202402/sight/h1.jpg",
      "score": 4.3,
      "province": "广东省",
      "comment_count": 0
    }
  ]
}
```
### 返回字段的说明
|字段|类型|说明|
|---|---|---|
|meta| |分页原数据|
|objects| |objects下位轮比兔对象，详细如下|
|pk|int|记录ID|
|name|String|名称|
|desc|String|描述信息|
|img|String|图片地址|
|
