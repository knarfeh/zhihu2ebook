# EE-Book
===

## 简介
===
### 缘起
在知乎「发现(大V们)更大的世界」的过程中，我发现了一个开源项目[ZhihuHelp](https://github.com/YaoZeyuan/ZhihuHelp)，刚好初学Python，于是跟着慢慢地学习，写了一些简单爬虫，写正则表达式，学BS库，学EPub格式电子书的组织结构，给知乎助手这个项目提Issues，pull requests，后来根据自己的需要写了简书的版本，能够把某个博主的所有博文做成电子书，如，把王垠的所有博客做成EPub格式的电子书：
![wangyin](http://7xi5vu.com1.z0.glb.clouddn.com/2016-03-09-jianshu_epub_wangyin.png?imageView/2/w/800/q/90)
地址是：[jianshu2e-book](https://github.com/knarfeh/jianshu2e-book)

再后来，我又写了新浪博客的版本，把韩寒的博客做成EPub格式的电子书：
![hanhanblog](http://7xi5vu.com1.z0.glb.clouddn.com/2016-02-02-SinaBloghanhanepub.png?imageView/2/w/800/q/90)

地址是：[SinaBlog2e-book](https://github.com/knarfeh/SinaBlog2e-book)

我是Kindle重度用户，这几个程序的功能对我很有帮助，用着用着，有一天我突然想到，其实这样的需求还真不少，我应该把这个程序变成一个框架，把需要爬取的网站作为一个个模块放在里面，于是便有了[EE-Book]()   TODO: 加入github的网址

### 所以，EE-Book是什么？
简单来说，EE-Book能够让你把特定网站的特定内容爬取下来做成EPub格式的电子书。它是桌面程序，用Python+PyQt开发，在各种主流平台都可以使用。这个程序将是模块化，社区化的，任何人只要有需求，都可以提Issues，或者pull requests，然后这个模块将会添加到程序中，这样大家都能用了。当然这里的「提Issues，或者pull requests」是广义的概念，它可以是github项目主页的页面，也可以是独立的网站，独立的论坛，这个程序正在开发中，暂时没有Web的版本，以后开发对应的网站也未尝不可。

### 一个应用场景
小A是一个播客重度用户，他是一个Python初学者，有一天他开始听[talk python to me](https://talkpython.fm/)，在iTunes下载之后，他发现这个节目的网站上几乎所有的[episodes](https://talkpython.fm/episodes/all)都有对应的文稿，「真不错，可以学Python，可以练听力，还可以学英语」，但问题来了，小A用电脑的时候根本没空听Podcast，而这个播客的主页又没有做移动端的适配，拿手机完全没办法看，于是他提了一个Issue，程序员小B看见了这个Issue，嘿，刚好我也在听这个，就写这个模块方便大家吧，于是EE-Book新的版本中就有了这一模块，小A制作了电子书，终于可以拿着kindle或阅读了。

这样的场景当然还有很多。网络上的资源参差不齐，我们不缺阅读资源，我们缺的是深度阅读，EE-Book就可以给我们一个选择，在网络不便的时候，在需要断绝干扰深度思考的时候，我们可以利用EE-Book的功能进行深度阅读。

## 依赖 
===
 * [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/)(暂时没有放在项目目录中)
 * [lxml](http://lxml.de/)
 * [PyQt4](https://www.riverbankcomputing.com/software/pyqt/download)
 
### 解决依赖
```shell
$ sudo pip install -r requirements.txt
```
## 开发环境
Mac 10.11   
Python 	2.7.11      
PyCharm CE 5.0.3  

## 使用说明
待修复问题:
知乎:
暂时不能爬取私人收藏夹

