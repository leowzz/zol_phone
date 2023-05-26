# Scrapy 项目目录

## 0. 安装

```bash
pip install scrapyd

pip install scrapyd-client
```

## 1. 使用

在项目目录下启动 scrapyd, 默认监听 6800 端口

```bash
scrapyd
```

编辑 `scrapy.cfg` 文件，

- 修改 `url` 为 scrapyd 服务的地址
- 修改 [deploy:<部署名称>]
- 修改 project 为项目名称

```bash
[deploy:vm1]
url = http://localhost:6800/
project = phone_crawler
```

发布项目

```bash
# scrapyd-deploy <部署名称> -p <项目名称>
scrapyd-deploy vm1 -p phone_crawler
```

编辑 setup.py 文件，修改版本号和设置路径

```python
setup(
    name='phone_crawler',
    version='1.0.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = phone_crawler.settings']},
)
```

Scrapy pipelines 中使用 Django ORM 存储数据

参考:

Scrapy pipelines 中使用 Django ORM 存储数据

参考: https://blog.csdn.net/weixin_35757704/article/details/78922114

## 2. Scrapyd 的功能

Scrapyd 提供了一系列 HTTP 接口来实现各种操作，在这里我们可以将接口的功能梳理一下，以 Scrapyd 所在的 IP 为 12 为例进行讲解。

### 2.1 daemonstatus.json

这个接口负责查看 Scrapyd 当前服务和任务的状态，我们可以用 curl 命令来请求这个接口，命令如下：

```python
curl http://127.0.0.1:6800/daemonstatus.json 
1
```

这样我们就会得到如下结果：

```python
{"status": "ok", "finished": 90, "running": 9, "node_name": "datacrawl-vm", "pending": 0} 
1
```

返回结果是 Json 字符串，status 是当前运行状态， finished 代表当前已经完成的 Scrapy 任务，running 代表正在运行的 Scrapy 任务，pending 代表等待被调度的 Scrapyd 任务，node_name 就是主机的名称。

### 2.2 addversion.json

这个接口主要是用来部署 Scrapy 项目，在部署的时候我们需要首先将项目打包成 Egg 文件，然后传入项目名称和部署版本。

我们可以用如下的方式实现项目部署：

```python
curl http://127.0.0.1:6800/addversion.json -F project=wenbo -F version=first -F egg=@weibo.egg 
1
```

在这里 -F 即代表添加一个参数，同时我们还需要将项目打包成 Egg 文件放到本地。
这样发出请求之后我们可以得到如下结果：

```python
{"status": "ok", "spiders": 3} 
1
```

这个结果表明部署成功，并且其中包含的 Spider 的数量为 3。此方法部署可能比较烦琐，在后面我会介绍更方便的工具来实现项目的部署。

### 2.3 schedule.json

这个接口负责调度已部署好的 Scrapy 项目运行。我们可以通过如下接口实现任务调度：

```python
curl http://127.0.0.1:6800/schedule.json -d project=phone_crawler -d spider=PhoneBrandSpider 
1
```

在这里需要传入两个参数，project 即 Scrapy 项目名称，spider 即 Spider 名称。返回结果如下：

```python
{"status": "ok", "jobid": "6487ec79947edab326d6db28a2d86511e8247444"} 
1
```

status 代表 Scrapy 项目启动情况，jobid 代表当前正在运行的爬取任务代号。

### 2.4 cancel.json

这个接口可以用来取消某个爬取任务，如果这个任务是 pending 状态，那么它将会被移除，如果这个任务是 running 状态，那么它将会被终止。

我们可以用下面的命令来取消任务的运行：

```python
curl http://127.0.0.1:6800/cancel.json -d project=weibo -d job=6487ec79947edab326d6db28a2d86511e8247444 
1
```

在这里需要传入两个参数，project 即项目名称，job 即爬取任务代号。返回结果如下：

```python
{"status": "ok", "prevstate": "running"} 
1
```

status 代表请求执行情况，prevstate 代表之前的运行状态。

### 2.5 listprojects.json

这个接口用来列出部署到 Scrapyd 服务上的所有项目描述。我们可以用下面的命令来获取 Scrapyd 服务器上的所有项目描述：

```python
curl http://127.0.0.1:6800/listprojects.json 
1
```

这里不需要传入任何参数。返回结果如下：

```python
{"status": "ok", "projects": ["weibo", "zhihu"]} 
1
```

status 代表请求执行情况，projects 是项目名称列表。

### 2.6 listversions.json

这个接口用来获取某个项目的所有版本号，版本号是按序排列的，最后一个条目是最新的版本号。

我们可以用如下命令来获取项目的版本号：

```python
curl http://127.0.0.1:6800/listversions.json?project=weibo 
1
```

在这里需要一个参数 project，就是项目的名称。返回结果如下：

```python
{"status": "ok", "versions": ["v1", "v2"]} 
1
```

status 代表请求执行情况，versions 是版本号列表。

### 2.7 listspiders.json

这个接口用来获取某个项目最新的一个版本的所有 Spider 名称。我们可以用如下命令来获取项目的 Spider 名称：

```python
curl http://127.0.0.1:6800/listspiders.json?project=weibo 
1
```

在这里需要一个参数 project，就是项目的名称。返回结果如下：

```python
{"status": "ok", "spiders": ["weibocn"]} 
1
```

status 代表请求执行情况，spiders 是 Spider 名称列表。

### 2.8 listjobs.json

这个接口用来获取某个项目当前运行的所有任务详情。我们可以用如下命令来获取所有任务详情：

```python
curl http://127.0.0.1:6800/listjobs.json?project=weibo 
1
```

在这里需要一个参数 project，就是项目的名称。返回结果如下：

```python
{"status": "ok", 
 "pending": [{"id": "78391cc0fcaf11e1b0090800272a6d06", "spider": "weibocn"}], 
 "running": [{"id": "422e608f9f28cef127b3d5ef93fe9399", "spider": "weibocn", "start_time": "2017-07-12 10:14:03.594664"}], 
 "finished": [{"id": "2f16646cfcaf11e1b0090800272a6d06", "spider": "weibocn", "start_time": "2017-07-12 10:14:03.594664", "end_time": "2017-07-12 10:24:03.594664"}]} 
1234
```

status 代表请求执行情况，pendings 代表当前正在等待的任务，running 代表当前正在运行的任务，finished 代表已经完成的任务。

### 2.9 delversion.json

这个接口用来删除项目的某个版本。我们可以用如下命令来删除项目版本：

```python
curl http://127.0.0.1:6800/delversion.json -d project=weibo -d version=v1 
1
```

在这里需要一个参数 project，就是项目的名称，还需要一个参数 version，就是项目的版本。返回结果如下：

```python
{"status": "ok"} 
1
```

status 代表请求执行情况，这样就代表删除成功了。

### 2.10 delproject.json

这个接口用来删除某个项目。我们可以用如下命令来删除某个项目：

```python
curl http://127.0.0.1:6800/delproject.json -d project=weibo 
1
```

在这里需要一个参数 project，就是项目的名称。返回结果如下：

```python
{"status": "ok"} 
1
```

status 代表请求执行情况，这样就代表删除成功了。
以上就是 Scrapyd 所有的接口，我们可以直接请求 HTTP 接口即可控制项目的部署、启动、运行等操作。
