# 中关村在线 手机信息爬取

使用Django, Scrapy

前端页面使用 [欲饮琵琶码上催/bootstrap-admin](https://gitee.com/ajiho/bootstrap-admin.git) 模板

## 项目配置

```bash
pip install -r requirements.txt
```

更改`zol_phone.settings`中的数据库及对象存储配置

更改`apps.crawler.setting`中的爬虫配置
如果不想用对象存储, 可以将`IMAGES_STORE`更改为本地路径

## 总结

### 报错 Refused to display 'http://127.0.0.1:8000/ in a frame because it set 'X-Frame-Option

将某个页面放到框架中报错,

### Django Scrapy apps.*.models 兼容问题

https://www.cnblogs.com/lewangchen/p/15049778.html

删除apps.your_app.apps.py中的内容, 使用项目根路径方式导入, INSTALLED_APPS中添加apps.your_app


**处理方法：**

1. 注释掉上面中间件，但是这样不好，容易出现中间人攻击。
   最好的方法：

```python
MIDDLEWARE = [
    ...,
    # 注释掉这一行
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

2. 在view中添加装饰器

```python
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt


@xframe_options_exempt
def add_staff(request):
    return render(request, 'login/admin-list.html')


class SpiderView(View):
    @xframe_options_exempt
    def get(self, request):
        return render(request, 'spiders_list.html')

```

3. 在setting中设置：

X_FRAME_OPTIONS = 'SAMEORIGIN'

> X-Frame-Options 有三个值:
> DENY ：表示该页面不允许在 frame 中展示，即便是在相同域名的页面中嵌套也不允许
> SAMEORIGIN ：表示该页面可以在相同域名页面的 frame 中展示
> ALLOW-FROM uri ：表示该页面可以在指定来源的 frame 中展示
> 换一句话说，如果设置为 DENY，不光在别人的网站 frame 嵌入时会无法加载，在同域名页面中同样会无法加载。
> 另一方面，如果设置为 SAMEORIGIN，那么页面就可以在同域名页面的 frame 中嵌套。