# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '\\wsl$\Ubuntu-20.04\home\ppuska\mediscara_ws\src\mediscara\mediscara\scripts\widgets\layout\error_list_item.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ErrorListItem(object):
    def setupUi(self, ErrorListItem):
        ErrorListItem.setObjectName("ErrorListItem")
        ErrorListItem.resize(523, 31)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ErrorListItem.sizePolicy().hasHeightForWidth())
        ErrorListItem.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(ErrorListItem)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(ErrorListItem)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.label_node_name = QtWidgets.QLabel(ErrorListItem)
        self.label_node_name.setObjectName("label_node_name")
        self.horizontalLayout.addWidget(self.label_node_name)
        self.label_2 = QtWidgets.QLabel(ErrorListItem)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.label_error_message = QtWidgets.QLabel(ErrorListItem)
        self.label_error_message.setObjectName("label_error_message")
        self.horizontalLayout.addWidget(self.label_error_message)
        self.label_3 = QtWidgets.QLabel(ErrorListItem)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.label_error_code = QtWidgets.QLabel(ErrorListItem)
        self.label_error_code.setObjectName("label_error_code")
        self.horizontalLayout.addWidget(self.label_error_code)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(3, 2)
        self.horizontalLayout.setStretch(5, 1)

        self.retranslateUi(ErrorListItem)
        QtCore.QMetaObject.connectSlotsByName(ErrorListItem)

    def retranslateUi(self, ErrorListItem):
        _translate = QtCore.QCoreApplication.translate
        ErrorListItem.setWindowTitle(_translate("ErrorListItem", "Form"))
        self.label.setText(_translate("ErrorListItem", "Node name:"))
        self.label_node_name.setText(_translate("ErrorListItem", "TextLabel"))
        self.label_2.setText(_translate("ErrorListItem", "Error message:"))
        self.label_error_message.setText(_translate("ErrorListItem", "TextLabel"))
        self.label_3.setText(_translate("ErrorListItem", "Error code"))
        self.label_error_code.setText(_translate("ErrorListItem", "TextLabel"))
