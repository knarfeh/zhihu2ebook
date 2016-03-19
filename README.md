# EE-Book

## 简介

更多内容写在博客中，这里是个简单介绍。
### 缘起
在知乎「发现(大V们)更大的世界」的过程中，我发现了一个开源项目[ZhihuHelp](https://github.com/YaoZeyuan/ZhihuHelp)，刚好初学Python，于是跟着慢慢地学习，后来根据自己的需要写了简书的版本，能够把某个博主的所有博文做成电子书，如，把王垠的所有博客做成EPub格式的电子书：
![wangyin](http://7xi5vu.com1.z0.glb.clouddn.com/2016-03-09-jianshu_epub_wangyin.png?imageView/2/w/800/q/90)
地址是：[jianshu2e-book](https://github.com/knarfeh/jianshu2e-book)

再后来，我又写了新浪博客的版本，把韩寒的博客做成EPub格式的电子书：
![hanhanblog](http://7xi5vu.com1.z0.glb.clouddn.com/2016-02-02-SinaBloghanhanepub.png?imageView/2/w/800/q/90)

地址是：[SinaBlog2e-book](https://github.com/knarfeh/SinaBlog2e-book)

我是Kindle重度用户，这几个程序的功能对我很有帮助，用着用着，有一天我突然想到，其实这样的需求还真不少，我应该把这个程序变成一个框架，把需要爬取的网站作为一个个模块放在里面，于是便有了这个项目。

### 所以，EE-Book是什么？
简单来说，EE-Book能够让你把特定网站的特定内容爬取下来做成EPub格式的电子书。   

它是桌面程序，用Python+PyQt开发，在各种主流平台都可以使用。这个程序将是模块化，社区化的。

### 一个应用场景
小A是一个播客重度用户，他是一个Python初学者，有一天他开始听[talk python to me](https://talkpython.fm/)，在iTunes下载之后，他发现这个节目的网站上几乎所有的[episodes](https://talkpython.fm/episodes/all)都有对应的文稿，「真不错，可以学Python，可以练听力，还可以学英语」，但问题来了，小A用电脑的时候根本没空听Podcast，而这个播客的主页又没有做移动端的适配，拿手机完全没办法看，于是他提了一个Issue，程序员小B看见了这个Issue，嘿，刚好我也在听这个，就写这个模块方便大家吧，于是EE-Book新的版本中就有了这一模块，小A制作了电子书，终于可以拿着kindle或阅读了。

这样的场景当然还有很多。网络上的资源参差不齐，我们不缺阅读资源，我们缺的是深度阅读，EE-Book给我们一个这样的选择，在网络不便的时候，在需要断绝干扰深度思考的时候，我们可以利用EE-Book的功能进行深度阅读。这个，就是这个程序的意义。

## 依赖

 * [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/)
 * [lxml](http://lxml.de/)
 * [PyQt4](https://www.riverbankcomputing.com/software/pyqt/download)
 
### 解决依赖
```shell
$ sudo pip install -r requirements.txt
```
## 开发环境

Mac 10.11   
Python 2.7.11      
PyCharm CE 5.0.3  

## 使用说明

该项目最初是命令行界面，将网址写入ReadList.txt, 把EEBook.py的recipe_kind写为对应的种类，执行  

```shell
python EEBook.py
```

即可运行得到结果，生成的电子书在「生成的电子书」文件夹中。

目前正在用PyQt编写图形界面，运行

```shell
python UI_EEBook.py
```

即可。

### 待修复问题:
目前的bug，不完善的地方应该非常非常多。。。。。抱歉

知乎:  

* 登陆的部分需要优化
* 暂时不能爬取私人收藏夹

### TODO List
#### 写在前面
calibre写了快十年，功能已经非常强大，EE-Book这个程序本质上也只是造轮子而已，但我也想有创造性地造轮子，写这个程序，一方面是为了练手，另一方面也是为了做calibre不能做的事情。所以，如果全按照calibre的功能进行模仿的话，TODO list有太多要写了，目前EE-Book会更专注于电子书的制作上。电子书的管理，阅读等功能可能会在后期慢慢加上。

* 优化后台代码，使得添加模块变得简单、快捷
* 新浪博客
	* 单篇文章制作
	* 各种细节，比如评论数，发布时间、更新时间、标签等等
	* ...
* 简书
   * 单篇文章抓取，专题、文集的爬取
   * 各种细节，粉丝数、字数、收获喜欢
   * ...
* GUI界面
	* 图标
	* 通过标签分类浏览
	* 搜索功能
	* EPub阅读器
	* 通过选项配置知乎模块的config内容
	* ...
* 打包发布，制作mac的app程序，windows的exe程序

## License

[MIT](./LICENSE) 