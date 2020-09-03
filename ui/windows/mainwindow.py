# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'mainwindow.ui'
##
# Created by: Qt User Interface Compiler version 5.15.0
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
                            QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                           QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
                           QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1140, 857)
        self.open_image = QAction(MainWindow)
        self.open_image.setObjectName(u"open_image")
        self.open_device = QAction(MainWindow)
        self.open_device.setObjectName(u"open_device")
        self.field_depth_tool = QAction(MainWindow)
        self.field_depth_tool.setObjectName(u"field_depth_tool")
        self.field_depth_tool.setCheckable(False)
        self.shake_tool = QAction(MainWindow)
        self.shake_tool.setObjectName(u"shake_tool")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.mdiArea = QMdiArea(self.centralwidget)
        self.mdiArea.setObjectName(u"mdiArea")
        self.mdiArea.setLineWidth(0)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        self.mdiArea.setTabShape(QTabWidget.Rounded)

        self.gridLayout_2.addWidget(self.mdiArea, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1140, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menu.addAction(self.open_image)
        self.menu.addAction(self.open_device)
        self.menu_2.addAction(self.field_depth_tool)
        self.menu_2.addAction(self.shake_tool)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"ImageTools", None))
        self.open_image.setText(QCoreApplication.translate(
            "MainWindow", u"\u6253\u5f00\u56fe\u7247", None))
        self.open_device.setText(QCoreApplication.translate(
            "MainWindow", u"\u6253\u5f00\u8bbe\u5907(RTSP)", None))
        self.field_depth_tool.setText(QCoreApplication.translate(
            "MainWindow", u"\u955c\u5934\u8ba1\u7b97\u5668", None))
        self.shake_tool.setText(QCoreApplication.translate(
            "MainWindow", u"\u6296\u52a8\u6d4b\u8bd5\u5de5\u5177", None))
        self.menu.setTitle(QCoreApplication.translate(
            "MainWindow", u"\u6587\u4ef6", None))
        self.menu_2.setTitle(QCoreApplication.translate(
            "MainWindow", u"\u5de5\u5177", None))
    # retranslateUi