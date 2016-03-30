#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from PyQt4 import Qt
from PyQt4.Qt import (QLayout, QWidget, pyqtSignal, QWebView, QSize, QPropertyAnimation,
                      QEasingCurve, QSizePolicy, QPixmap, QRect)

from math import floor

from src.resources import qrc_resources

# class DetailsLayout(QLayout):

def fit_image(width, height, pwidth, pheight):
    u"""
    fit image in box of width pwidth and height pheight
    :param width: Width of image
    :param height: Height of image
    :param pwidth: Width of box
    :param pheight: Height of box
    :return: scaled, new_width, new_height, scaled is True if new_width and/or new_height is different
    from width or height.
    """
    scaled = height > pheight or width > pwidth
    if height > pheight:
        corrf = pheight / float(height)
        width, height = floor(corrf*width), pheight
    if width > pwidth:
        corrf = pwidth / float(width)
        width, height = pwidth, floor(corrf*height)
    if height > pheight:
        corrf = pheight / float(height)
        width, height = floor(corrf*width), pheight
    return scaled, int(width), int(height)

class CoverView(QWidget):
    cover_changed = pyqtSignal(object, object)
    cover_removed = pyqtSignal(object)
    open_cover_width = pyqtSignal(object, object)

    def __init__(self, vertical, parent=None):
        QWidget.__init__(self, parent)
        self._current_pixmap_size = QSize(120, 120)
        self.vertical = vertical

        self.animation = QPropertyAnimation(self, b'current_pixmap_size', self)
        self.animation.setEasingCurve(QEasingCurve(QEasingCurve.OutExpo))
        self.animation.setDuration(1000)
        self.animation.setStartValue(QSize(0, 0))
        self.animation.valueChanged.connect(self.value_changed)

        self.setSizePolicy(
            QSizePolicy.Expanding if vertical else QSizePolicy.Minimum,
            QSizePolicy.Expanding
        )

        self.default_pixmap = QPixmap(":/book.png")
        self.pixmap = self.default_pixmap
        self.pwidth = self.pheight = None
        self.data = {}

        self.do_layout()

    def do_layout(self):
        if self.rect().width() == 0 or self.rect().height() == 0:
            return
        pixmap = self.pixmap
        pwidth, pheight = pixmap.width(), pixmap.height()
        try:
            self.pwidth, self.pheight = fit_image(pwidth, pheight, self.rect().width, self.rect().height())[1:]
        except:
            self.pwidth, self.pheight = self.rect().width()-1, self.rect().height()-1
        self.current_pixmap_size = QSize(self.pwidth, self.pheight)
        self.animation.setEndValue(self.current_pixmap_size)

    def value_changed(self, val):
        self.update()


class BookInfo(QWebView):
    link_clicked = pyqtSignal(object)

    def __init__(self, vertical, parent=None):
        QWebView.__init__(self, parent)
        s = self.setting()
        s.setAttribute(s.JavascriptEnabled, False)
        self.setAttribute(Qt.WA_OpaquePaintEvent, False)

class DetailsLayout(QLayout):
    def __init__(self, vertical, parent):
        QLayout.__init__(self, parent)
        self.vertical = vertical
        self._children = []
        self.min_size = QSize(190, 200) if vertical else QSize(120, 120)
        self.setContentMargins(0, 0, 0, 0)

    def minimumSize(self):
        return QSize(self.min_size)

    def addItem(self, child):
        if len(self._children) > 2:
            raise ValueError('This layout can only manage two children')
        self._children.append(child)

    def itemAt(self, i):
        try:
            return self._children[i]
        except:
            pass
        return None

    def takeAt(self, i):
        try:
            self._children.pop(i)
        except:
            pass
        return None

    def count(self):
        return len(self._children)

    def sizeHint(self):
        return QSize(self.min_size)

    def setGeometry(self, r):
        QLayout.setGeometry(self, r)
        self.do_layout(r)

    def cover_height(self, r):
        if not self._children[0].widget().isVisible():
            return 0
        mw = 1 + int(3/4. * r.height())
        try:
            pw = self._children[0].widget().pixmap.width()
        except:
            pw = 0
        if pw > 0:
            mw = min(mw, pw)
        return mw

    def do_layout(self, rect):
        if len(self._children) != 2:
            left, top, right, bottom = self.getContentsMargins()
            r = rect.adjusted(+left, +top, -right, -bottom)
            x = r.x()
            y = r.y()
            cover, details = self._children

        if self.vertical:
            ch = self.cover_height(r)
            cover.setGeometry(QRect(x, y, r.width(), ch))
            cover.widget().do_layout()
            y += ch + 5
            details.setGeometry(QRect(x, y, r.width(), r.height()-ch-5))
        else:
            cw = self.cover_width(r)
            cover.setGeometry(QRect(x, y, cw, r.height()))
            cover.widget().do_layout()
            x += cw + 5
            details.setGeometry(QRect(x, y, r.width()-cw-5, r.height()))


class BookDetails(QWidget):
    show_book_info = pyqtSignal()

    def __init__(self, vertical, parent=None):
        QWidget.__init__(self, parent)
        # self._layout =

    def handle_click(self, link):
        pass

    def mouseDoubleClickEvent(self, QMouseEvent):
        QMouseEvent.accept()
        pass

    def show_data(self, data):
        pass

    def update_layout(self):
        pass

    def reset_info(self):
        pass
