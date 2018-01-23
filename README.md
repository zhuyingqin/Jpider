## Jpder
功能：主要用于网站信息的简单爬取入库可视化等功能
作者：朱应钦

### 前期准备
Django
Requests
Jsonpath
lxml

### 使用说明
进入首页输入提示信息，URL和post/get不可为空，其余均可为空。
User—Agent自动生成
#### URL翻页
```
url{}+(0,226,25) {}中添加数值【0为初始量,226为最终量,25为每次增加的量】
例如豆瓣图书的爬取
url = https://book.douban.com/top250?start={}+(0,226,25)
```
#### post/get
输入post or get即可
#### Referer
```
例如：拉勾网的爬取
https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=
```
#### Data翻页
```
例如：拉勾网的爬取
{'first':true,'pn':+(0-226-25),'kd':'python'}
(0-226-25)【0为初始量,226为最终量,25为每次增加的量】
```
#### cookies
同Referer，浏览器截取即可
#### 进入xpath阶段
点击提交后，进入信息获取界面，
基础源码的生成方便用于调试阶段
若传入html值，输入xpath值则可
```
豆瓣网站爬取案例
URL = https://book.douban.com/top250?start={}+(0,226,25)
Post／Get = get
点击提交
基本位置：//tr[@class="item"]
核心字段：td/div/a/@title
拓展字段0:td/div/a/@href
拓展字段1:td/p/text()

```
若传入json值，输入jsonpath则可
```
拉勾网站爬取案例
URL：https://www.lagou.com/jobs/positionAjax.json?city=%E6%88%90%E9%83%BD&needAddtionalResult=false&isSchoolJob=0
Post／Get = post
Referer = https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=
data = first:true,pn:+(1-5-1),kd:python
点击提交
基本位置：$..result
核心字段：companyShortName
拓展字段：positionId
```
