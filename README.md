# EE-Book

[![Join the chat at https://gitter.im/knarfeh/EE-Book](https://badges.gitter.im/knarfeh/EE-Book.svg)](https://gitter.im/knarfeh/EE-Book?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[中文](./README_cn.md) | [English](./README.md)

*Note*: Due to personal reason, there will be no big changes in the next two months, Only a few small patches.   --2016.04.19  

[EE-Book](https://github.com/knarfeh/EE-Book) is a command-line utility to downlaod text from the Web, and make it a e-book. GUI is under developing.

## Supported Sites (UPDATING!)

| website | home page                                | supported type                           |
| :------ | ---------------------------------------- | ---------------------------------------- |
| 知乎      | [www.zhihu.com](http://www.zhihu.com)    | **问题：** `zhihu.com/question/{question_id}`<br/>**答案：** `zhihu.com/question/{question_id}/answer/{answer_id}`<br/>**话题：** `zhihu.com/topic/{topic_id}`<br/>**用户的全部回答：** `zhihu.com/people/{people_id}` or `zhihu.com/people/{people_id}/answers`<br/>**收藏夹：** `zhihu.com/collection/{collection_id}` <br/> **专栏：** `zhuanlan.zhihu.com/{zhuanlan_id}` |
| 简书      | [www.jianshu.com](http://www.jianshu.com) | **用户的所有文章：** `jianshu.com/users/{people_id}/latest_articles`<br/>**专题：** `jianshu.com/collection/{collection_id}`<br/>**文集：** `jianshu.com/notebooks/{notebooks_id}/latest` or `jianshu.com/notebooks/{notebooks_id}/top` |
| csdn博客  | [blog.csdn.net](http://blog.csdn.net)    | **用户的所有文章：** `blog.sina.com.cn/u/{people_id}` |
| 新浪博客   | [blog.sina.com.cn](http://blog.sina.com.cn/) | **用户的所有文章：** `blog.csdn.net/{people_id}` |
| 博客园     | [www.cnblogs.com/](http://www.cnblogs.com/) | **用户的所有文章：** `cnblogs.com/{people_id}/`  |
| 易百教程   | [www.yiibai.com](http://www.yiibai.com/) | **某个教程的文章：** `yiibai.com/{tutorial_kind}`|
| Talk Python To Me | [www.talkpython.fm](https://www.talkpython.fm)| **transcripts of [「Talk Python To Me」](https://www.talkpython.fm):** `https://talkpython.fm/episodes/all`|

## Usage

get help info:  

```console
$ python ee-book -h
```

for example:  

```console
$ python ee-book -u jianshu.com/users/b1dd2b2c87a8/latest_articles
```

after a while, you will get the e-book:   

![directory](http://7xi5vu.com1.z0.glb.clouddn.com/2016-03-09directory.png)  

![scheme](http://7xi5vu.com1.z0.glb.clouddn.com/2016-03-09Scheme.png)

## Contributing

...would be awesome! 

### requirements

 * [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/)
 * [lxml](http://lxml.de/)
 * [PyQt4](https://www.riverbankcomputing.com/software/pyqt/download)

### Setting up a development environment for EE-Book 

```Console
$ pip install -r requirements.txt
```

[install pyqt4](https://riverbankcomputing.com/software/pyqt/download/)


### [TODO List](./doc/TODOlist.md)

## Relevant Infomation

* previous [README](https://github.com/knarfeh/EE-Book/blob/c4d870ff8cca6bbac97f04c9da727397cee8d519/README.md)

* An [article](http://knarfeh.github.io/2016/03/17/EE-Book/) posted on [v2ex](https://v2ex.com/)

## Thanks

* [知乎助手](https://github.com/YaoZeyuan/ZhihuHelp)
* [calibre](https://github.com/kovidgoyal/calibre)
* [you-get](https://github.com/soimort/you-get)

## License

EE-Book is licensed under the terms of [MIT license](./LICENSE).