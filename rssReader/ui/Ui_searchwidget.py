# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'searchwidget.ui'
#
# Created: Mon Jun 17 10:25:24 2013
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(369, 32)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setMargin(2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.close = QtGui.QToolButton(Form)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/editdelete.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.close.setIcon(icon)
        self.close.setAutoRaise(True)
        self.close.setObjectName(_fromUtf8("close"))
        self.horizontalLayout.addWidget(self.close)
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.text = QtGui.QLineEdit(Form)
        self.text.setObjectName(_fromUtf8("text"))
        self.horizontalLayout.addWidget(self.text)
        self.previous = QtGui.QToolButton(Form)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/1leftarrow.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.previous.setIcon(icon1)
        self.previous.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.previous.setAutoRaise(True)
        self.previous.setObjectName(_fromUtf8("previous"))
        self.horizontalLayout.addWidget(self.previous)
        self.next = QtGui.QToolButton(Form)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/1rightarrow.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next.setIcon(icon2)
        self.next.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.next.setAutoRaise(True)
        self.next.setObjectName(_fromUtf8("next"))
        self.horizontalLayout.addWidget(self.next)
        self.matchCase = QtGui.QCheckBox(Form)
        self.matchCase.setObjectName(_fromUtf8("matchCase"))
        self.horizontalLayout.addWidget(self.matchCase)
        self.label.setBuddy(self.text)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.text, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.next.animateClick)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.close.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.close.setShortcut(QtGui.QApplication.translate("Form", "Esc", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "&查找:", None, QtGui.QApplication.UnicodeUTF8))
        self.previous.setText(QtGui.QApplication.translate("Form", "&Previous", None, QtGui.QApplication.UnicodeUTF8))
        self.next.setText(QtGui.QApplication.translate("Form", "&Next", None, QtGui.QApplication.UnicodeUTF8))
        self.matchCase.setText(QtGui.QApplication.translate("Form", "匹配大小写", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc
