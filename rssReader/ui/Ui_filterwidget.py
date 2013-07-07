# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filterwidget.ui'
#
# Created: Mon Jun 17 10:26:33 2013
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
        Form.resize(559, 28)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.clear = QtGui.QToolButton(Form)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/editclear.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clear.setIcon(icon)
        self.clear.setAutoRaise(True)
        self.clear.setObjectName(_fromUtf8("clear"))
        self.horizontalLayout.addWidget(self.clear)
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.filter = QtGui.QLineEdit(Form)
        self.filter.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.filter.setObjectName(_fromUtf8("filter"))
        self.horizontalLayout.addWidget(self.filter)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.statusCombo = QtGui.QComboBox(Form)
        self.statusCombo.setFocusPolicy(QtCore.Qt.NoFocus)
        self.statusCombo.setObjectName(_fromUtf8("statusCombo"))
        self.statusCombo.addItem(_fromUtf8(""))
        self.statusCombo.addItem(_fromUtf8(""))
        self.statusCombo.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.statusCombo)
        self.label.setBuddy(self.filter)
        self.label_2.setBuddy(self.statusCombo)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.clear.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "过滤:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "状态:", None, QtGui.QApplication.UnicodeUTF8))
        self.statusCombo.setItemText(0, QtGui.QApplication.translate("Form", "所有文章", None, QtGui.QApplication.UnicodeUTF8))
        self.statusCombo.setItemText(1, QtGui.QApplication.translate("Form", "未读", None, QtGui.QApplication.UnicodeUTF8))
        self.statusCombo.setItemText(2, QtGui.QApplication.translate("Form", "重要", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc
