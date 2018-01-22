# 导入Django方法
from django.shortcuts import render
from django.http import HttpResponse          # 返回html值用于检查程序正确性
from django.http import HttpResponseRedirect  # 重定向
# 引入我创建的表单类
from .models import Jpider_response     # 用于存储首页表单的models
from .forms import UrlForm              # 首页表单
from .forms import XpathForm            # Xpath获取路径表单
# 调用自制工具包
import sys                              # 导入包的位置
sys.path.append('/Users/zhuyingqin/small_pig/Jpider/web/tool')
from tool_item import Tool              # data规整、User-Agent、cookies、IP
from tool_item import requests_tool     # 翻页URL、requests
from tool_item import Web_Xpath         # Xpath、
# 调用爬虫函数          
import re                               # 导入正则
import time                             # 时间函数


def index(request):
    headers = {}
    headers["User-Agent"] = Tool().get_user_agent()
    proxies = Tool().get_ip()                   # 获取代理IP
    
    if request.method == 'POST':                # 当提交表单时 
        
        form = UrlForm(request.POST)            # form 包含提交的数据
        
        if form.is_valid():                     # 如果提交的数据合法
            url = form.cleaned_data['url']                      # 获取爬取的URL
            request_way = form.cleaned_data['request_way']      # 获取GET/POST方式
            headers["Referer"] = form.cleaned_data['referer']   # 获取Referer传入headers
            data = form.cleaned_data['data']                    # 获取data的值
            cookies = form.cleaned_data['cookies']              # 获取cookies的值

        if cookies:                                             # 判断是否输入cookies
            cookies = Tool(cookies).string_dict()               # 将从浏览器复制的cookies序列化
        else:
            cookies = {}                                        # 若cookies无值则返回一个空字典(用于eval)
        if data:                                                # 判断是否输入data
            data=Tool(data = data).get_data()                   # 将输入的post格式化
        else:
            data = {}                                           # 若data无值则返回一个空字典(用于eval)
        
        # 将用户输入的需要爬取的参数保存models,用于生成对应的代码[属于models的改操作]
        Jpider_response.objects.all().update(url=url,headers=headers,data=data,cookies=cookies)
        # requests获取html写入tool_item.py中,适用于翻页网站需要多次请求的需求 
        # html = requests_tool(request_way,url=url,headers=headers,data=data,cookies=cookies).requests_html(url=url)

        return HttpResponseRedirect('pro/')     # 跳转至下一个页面
    else:                                       # 当正常访问时
        form = UrlForm()
    return render(request, 'index.html', {'form': form})


def program(request):
    html = Jpider_response.objects.get(pk=1)    # 从models提取数据
    url = html.url
    headers = eval(html.headers)                # 将headers数据变成字典
    data = eval(html.data)                      # 将data数据变成字典
    cookies = eval(html.cookies)                # 将cookies数据变成字典
    if request.method == 'POST':                # 当提交表单时
        form = XpathForm(request.POST)          # form 包含提交的数据 
        if form.is_valid():                     # 如果提交的数据合法
            infos = form.cleaned_data['infos']                      # 基本位置
            info = form.cleaned_data['info']                        # 核心字段
            info_zero = form.cleaned_data['info_zero']              # 拓展字段0-9
            info_one = form.cleaned_data['info_one']                 
            info_two = form.cleaned_data['info_two']
            info_three = form.cleaned_data['info_three']
            info_four = form.cleaned_data['info_four']
            info_five = form.cleaned_data['info_five']
            info_six = form.cleaned_data['info_six']
            info_seven = form.cleaned_data['info_seven']
            info_eight = form.cleaned_data['info_eight']
            info_nine = form.cleaned_data['info_nine']
            add_infos = [info_zero,info_one,info_two,info_three,info_four
                        ,info_five,info_six,info_seven,info_eight,info_nine]    # 拓展字段合集
            # print(add_infos)
        # 网页翻页值传入
        if re.findall('\((.*?)\)',html.url):                         # 判断括号内是否有值
            urls = requests_tool(url=html.url).page_turning()        # 获取需要爬取的URL值
            html_xpath_value = []
            for url in urls:
                html_value = requests_tool(headers=headers,data=data,cookies=cookies).requests_html(url)    # 获取到html
                html_xpath = Web_Xpath(infos=infos,x_info=info,add_infos=add_infos).html_xpath(html_value)                # xpath提取
                # 写入库然后提取出来使用（后续加入）
                html_xpath_value += html_xpath                       # list合并的方法(需修改)
            return render(request, 'xpath.html', {'html_xpath': html_xpath_value,'html':html})
        # Data翻页值传入
        data_turning = requests_tool(data=data).data_turning()       # data翻页[key_find, value_find]
        
        if data_turning[0]:                                          # 判断是否有翻页值传入
            data_add = re.findall('\((.*?)\)', data_turning[1])      # 正则提取url括号中的值(用于翻页等)["0,226,25"]
            data_add = data_add[0].split('-')                        # 示例:[0,226,25]
            json_xpath_value = []
            for i in range(int(data_add[0]), int(data_add[1]), int(data_add[2])):  
                data[data_turning[0]] = str(i)                       # data_turning[0] key_find(翻页参数的key值)
                html = requests_tool(request_way='post',headers=headers,data=data,cookies=cookies).requests_html(url=url)
                html_json_xpath = Web_Xpath(infos=infos,x_info=info,add_infos=add_infos).json_get(html)
                json_xpath_value += html_json_xpath
                time.sleep(0.2)
            return render(request, 'xpath.html', {'html_xpath': json_xpath_value,'html':html})

        html = requests_tool(request_way='get',headers=eval(html.headers),data=eval(html.data),cookies=eval(html.cookies)).requests_html(url=html.url)
        return HttpResponse(html)
    else:# 当正常访问时
        form = XpathForm()
    return render(request, 'xpath.html', {'form': form,'html': html})


        