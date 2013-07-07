# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created: Mon Jun 17 10:23:53 2013
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(480, 397)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMaximumSize(QtCore.QSize(480, 556))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/urssus.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setSizeGripEnabled(True)
        Dialog.setModal(False)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(9, 9, 461, 251))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/urssus.jpg")))
        self.label.setObjectName(_fromUtf8("label"))
        self.textBrowser = QtGui.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(10, 260, 461, 81))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(226, 226, 226, 180))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 226, 226, 180))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.textBrowser.setPalette(palette)
        self.textBrowser.setFrameShape(QtGui.QFrame.NoFrame)
        self.textBrowser.setFrameShadow(QtGui.QFrame.Plain)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.okButton = QtGui.QPushButton(Dialog)
        self.okButton.setGeometry(QtCore.QRect(190, 360, 77, 25))
        self.okButton.setObjectName(_fromUtf8("okButton"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "About uRSSus", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser.setHtml(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'宋体\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">NewsSpider:新闻收集器（Ver 0.01）</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">                测试版</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-size:8pt;\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("Dialog", "&关闭", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc
