# MobikeAgent
摩拜单车(Mobike)扫描器，自动搜集全国可用的单车。支持输出CSV和KML。

![Google Earth中可视化收集到的KML](https://github.com/yrjyrj123/image/raw/master/mobike_agent_demo.gif)

白色底色为Lite版单车，红色底色为老版摩拜单车，红包为红包车，你懂的。

## 依赖安装
	pip install -r requirements.txt

## 基本使用

### 第一步(可选)：
之前摩拜单车服务器对请求频率作出限制，必须使用代理服务器，躲避IP限制。不过似乎近期服务器在切换为OpenResty后不再限制请求频率。我搜集了几w个开放代理，存放在**proxies.txt**中，开放代理并不能保证一直有效，需要使用**check_proxy.py**筛选出可用的代理。服务器已经全面切换为HTTPS，能支持HTTPS的代理不多。

	python check_proxy.py
	
生成的**good_proxies.txt**中存放可用的代理服务器

### 第二步：
使用**mobike.py**开始爬取数据，默认会使用**good_proxies.txt**中的代理，如果不需要使用代理，只要删掉**good_proxies.txt**，或者删除这个文件中的所有内容。
	
	python mobike.py
	
## 高级用法
**mobike.py**中提供**get\_bikes\_in\_range**函数可供外部调用，默认输出格式为CSV(车辆编号,类型,经度,纬度)，也可以使用**kml\_path**参数生成KML文件

	import mobike
	
	mobike.get_bikes_in_range(116, 116.8, 39.6, 40.3, csv_path="beijing.csv")  #北京六环以内的区域,可以涵盖95%以上的车
	
    mobike.get_bikes_in_range(115.7, 117.4, 39.4, 41.6, csv_path="beijing_all.csv")  #地理书上的整个北京辖区,大约是六环内的7倍面积	
    
    mobike.get_bikes_in_range(116, 116.8, 39.6, 40.3, kml_path="out.kml")   #输出KML文件，用于在Google Earth等工具中可视化
    
## 数据样例
**/data**目录下为2017年4月采集的北京地区数据，摩拜单车在北京已经投放了超过37w辆，文件很大，压缩了一下。注意：摩拜单车返回的是火星坐标。最新的爬虫已经会自动转换成WGS84了，但是这个文件夹里的数据目前还是使用火星坐标，爬一次还是挺费时间的，以后会统一成WGS84。

## TODO：
* 增加命令行功能，把这个脚本变成一个命令行工具

## PS:
虽然优化了扫描的算法，但是爬取一次全北京的单车还是需要9w+次请求，耗时40分钟左右，请不要在高峰期运行，以免给摩拜单车的服务器造成压力。