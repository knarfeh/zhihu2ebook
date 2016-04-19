# -*- coding: utf-8 -*-

import sys
import locale
import codecs
import os

__license__ = 'GPL v3'
__copyright__ = '2016, Frank He knarfeh@outlook.com'
__appname__ = u'EE-Book'
numeric_version = (0, 0, 1)
__version__ = u'.'.join(map(unicode, numeric_version))
__author__ = u"Frank he <knarfeh@outlook.com>"

u"""
Various run time constants.
"""

info_meta = u"""站点:         {website}
标题:         {title}
描述:         {desc}
是否需要登录?   {need_login}

支持的类型:

{supported_type}
"""

zhihu = {
    'website': 'zhihu',
    'title': u'知乎',
    'desc': u'与世界分享你的知识、经验和见解',
    'need_login': u'是!',
    'supported_type': u"""问题: http://www.zhihu.com/question/{question_id}
答案: http://www.zhihu.com/question/{question_id}/answer/{answer_id}
话题: http://www.zhihu.com/topic/{topic_id}
用户的全部回答: http://www.zhihu.com/people/{people_id}
            http://www.zhihu.com/people/{people_id}/answers
收藏夹: http://www.zhihu.com/collection/{collection_id}
专栏: http://zhuanlan.zhihu.com/{zhuanlan_id}"""
}

jianshu = {
    'website': 'http://www.zhihu.com',
    'title': u'简书',
    'desc': u"""交流故事，沟通想法
             一个基于内容分享的社区""",
    'need_login': u'否',
    'supported_type': u"""用户的所有文章: http://www.jianshu.com/users/{people_id}/latest_articles"""
}

sinablog = {
    'website': 'http://blog.sina.com.cn',
    'title': u'新浪博客',
    'desc': u"""全中国最主流，最具人气的博客频道。拥有最耀眼的娱乐明星博客、最知性的名人博客、最动人的情感博客，最自我的草根博客""",
    'need_login': u'否',
    'supported_type': u"""用户的所有文章: http://blog.sina.com.cn/u/{people_id}"""
}

csdnblog_info = {
    'website': 'http://blog.csdn.net/',
    'title': u'csdn博客',
    'desc': u"""""",
    'need_login': u'否',
    'supported_type': u"""用户的所有文章: http://blog.csdn.net/{people_id}"""
}

zhihu_info = info_meta.format(**zhihu)
jianshu_info = info_meta.format(**jianshu)
sinablog_info = info_meta.format(**sinablog)
csdnblog_info = info_meta.format(**csdnblog_info)

url_info = {
    'zhihu': zhihu_info,
    'jianshu': jianshu_info,
    'sinablog': sinablog_info,
    'csdnblog': csdnblog_info
}

_plat = sys.platform.lower()
iswindows = 'win32' in _plat or 'win64' in _plat
isosx = 'darwin' in _plat
isnewosx = isosx and getattr(sys, 'new_app_bundle', False)
isfreebsd = 'freebsd' in _plat
isnetbsd = 'netbsd' in _plat
isdragonflybsd = 'dragonfly' in _plat
isbsd = isfreebsd or isnetbsd or isdragonflybsd
islinux = not(iswindows or isosx or isbsd)
isfrozen = hasattr(sys, 'frozen')
isunix = isosx or islinux
isxp = iswindows and sys.getwindowsversion().major < 6
is64bit = sys.maxsize > (1 << 32)

try:
    preferred_encoding = locale.getpreferredencoding()
    codecs.lookup(preferred_encoding)
except:
    preferred_encoding = 'utf-8'

# #############################################################
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
EPUBSTOR_DIR = os.path.dirname(os.path.dirname(__file__)) + '/e-books_produced'
LIBRARY_DIR = os.path.join(PROJECT_DIR, 'bookdata') + os.sep

if not os.path.exists(LIBRARY_DIR):
    os.mkdir(LIBRARY_DIR)

LIBRARY = os.path.join(LIBRARY_DIR, "library.json")

if not os.path.exists(LIBRARY):
    open(LIBRARY, 'w').close()
# #############################################################

_osx_ver = None

ISOTIMEFORMAT = '%Y-%m-%d %X'

def get_osx_version():
    global _osx_ver
    if _osx_ver is None:
        import platform
        from collections import namedtuple
        OSX = namedtuple('OSX', 'major minor tertiary')
        try:
            ver = platform.mac_ver()[0].split('.')
            if len(ver) == 2:
                ver.append(0)
            _osx_ver = OSX(*(map(int, ver)))
        except:
            _osx_ver = OSX(0, 0, 0)
    return _osx_ver

filesystem_encoding = sys.getfilesystemencoding()
if filesystem_encoding is None:
    filesystem_encoding = 'utf-8'
else:
    try:
        if codecs.lookup(filesystem_encoding).name == 'ascii':
            filesystem_encoding = 'utf-8'
            # On linux, unicode arguments to os file functions are coerced to an ascii
            # bytestring if sys.getfilesystemencoding() == 'ascii', which is
            # just plain dumb. This is fixed by the icu.py module which, when
            # imported changes ascii to utf-8
    except:
        filesystem_encoding = 'utf-8'

DEBUG = False


def debug():
    global DEBUG
    DEBUG = True


def get_unicode_windows_env_var(name):
    import ctypes
    name = unicode(name)
    n = ctypes.windll.kernel32.GetEnvironmentVariableW(name, None, 0)
    if n == 0:
        return None
    buf = ctypes.create_unicode_buffer(u'\0'*n)
    ctypes.windll.kernel32.GetEnvironmentVariableW(name, buf, n)
    return buf.value


def get_windows_username():
    """
    Return the user name of the currently loggen in user as a unicode string.
    Note that usernames on windows are case insensitive, the case of the value
    returned depends on what the user typed into the login box at login time.
    """
    import ctypes
    try:
        advapi32 = ctypes.windll.advapi32
        GetUserName = getattr(advapi32, u'GetUserNameW')
    except AttributeError:
        pass
    else:
        buf = ctypes.create_unicode_buffer(257)
        n = ctypes.c_int(257)
        if GetUserName(buf, ctypes.byref(n)):
            return buf.value

    return get_unicode_windows_env_var(u'USERNAME')


def get_windows_temp_path():
    import ctypes
    n = ctypes.windll.kernel32.GetTempPathW(0, None)
    if n == 0:
        return None
    buf = ctypes.create_unicode_buffer(u'\0'*n)
    ctypes.windll.kernel32.GetTempPathW(n, buf)
    ans = buf.value
    return ans if ans else None


def get_windows_user_locale_name():
    import ctypes
    k32 = ctypes.windll.kernel32
    n = 255
    buf = ctypes.create_unicode_buffer(u'\0'*n)
    n = k32.GetUserDefaultLocaleName(buf, n)
    if n == 0:
        return None
    return u'_'.join(buf.value.split(u'-')[:2])

