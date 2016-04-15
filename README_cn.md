# EE-Book

[中文](./README_cn.md) | [English](./README.md)   

[EE-Book](https://github.com/knarfeh/EE-Book) 是一个命令行程序，它可以从网络上爬取内容制作成EPub格式电子书。图形界面正在开发中。  

## 支持的网站 (正在更新中!)  

* [https://www.zhihu.com/](https://www.zhihu.com/)
* [https://www.jianshu.com/](https://www.jianshu.com/)
* [http://blog.sina.com.cn/](http://blog.sina.com.cn/)
* [http://blog.csdn.net/](http://blog.csdn.net/)

## 用法

获得帮助信息:  

```shell
./ee-book -h
```

举个例子:  

```shell
./ee-book -u http://www.jianshu.com/users/b1dd2b2c87a8/latest_articles
```

稍等片刻, 你就可以得到电子书了:  

![yinwang](http://7xi5vu.com1.z0.glb.clouddn.com/2016-03-09jianshu_yinwang.png)


## 贡献代码
...当然欢迎!

### 解决依赖

 * [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/)
 * [lxml](http://lxml.de/)
 * [PyQt4](https://www.riverbankcomputing.com/software/pyqt/download)

### 建立 EE-Book 的开发环境

```shell
$ sudo pip install -r requirements.txt
```

[安装 pyqt4](https://riverbankcomputing.com/software/pyqt/download/)


### [TODO List](./doc/TODOlist.md)

## 相关信息

* 之前版本的 [README](https://github.com/knarfeh/EE-Book/blob/c4d870ff8cca6bbac97f04c9da727397cee8d519/README.md)

* 发在[v2ex](https://v2ex.com/)的一篇[文章](http://knarfeh.github.io/2016/03/17/EE-Book/)

## 软件版权许可证

EE-Book 遵循 [MIT license](./LICENSE).

