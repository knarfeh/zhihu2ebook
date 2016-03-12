# -*- coding: utf-8 -*-

import urllib2
import re
from bs4 import BeautifulSoup

from src.tools.match import Match

SinaBlog_author_id = 1287694611
href_article_list = 'http://blog.sina.com.cn/s/articlelist_{}_0_1.html'.format(SinaBlog_author_id)
href_index = 'http://blog.sina.com.cn/u/{}'.format(SinaBlog_author_id)
href_profile = 'http://blog.sina.com.cn/s/profile_{}.html'.format(SinaBlog_author_id)

article_href = 'http://blog.sina.com.cn/s/blog_5f34b1e601010fxd.html'

html = urllib2.urlopen(article_href)
content = html.read()

# print "content内容:" + content

soup = BeautifulSoup(content, "lxml")

def get_attr(dom, attr, defaultValue=""):
    u"""
    获取bs中tag.content的指定属性
    若content为空或者没有指定属性则返回默认值
    """
    if dom is None:
        return defaultValue
    return dom.get(attr, defaultValue)

def fix_html(content=''):
    content = content.replace('</br>', '').replace('</img>', '')
    content = content.replace('<br>', '<br/>')
    content = content.replace('href="//link.zhihu.com', 'href="https://link.zhihu.com')  # 修复跳转链接
    for item in re.findall(r'\<noscript\>.*?\</noscript\>', content, re.S):
        content = content.replace(item, '')
    return content

def get_tag_content(tag):
    u"""
    用于提取bs中tag.contents的内容
    需要对<br>进行预处理，将<br>换成<br/>,否则会爆栈，参考http://palydawn.blog.163.com/blog/static/1829690562012112285248753/
    """
    return "".join([unicode(x) for x in tag.contents])

def SinaBlog(content=''):
    u"""

    :param content: Sina博客网址, 如:http://blog.sina.com.cn/u/1287694611
    :return:  re.match object
    """
    return re.search(r'(?<=blog\.sina\.com\.cn/u/)(?P<SinaBlog_people_id>[^/\n\r]*)', content)

def SinaBlog_article_content(content=''):
    return re.search(r'(?<=<!-- 正文开始 -->)<?P<real_content>(<!-- 正文结束 -->)', content)



from src.tools.path import Path

path = Path()
print path.base_path


# article_body = soup.find('div', class_='articalContent')
# if not article_body:
#     print (u"博文内容没有找到")
# article_body = str(article_body)
#
# print article_body

# lindex = article_body.find('<div class="articalTitle"')
# rindex = article_body.find('<!-- 正文结束 -->')
# print rindex
# result = article_body[lindex:rindex]
# print result + '</div>'    # 因为没有爬取评论的部分作为博客的内容,所以最后会少一个</div>

# # result_re = SinaBlog_article_content(article_body)
# # result = result_re.group('real_content')
#
# print result



# print article_body

# article_body = soup.find('div', class_='artical', id='articlebody')
# article_body = article_body.find('div', id='sina_keyword_ad_area2')
# article_body = soup.select('div.articalContent')[0]
# print article_body
# author_name = soup.select('div.info_nm span strong')
# if not author_name:
#     print u"没有找到"
# print author_name

# title = soup.select('div.articalTitle h2')
# article_title = title[0].get_text()
# print article_title

# id = soup.select('div.artical h2')
# article_id = get_attr(id[0], 'id')
# article_id = article_id[2:]
# print article_id


# # 下面的代码是为了set_dom
# body = soup.find('div', class_='SG_conn', id='module_920')
# if body:
#     content = get_tag_content(body)
#     content = BeautifulSoup(fix_html(content), 'lxml')
#     print content

# article_href_list = []
#
# article_list = soup.select('span.atc_title a')
# for item in range(len(article_list)):
#     article_title = get_attr(article_list[item], 'href')
#     article_href_list.append(article_title)
#     print article_title
#
# print article_href_list

# article_num = soup.select('div.SG_connHead span em')
# article_num = article_num[0].get_text()
# print article_num[1:-1]
#
# print int(article_num)

# description = soup.select('table.personTable tbody tr td p')
# if not description:
    # Debug.logger.debug(u"没有找到个人简介")
    # return
# description = description[1].get_text().replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')
# self.info['description'] = description
# print description
# # print soup.prettify()
# div_info_img = soup.select('div.info_img img')      # 获得头像地址 creator_logo
# info_img_href = div_info_img.get('real_src')
# print info_img_href
# print get_attr(div_info_img[0], 'real_src')
# # print soup.

