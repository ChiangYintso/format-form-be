# Format Form API文档

- [Base URL](#base-url)
- [Error Code](#error-code)
- [问题类型](#问题类型)
  - [单项选择](#单项选择)
  - [多项选择](#多项选择)
  - [简答](#简答)
  - [验证器](#验证器)
- [表单](#表单)
  - [新建表单](#新建表单)
  - [获取用户创建的全部表单](#获取用户创建的全部表单)
  - [获取一个表单模板](#获取一个表单模板)
  - [删除表单模板](#删除表单模板)
## Base URL

https://api.jiangyinzuo.cn/

## Error Code

+ 4001: 未知错误、默认错误
+ 4002: 参数错误
+ 5000: 服务端错误

## 问题类型  

每个问题均为一个对象

### 单项选择

*Parameters:*  
+ (String) type: "single_choice"
+ (Array) options: 由选项组成的数组
+ (Number) answer: 正确选项，用数组下标表示
+ [ (Number) score: 分数 ]

### 多项选择

*Parameters:*
+ (String) type: "multiple_choice"
+ (Array) options: 由选项组成的数组
+ (Array) answer: 由下标组成的数组
+ [ (Array) score: 长度为二的数组，其中score[0]表示全对得分，score[1]表示部分选对得分，如[4, 2] ]

### 简答

*Parameters:*
+ (String) type: "essay"
+ (String) answer: 回答
+ [ (Number) score: 分数 ]

### 验证器

*Parameters:*
+ (String) type: "validator"
+ (String) rules: 正则表达式
+ (String) answer: 回答

## 表单

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
+ (Array) questions: 对象数组，数组中元素均为问题类型 

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

### 获取一个表单模板

*URL:*
> GET /form_templates/?object_id=OBJECT_ID

*Parameters:*
+ (String) object_id: 表单在mongodb中存储的_id

*Response <font color="#AA5555">200</font>:*
> {  
> &emsp;"error_code": 0,  
> &emsp;"msg": "ok",  
> &emsp;"request": "GET&emsp;/form_templates"  
> &emsp;"form_temps": [Object]
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
