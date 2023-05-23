# 中关村在线 手机信息爬取

使用Django, Scrapy

## 项目配置

```bash
pip install -r requirements.txt
```

更改`zol_phone.settings`中的数据库及对象存储配置

更改`apps.crawler.setting`中的爬虫配置
如果不想用对象存储, 可以将`IMAGES_STORE`更改为本地路径