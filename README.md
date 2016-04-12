# EE-Book

([中文文档](./README_cn.md))    

[EE-Book](https://github.com/knarfeh/EE-Book) is a command-line utility to downlaod text from the Web, and make it a e-book. GUI is under developing.


## Usage

get help info:  

```shell
./ee-book -h
```

for example:  

```shell
./ee-book -u http://www.jianshu.com/users/b1dd2b2c87a8/latest_articles
```

then you can get the book:  
![yinwang](http://7xi5vu.com1.z0.glb.clouddn.com/2016-03-09jianshu_yinwang.png)

## Supported Sites (UPDATING!)
* [zhihu](https://www.zhihu.com/)
* [jianshu](https://www.jianshu.com/)
* [sinablog](http://blog.sina.com.cn)

## Prerequisites

 * [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/)
 * [lxml](http://lxml.de/)
 * [PyQt4](https://www.riverbankcomputing.com/software/pyqt/download)

### requirements

```shell
$ sudo pip install -r requirements.txt
```

[install pyqt4](https://riverbankcomputing.com/software/pyqt/download/)


### [TODO List](./doc/TODOlist.md)

## Relevant Infomation

* previous [README](https://github.com/knarfeh/EE-Book/blob/c4d870ff8cca6bbac97f04c9da727397cee8d519/README.md)

* An [article](http://knarfeh.github.io/2016/03/17/EE-Book/) posted on [v2ex](https://v2ex.com/)

## License

licensed under the [MIT license](./LICENSE).

