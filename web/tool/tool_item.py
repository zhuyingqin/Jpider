import random
import sys
from lxml import etree
import requests
import jsonpath
import re
from web.models import Jpider_memory

class Tool:
    """
    1.cookies转换
    2.UA随机获取
    3.代理IP获取（代理IP的验证以及自动更新）
    4.post格式整理
    """
    def __init__(self, cookies="", data=""):
        self.cookies = cookies
        self.data = data
        with open('/Users/zhuyingqin/small_pig/Jpider/web/tool/UA.txt', 'r') as f:
            # 打开UA.txt随机选取一个User—Agent
            self.user_agents = f.readlines()
        with open("/Users/zhuyingqin/small_pig/Jpider/web/tool/IP.txt", 'r') as f:
            # 打开IP.txt随机选取一个代理IP值
            self.ip = f.readlines()

    def string_dict(self):
        """
        将浏览器中复制的cookies转化成字典
        """
        item_dict = {}
        items = self.cookies.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            item_dict[key] = value
        return item_dict

    def get_user_agent(self):
        """
        随机获取UA
        """
        user_agent = random.choice(self.user_agents).strip()  
        return user_agent                          # 返回一个User—Agent

    def get_ip(self):
        """
        随机获取代理IP
        """     
        ip = random.choice(self.ip).strip()        # 随机获取代理IP
        proxies = {}
        if ip.split(':')[0] == "http":             # 判断HTTP/HTTPS
            proxies['http'] = "http://"+ip.split("//")[1]
        else:
            proxies['https'] = "http://"+ip.split("//")[1]
        return proxies                             # 返回一个代理IP

    def get_data(self):
        """
        first:true,pn:+(0-226-25),kd:python
        输入格式:first:true,pn:1,kd:python
        输出格式:{'first':true,'pn':1,'kd':'python'}
        Post 格式规整
        """
        data = self.data.split(',')
        dict_item = {}
        for item in data:
            items = item.split(':')
            key = str(items[0])
            value = str(items[1])
            dict_item[key] = value
        return dict_item 


class requests_tool:
    """
    
    """
    def __init__(self,request_way="get",url="",headers={},data={},
                      cookies={}):
        """
        此处的url为第一次需要访问的值
        """
        self.request_way = request_way      # Requests post/get方式
        self.url = url                      # url给大家一起用
        self.headers = headers              # Requests 的 headers
        self.data = data                    # post/get 传值
        self.cookies = cookies              # cookies的值
    
    def requests_html(self,url=""):
        """
        选择请求方式,GET/POST方式
        并传入url的值(可根据情况而改变)
        返回:获取到网页的HTML值
        """
        # headers = {}
        # proxies = Tool().get_ip()                     # 获取代理IP
        if self.request_way == "get":                   # 选择方式
            html = requests.get(url,headers=self.headers,data=self.data,
                                    cookies=self.cookies)   
            html.encoding = "utf-8"                     # 设置编码格式
            html = html.text                            # 返回text 
            # get的方式
        else:
            html = requests.post(url,headers=self.headers,data=self.data,
                                    cookies=self.cookies)  
            # post方式
            # html.encoding = "utf-8"                     # 设置编码格式
            # html = html.json()                          # 返回json
        return html

    def page_turning(self):
        # url{}+(0,226,25) {}中添加数值【0为初始量,226为最终量,25为每次增加的量】
        # 根据增量获取所有的URL
        urls = []                                       # 需要爬取的所有URL
        url_add = re.findall('\((.*?)\)',self.url)      # 正则提取url括号中的值(用于翻页等)["0,226,25"]
        url_add = url_add[0].split(',')                 # [0,226,25]                 
        for i in range(int(url_add[0]),int(url_add[1]),int(url_add[2])):
            url= self.url.split('+')[0].format(i)       # 往{}中添加数值
            urls.append(url)                            # 将url存入到list中
        return urls   

    def data_turning(self):
        # {'first':true,'pn':+(0-226-25),'kd':'python'}
        # 传入数据翻页
        key_find = ""
        value_find = ""
        for key,value in self.data.items():             # 遍历字典中的key、value
            if re.findall('\((.*?)\)', value):          # 正则提取url括号中的值(用于翻页等)["0,226,25"]
                key_find = key
                value_find = value

        return [key_find,value_find]


