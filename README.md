# MobikeAgent
摩拜单车(Mobike)扫描器，自动搜集全北京、上海所有可用的单车。支持输出CSV和KML。

![Google Earth中可视化收集到的KML](https://github.com/yrjyrj123/image/raw/master/mobike_agent_demo.gif)

白色底色为新增的Lite版单车，红色底色为老版摩拜单车。

##依赖安装
	pip install -r requirements.txt

##基本使用

###第一步：
由于摩拜单车服务器对请求频率作出限制，必须使用代理服务器，躲避IP限制。我搜集了近1w个开放代理，存放在**proxies.txt**中，不过开放代理并不能保证一直有效，需要使用**check_proxy.py**筛选出可用的代理。

	python check_proxy.py
	
生成的**good_proxies.txt**中存放可用的代理服务器

###第二步：
使用**mobike.py**开始爬取数据，默认使用**good_proxies.txt**中的代理
	
	python mobike.py
	
##高级用法
**mobike.py**中提供**get\_bikes\_in\_range**函数可供外部调用，默认输出格式为csv(车辆编号,经度,纬度)，也可以使用**kml\_path**参数生成KML文件

	import mobike
	
	mobike.get_bikes_in_range(116, 116.8, 39.6, 40.3)  #北京六环以内的区域,3186块,可以涵盖95%以上的车
	
    mobike.get_bikes_in_range(115.7, 117.4, 39.4, 41.6)  #地理书上的整个北京辖区,20976块,大约是六环内的7倍面积	
    
    mobike.get_bikes_in_range(116, 116.8, 39.6, 40.3, kml_path="out.kml")   #输出KML文件，用于在Google Earth等工具中可视化
    
##数据样例：
**/data**目录下为2016年10月22日中午采集的数据。分为北京和上海的CSV和KML文件，共4个，约4w辆单车，供参考。

##TODO：
* 增加命令行功能，把这个脚本变成一个命令行工具