# 1. Format Form API文档

- [1.1. Base URL](#11-base-url)
- [1.2. 问题类型](#12-问题类型)
  - [1.2.1. 单项选择](#121-单项选择)
  - [1.2.2. 多项选择](#122-多项选择)
  - [1.2.3. 简答](#123-简答)
  - [1.2.4. 验证器](#124-验证器)
- [1.3. 表单](#13-表单)
  - [1.3.1. 新建表单](#131-新建表单)
  - [1.3.2. 获取用户创建的全部表单](#132-获取用户创建的全部表单)

## 1.1. Base URL

https://api.jiangyinzuo.cn/

## 1.2. 问题类型  

### 1.2.1. 单项选择

*Parameters:*  
+ (String) type: "single_choice"
+ (Array) options: 由选项组成的数组
+ (Number) answer: 正确选项，用数组下标表示
+ [ (Number) score: 分数 ]

### 1.2.2. 多项选择

*Parameters:*
+ (String) type: "multiple_choice"
+ (Array) options: 由选项组成的数组
+ (Array) answer: 由下标组成的数组
+ [ (Array) score: 长度为二的数组，其中score[0]表示全对得分，score[1]表示部分选对得分，如[4, 2] ]

### 1.2.3. 简答

*Parameters:*
+ (String) type: "essay"
+ (String) answer: 回答
+ [ (Number) score: 分数 ]

### 1.2.4. 验证器

*Parameters:*
+ (String) type: "validator"
+ (String) rules: 正则表达式
+ (String) answer: 回答

## 1.3. 表单

表单中包含的问题类型见上文“问题类型”。

### 1.3.1. 新建表单

*URL:*
> POST /form_templates

*Parameters:* 
+ (String) open_id: 用户的openid
+ (String) title: 表单标题
+ (String) type: 表单类型
+ [ (Number) score: 总分 ]
+ (Number) time_limit: 时间限制，单位：分钟
+ [ (String) start_time: 开始时间，如"201903209000" ]
+ [ (String) end_time: 结束时间，如"201903211230" ]
+ (Array) questions: 对象数组，数组中元素均为问题类型 

*Response <font color="#AA5555">201</font>:*
> {  
> &emsp;"error_code": 0,  
> &emsp;"msg": "ok",  
> &emsp;"request": "POST&emsp;/form_templates"  
> }

### 1.3.2. 获取用户创建的全部表单

*URL:*
> GET /form_templates

*Parameters:*
+ (String) openid: 用户的openid

*Response <font color="#AA5555">200</font>:*
> {  
> &emsp;"error_code": 0,  
> &emsp;"msg": "ok",  
> &emsp;"request": "GET&emsp;/form_templates"  
> }