class Web_Xpath:
    """
    """
    def __init__(self,infos,x_info,add_infos=[]):
        self.infos = infos                              # 基本位置
        self.x_info = x_info                            # 核心字段
        self.add_infos = add_infos                      # 拓展字段列表
    
    def html_xpath(self,html=""):
        """
        1.多网页爬取
        2.xpath提取网页信息
        """
        need_infos = []                                             # 存储需要信息的列表存储示例:[[],[],[]]
        selector = etree.HTML(html)                                 # xpath解析呗
        get_infos = selector.xpath(self.infos)                      # xpath方式提取有用信息
        for info in get_infos:                              
            # book_name = info.xpath(self.x_info)[0]
            need_info = []                                          # 
            if self.x_info:                                         # 接收到表单值
                x_info = info.xpath(self.x_info)[0]                 # xpath获取基本位置
                need_info.append(x_info)                            # 数据存储
                Jpider_memory.objects.get_or_create(title=x_info)   # 数据库存储
                obj = Jpider_memory.objects.get(title=x_info)       # models title标签创立
            
            if self.add_infos[0]:
                info_zero = info.xpath(self.add_infos[0])[0]        # Xpath获取核心字段
                need_info.append(info_zero)                         
                obj.content = info_zero                             # 存入数据库字段

            if self.add_infos[1]:
                info_one = info.xpath(self.add_infos[1])[0]         # Xpath获取拓展字段1
                need_info.append(info_one)
                obj.extfield1 = info_one

            if self.add_infos[2]:
                info_two = info.xpath(self.add_infos[2])[0]         # Xpath获取拓展字段2
                need_info.append(info_two)
                obj.extfield2 = info_two

            if self.add_infos[3]:   
                info_three = info.xpath(self.add_infos[3])[0]       # Xpath获取拓展字段3
                need_info.append(info_three)
                obj.extfield3 = info_three

            if self.add_infos[4]:
                info_four = info.xpath(self.add_infos[4])[0]        # Xpath获取拓展字段4
                need_info.append(info_four)
                obj.extfield4 = info_four

            if self.add_infos[5]:
                info_five = info.xpath(self.add_infos[5])[0]        # Xpath获取拓展字段5
                need_info.append(info_five)
                obj.extfield5 = info_five

            if self.add_infos[6]:
                info_six = info.xpath(self.add_infos[6])[0]         # Xpath获取拓展字段6
                need_info.append(info_six)
                obj.extfield6 = info_six
                
            if self.add_infos[7]:
                info_seven = info.xpath(self.add_infos[7])[0]       # Xpath获取拓展字段7
                need_info.append(info_seven)
                obj.extfield7 = info_seven
                
            if self.add_infos[8]:
                info_eight = info.xpath(self.add_infos[8])[0]       # Xpath获取拓展字段8
                need_info.append(info_eight)
                obj.extfield8 = info_eight
                
            if self.add_infos[9]:
                info_nine = info.xpath(self.add_infos[9])[0]        # Xpath获取拓展字段9
                need_info.append(info_nine)
                obj.extfield9 = info_nine
            need_infos.append(need_info)
            obj.save()
            # Jpider_memory.objects.get_or_create(title=x_info,content=info_zero,extfield1=info_one)  
        return need_infos
        # urls = 

    def json_get(self,result=""):
        """
        json数据的处理
        """
        result.encoding = 'utf-8'
        result = result.json()
        need_infos = []
        get_infos = jsonpath.jsonpath(result, self.infos)[0]
        # print(get_infos)
        for info in get_infos:
            need_info = []
            if self.x_info:
                need_info.append(info[self.x_info])
                print(need_info)
            if self.add_infos[0]:
                need_info.append(info[self.add_infos[0]])
            if self.add_infos[1]:
                need_info.append(info[self.add_infos[1]])
            if self.add_infos[2]:
                need_info.append(info[self.add_infos[2]])
            if self.add_infos[3]:
                need_info.append(info[self.add_infos[3]])
            if self.add_infos[4]:
                need_info.append(info[self.add_infos[4]])
            if self.add_infos[5]:
                need_info.append(info[self.add_infos[5]])
            if self.add_infos[6]:
                need_info.append(info[self.add_infos[6]])
            if self.add_infos[7]:
                need_info.append(info[self.add_infos[7]])
            if self.add_infos[8]:
                need_info.append(info[self.add_infos[8]])
            if self.add_infos[9]:
                need_info.append(info[self.add_infos[9]])
            need_infos.append(need_info)
        return need_infos
        
