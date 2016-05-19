# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Program Files\Python 2.7\MCmapper\code\grid.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Grid_Screen(object):
    def setupUi(self, Grid_Screen):
        Grid_Screen.setObjectName(_fromUtf8("Grid_Screen"))
        Grid_Screen.resize(728, 670)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/png/Map_Item_16.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Grid_Screen.setWindowIcon(icon)
        self.gridLayout_2 = QtGui.QGridLayout(Grid_Screen)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.GridTable = QtGui.QTableWidget(Grid_Screen)
        self.GridTable.setAlternatingRowColors(False)
        self.GridTable.setObjectName(_fromUtf8("GridTable"))
        self.GridTable.setColumnCount(0)
        self.GridTable.setRowCount(0)
        self.GridTable.horizontalHeader().setVisible(False)
        self.GridTable.verticalHeader().setVisible(False)
        self.gridLayout_2.addWidget(self.GridTable, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame = QtGui.QFrame(Grid_Screen)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.xCen_SB = QtGui.QSpinBox(self.frame)
        self.xCen_SB.setAlignment(QtCore.Qt.AlignCenter)
        self.xCen_SB.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.xCen_SB.setMinimum(-999999999)
        self.xCen_SB.setMaximum(999999999)
        self.xCen_SB.setProperty("value", 0)
        self.xCen_SB.setObjectName(_fromUtf8("xCen_SB"))
        self.gridLayout.addWidget(self.xCen_SB, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.zCen_SB = QtGui.QSpinBox(self.frame)
        self.zCen_SB.setAlignment(QtCore.Qt.AlignCenter)
        self.zCen_SB.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.zCen_SB.setMinimum(-999999999)
        self.zCen_SB.setMaximum(999999999)
        self.zCen_SB.setProperty("value", 0)
        self.zCen_SB.setObjectName(_fromUtf8("zCen_SB"))
        self.gridLayout.addWidget(self.zCen_SB, 1, 1, 2, 1)
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 2, 1)
        self.scale_SB = QtGui.QSpinBox(self.frame)
        self.scale_SB.setAlignment(QtCore.Qt.AlignCenter)
        self.scale_SB.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.scale_SB.setMaximum(4)
        self.scale_SB.setObjectName(_fromUtf8("scale_SB"))
        self.gridLayout.addWidget(self.scale_SB, 3, 1, 1, 1)
        self.horizontalLayout.addWidget(self.frame)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.frame_2 = QtGui.QFrame(Grid_Screen)
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtGui.QFrame.Plain)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.GenPosi = QtGui.QPushButton(self.frame_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GenPosi.sizePolicy().hasHeightForWidth())
        self.GenPosi.setSizePolicy(sizePolicy)
        self.GenPosi.setObjectName(_fromUtf8("GenPosi"))
        self.verticalLayout.addWidget(self.GenPosi)
        self.Close_PB = QtGui.QPushButton(self.frame_2)
        self.Close_PB.setObjectName(_fromUtf8("Close_PB"))
        self.verticalLayout.addWidget(self.Close_PB)
        self.horizontalLayout.addWidget(self.frame_2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.frame_3 = QtGui.QFrame(Grid_Screen)
        self.frame_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtGui.QFrame.Plain)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.ComDisplay = QtGui.QLineEdit(self.frame_3)
        self.ComDisplay.setMaximumSize(QtCore.QSize(250, 16777215))
        self.ComDisplay.setAlignment(QtCore.Qt.AlignCenter)
        self.ComDisplay.setReadOnly(False)
        self.ComDisplay.setObjectName(_fromUtf8("ComDisplay"))
        self.verticalLayout_2.addWidget(self.ComDisplay)
        self.clipCB = QtGui.QCheckBox(self.frame_3)
        self.clipCB.setMaximumSize(QtCore.QSize(250, 16777215))
        self.clipCB.setObjectName(_fromUtf8("clipCB"))
        self.verticalLayout_2.addWidget(self.clipCB)
        self.horizontalLayout.addWidget(self.frame_3)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Grid_Screen)
        QtCore.QMetaObject.connectSlotsByName(Grid_Screen)

    def retranslateUi(self, Grid_Screen):
        Grid_Screen.setWindowTitle(_translate("Grid_Screen", "Map Aligner", None))
        self.label.setText(_translate("Grid_Screen", "X Center:", None))
        self.xCen_SB.setToolTip(_translate("Grid_Screen", "The map\'s X position", None))
        self.label_2.setText(_translate("Grid_Screen", "Z Center", None))
        self.zCen_SB.setToolTip(_translate("Grid_Screen", "The map\'s Z position", None))
        self.label_3.setText(_translate("Grid_Screen", "Map scale:", None))
        self.scale_SB.setToolTip(_translate("Grid_Screen", "The map\'s scale\n"
"The larger the scale, the more zoomed out it is\n"
"\n"
"0 : 1 pixel = 1 block\n"
"1 : 1 pixel = 2x2 blocks\n"
"2 : 1 pixel = 4x4 blocks\n"
"3 : 1 pixel = 8x8 blocks\n"
"4 : 1 pixel = 16x16 blocks (1 chunk)", None))
        self.GenPosi.setToolTip(_translate("Grid_Screen", "Generate map positions", None))
        self.GenPosi.setText(_translate("Grid_Screen", "Map positions", None))
        self.Close_PB.setToolTip(_translate("Grid_Screen", "Close window", None))
        self.Close_PB.setText(_translate("Grid_Screen", "Close", None))
        self.ComDisplay.setPlaceholderText(_translate("Grid_Screen", "/tp <x> <y> <z>", None))
        self.clipCB.setText(_translate("Grid_Screen", "Copy to clipboard on selection", None))

import MCIcon_rc
