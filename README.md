# EE-Book

[中文](./README.md) | [English](./README_en.md)   

[EE-Book](https://github.com/knarfeh/EE-Book) 是一个命令行程序，它可以从网络上爬取内容制作成EPub格式电子书。  

[网页版](http://ee-book.org)

## 支持的网站 (正在更新中!)  

| 名称 | 主页                               | 支持类型                          |
| :------ | ---------------------------------------- | ---------------------------------------- |
| 知乎      | [www.zhihu.com](http://www.zhihu.com)    | **问题：** `zhihu.com/question/{question_id}`<br/>**答案：** `zhihu.com/question/{question_id}/answer/{answer_id}`<br/>**话题：** `zhihu.com/topic/{topic_id}`<br/>**用户的全部回答：** `zhihu.com/people/{people_id}` or `zhihu.com/people/{people_id}/answers`<br/>**收藏夹：** `zhihu.com/collection/{collection_id}` <br/> **专栏：** `zhuanlan.zhihu.com/{zhuanlan_id}` |
| 简书      | [www.jianshu.com](http://www.jianshu.com) | **用户的所有文章：** `jianshu.com/users/{people_id}/latest_articles`<br/>**专题：** `jianshu.com/collection/{collection_id}`<br/>**文集：** `jianshu.com/notebooks/{notebooks_id}/latest` or `jianshu.com/notebooks/{notebooks_id}/top` |
| csdn博客  | [blog.csdn.net](http://blog.csdn.net)    | **用户的所有文章：** `blog.sina.com.cn/u/{people_id}` |
| 新浪博客   | [blog.sina.com.cn](http://blog.sina.com.cn/) | **用户的所有文章：** `blog.csdn.net/{people_id}` |
| 博客园     | [www.cnblogs.com/](http://www.cnblogs.com/) | **用户的所有文章：** `cnblogs.com/{people_id}/`  |
| 易百教程   | [www.yiibai.com](http://www.yiibai.com/) | **某个教程的文章：** `yiibai.com/{tutorial_kind}`|
| Talk Python To Me | [www.talkpython.fm](https://www.talkpython.fm)| **[「Talk Python To Me」](https://www.talkpython.fm)的文稿:** `https://talkpython.fm/episodes/all/`|

## 用法

获得帮助信息:  

```bash
$ python ee-book -h
```

举个例子:  

```bash
$ python ee-book -u jianshu.com/users/b1dd2b2c87a8/latest_articles
```

稍等片刻, 你就可以得到电子书了:  

![directory](http://7xi5vu.com1.z0.glb.clouddn.com/2016-03-09directory.png)  

![scheme](http://7xi5vu.com1.z0.glb.clouddn.com/2016-03-09Scheme.png)


## 贡献代码
...当然欢迎

### 解决依赖

 * [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/)
 * [lxml](http://lxml.de/)
 * ~ [PyQt4](https://www.riverbankcomputing.com/software/pyqt/download) ~

### 搭建 EE-Book 的开发环境


```bash
$ pip install -r requirements.txt
```

[安装 pyqt4](https://riverbankcomputing.com/software/pyqt/download/)


### [TODO List](./notes/TODOlist.md)

## 相关信息

* 之前版本的 [README](https://github.com/knarfeh/EE-Book/blob/c4d870ff8cca6bbac97f04c9da727397cee8d519/README.md)

* 发在[v2ex](https://v2ex.com/)的一篇[文章](http://knarfeh.github.io/2016/03/17/EE-Book/)

## 感谢

* [知乎助手](https://github.com/YaoZeyuan/ZhihuHelp)
* [calibre](https://github.com/kovidgoyal/calibre)
* [you-get](https://github.com/soimort/you-get)

## License

[MIT license](./LICENSE).