# creator_name = soup.select('div.info_nm span strong')       # 获得creator_name
# print creator_name[0].get_text()

# creator_id = soup.select('div.blognavInfo span a')
# creator_id_href = get_attr(creator_id[1], 'href')
#
# result = Match.SinaBlog_profile(creator_id)
# SinaBlog_id = result.group('SinaBlog_people_id')
# print SinaBlog_id



# # -*- coding: utf-8 -*-
#
# import threading
# import re
#
# from codes.baseclass import *
#
#
# class PageWoker(BaseClass, HttpBaseClass):
#     def __init__(self, url_info={}):
#         self.url_info = url_info
#         # self.print_dict(url_info)
#         # str_base_url_response = self.getHttpContent(url=url_info['base_url'])
#         # print "返回的目录内容？？：" + str_articlelist_response
#         # self.article_num = self.get_article_num(str_base_url_res=str_base_url_res)
#         # self.get_uid(str_base_url_response=str_base_url_response)
#
#     def get_article_package(self):
#         """
#         article_package:  [[article_title, article_body, post_time], [...]]
#         :return:
#         """
#         list_article_url = []
#         for int_current_page in range(self.url_info['article_pages']):
#             current_blog_page_url = "http://blog.sina.com.cn/s/articlelist_" + str(self.url_info['uid']) + "_0_" + str(int_current_page+1) + ".html"
#             # print current_blog_page_url
#             str_response = self.getHttpContent(url=current_blog_page_url)
#             now_article_url = re.findall(r'blog.sina.com.cn/s/blog_(\w+)\.html', str_response)
#             list_article_url = list_article_url + now_article_url
#
#         list_article_url.remove('4cf7b4ec0100eudp')     # 移除意见反馈留言板的ID（博文的形式）
#         # print "list_article_url" + str(list_article_url)
#         article_package = []       # 用来将所有的文章打包
#         for now_article_id in list_article_url:
#             # print now_article
#             article_url = "http://blog.sina.com.cn/s/blog_" + now_article_id + ".html"
#             article_url_response = self.getHttpContent(url=article_url)
#             now_article_title, now_article_body, now_post_time =\
#                 self.get_article_info(article_url_response=article_url_response, blog_title=self.url_info['blog_title'])
#             # TODO 没用title是因为制作电子书不能有中文
#             article_package.append([now_article_id, now_article_body, now_post_time])
#         # print "article_package！！！！" + str(article_package[0][0])
#         return article_package
#
#     def get_blog_info(self, base_url=''):
#         u"""
#         获得文章的数量，首页就有
#         :param base_url:
#         :return:
#         """
#         # print "article_num"
#         base_url_response = self.getHttpContent(url=base_url)
#         match = re.search(r'(?<=<em class="count SG_txtb">\()(\d{1,})', base_url_response)
#
#         if match:
#             article_num = match.group(0)
#             article_num = int(article_num)
#         else:
#             return 0     # 如果一篇博客都没有？？？TODO
#
#         match = re.search(r'(?<=<title>).*?(?=</title>)', base_url_response)
#         if match:
#             blog_title = match.group(0)
#         else:
#             blog_title = str(self.url_info['uid']) + "的博客"
#         return article_num, blog_title
#
#     def get_article_info(self, article_url_response, blog_title):
#         u"""
#         解析每篇文章，返回文章标题，内容，最后修改时间
#         :param article_url_response:
#         :return: article_title, article_body, post_time
#         """
#         match = re.search(r'(?<=<title>).*?(?=</title>)', article_url_response)
#         if match:
#             article_title = match.group(0).replace("_" + blog_title, "").replace("_新浪博客", "")
#         else:
#             article_title = "未匹配的文章标题"
#         # print "article title??:" + article_title
#         article_body = \
#             article_url_response[article_url_response.find("<!-- 正文开始 -->")+len("<!-- 正文开始 -->"):article_url_response.find("<!-- 正文结束 -->")]
#         # print "article_body:" + article_body
#         match = re.search(r'(?<=<span class="time SG_txtc">\().*?(?=\)</span>)', article_url_response)     # 最后更新时间
#         if match:
#             post_time = match.group(0)
#         else:
#             post_time = "未知时间"
#         # print "post_time:" + post_time
#
#         return article_title, article_body, post_time
#
#     def get_uid(self, base_url):
#         """
#         获得用户的uid
#         :param base_url:
#         :return:
#         """
#         str_base_url_response = self.getHttpContent(url=base_url)
#         match = re.search(r'(?<=articlelist_)\d{1,}', str_base_url_response)
#         if match:
#             article_num = match.group(0)
#             return int(article_num)
#         else:
#             return 0