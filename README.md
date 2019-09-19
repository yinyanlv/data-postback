# data-postback
data postback

## 环境要求
```
1、python3+
2、数据库相关驱动
    // mac osx
    brew install unixodbc [issue](https://github.com/mkleehammer/pyodbc/issues/87)
    安装oracle client library [教程+下载链接](https://oracle.github.io/odpi/doc/installation.html#macos)
```

## 启动步骤
```
1、pip install -r requirements.txt
2、linux: export APP_MODE={dev|test|prod}, windows: SET APP_MODE={dev|test|prod}
3、python __main__.py 或 python .
```