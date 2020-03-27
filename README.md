### 获取数据
疫情数据目前在网上已经有很多网站都在通报，比如丁香园、百度、今日头条等，但是这些数据都有一个缺陷就是仅展示当天的数据，如果我们想要获取一段时间的数据，那么就得长时间爬取，并存储数据，而且之前的数据还获取不到。这个时候我就想到了世界上最大的同性交友-GitHub。

![](https://upload-images.jianshu.io/upload_images/9101119-10c7fa52034d6adc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这里的数据来源于丁香园，而且爬取的比较早。之前作者是提供了获取所有数据的API，但是可能随着数据量的增大，网站压力太大，因此取消了获取全部数据的接口，但是数据上传到另一个项目中，我们只要下载就可以直接使用。

![](https://upload-images.jianshu.io/upload_images/9101119-b483d3c72477e283.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

数据内容如下：

![](https://upload-images.jianshu.io/upload_images/9101119-e8270a4375feee89.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

因为数据每个小时会获取并同步一次，所以这个里面同一天会有很多数据，而且部分地区并不是每天都有数据，可能存在某些天是没有数据的，我们必须对数据进行清洗处理，才能正常使用。

### 数据清洗
```python
import time
from datetime import date, timedelta, datetime
import pandas as pd
from collections import defaultdict

df = pd.read_json('data/DXYArea-TimeSeries.json')
df.head()
```
![](https://upload-images.jianshu.io/upload_images/9101119-57c0cfea97caf469.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


数据读取以后，存在以下几个问题：
1. 时间数据是统计的时间戳，需要转换为时间对象
2. 每日有多次条数据记录，我们只需要记录一次就行了
3. 数据是按照省份统计的，我们需要按国家进行统计
- 转换时间戳为时间对象
```python
df['updateTime'] = df['updateTime'].apply(lambda item: time.strftime('%Y-%m-%d', time.localtime(item // 1000)))
df.head()
```
![](https://upload-images.jianshu.io/upload_images/9101119-7c646224005c924c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 按照省份和时间去重，保证每个地区每天只有一条记录
```python
df.drop_duplicates(subset=['provinceShortName', 'updateTime'])
```

- 按国家统计
将一个国家的所有省份每天的数据加起来
```python
# 按省份分组
for province_name, items in self.df.groupby(by=['provinceName']):
    ......
    # 然后再按时间分组
    for update_time, item in items.groupby(by=['updateTime']):
        ....
```
数据清洗完以后，保存到csv文件中，格式如下：
![](https://upload-images.jianshu.io/upload_images/9101119-18d790cb572732ad.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 制作动图
动态图的制作，我们在GitHub上找到一个[开源的项目](https://github.com/Jannchie/Historical-ranking-data-visualization-based-on-d3.js)，根据配置修改对应的项，打开网页加载我们生成的csv文件

![](https://upload-images.jianshu.io/upload_images/9101119-f8034eea5e91e1dd.gif?imageMogr2/auto-orient/strip)