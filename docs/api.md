# Format Form API文档

- [Base URL](#base-url)
- [Error Code](#error-code)
- [表单模板](#表单模板)
  - [新建表单](#新建表单)
  - [获取用户创建的全部表单](#获取用户创建的全部表单)
  - [删除表单模板](#删除表单模板)
- [表单数据](#表单数据)
  - [提交表单数据](#提交表单数据)
## Base URL

https://api.jiangyinzuo.cn/

## Error Code

+ 4001: 未知错误、默认错误
+ 4002: 参数错误
+ 5000: 服务端错误
+ 5101: 查询错误

## 表单模板

表单中包含的问题类型见上文“问题类型”。

### 新建表单

*URL:*
> POST /form_templates

*Parameters:* 
+ (String) open_id: 用户的openid
+ (String) title: 表单标题
+ (String) type: 表单类型
+ [ (Number) score: 总分 ]
+ [ (Number) time_limit: 时间限制，单位：分钟 ]
+ [ (String) start_time: 开始时间，如"201903209000" ]
+ [ (String) end_time: 结束时间，如"201903211230" ]
+ (Array) questions: [{   
+   "desc": (String),
+   "type": (String) ["select", "radio", "essay"],
+   "necessary": (String) ["yes", "no"],
+   "detail": (Array, String) ["option1", "option2"], <re>
+ }, ...]

*Response <font color="#AA5555">201</font>:*
> {  
> &emsp;"error_code": 0,  
> &emsp;"form_temp_id": "_id",  
> &emsp;"msg": "ok",  
> &emsp;"request": "POST&emsp;/form_templates"  
> }

### 获取用户创建的全部表单

*URL:*
> GET /form_templates

*Parameters:*
+ (String) openid: 用户的openid

*Response <font color="#AA5555">200</font>:*
> {  
> &emsp;"error_code": 0,  
> &emsp;"msg": "ok",  
> &emsp;"request": "GET&emsp;/form_templates"  
> &emsp;"question_temps": [Array]
> }

### 删除表单模板

*URL:*
> DELETE /form_templates

*Parameters:*
+ (String) openid: 用户的openid
+ (String) _id: mongodb的ObjectId

*Response <font color="#AA5555">200</font>:*
> {  
> &emsp;"error_code": 0,   
> &emsp;"msg": "ok",   
> &emsp;"request": "DELETE /form_templates"  
> }  

## 表单数据

### 提交表单数据

*URL:*
> POST /form_data

*Parameters:*