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
EPUBSTOR_DIR = os.path.dirname(os.path.dirname(__file__)) + '/生成的电子书'
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

