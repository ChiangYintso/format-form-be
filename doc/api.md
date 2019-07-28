# Format Form api文档

- [Base URL](#base-url)
- [表单](#表单)
  - [新建表单](#新建表单)
  - [获取用户创建的全部表单](#获取用户创建的全部表单)

## Base URL

https://api.jiangyinzuo.cn/

## 表单

### 新建表单

*URL:*
> POST /form_templates

*Parameters:* 
> {  
> &emsp;"openid": "用户的openid",  
> &emsp;"form_data": {  
> &emsp;&emsp;"title": "表单标题",  
> &emsp;&emsp;"type": "表单类型",  
> &emsp;&emsp;"score": "总分",  
> &emsp;&emsp;"time_limit": "时间限制",  
> &emsp;&emsp;"items": [{  
> &emsp;&emsp;&emsp;"desc": "描述",  
> &emsp;&emsp;&emsp;"type": "类型",  
> &emsp;&emsp;&emsp;"options": [
> 

*Response <font color="#AA5555">201</font>:*
> {  
> &emsp;"error_code": 0,  
> &emsp;"msg": "ok",  
> &emsp;"request": "POST&emsp;/forms"  
> }

### 获取用户创建的全部表单

*URL:*
> GET /form_templates

*Parameters:*
> (string) openid: 用户的openid

*Response <font color="#AA5555">200</font>:*
> {  
> &emsp;"error_code": 0,  
> &emsp;"msg": "ok",  
> &emsp;"request": "GET&emsp;/forms"  
> }