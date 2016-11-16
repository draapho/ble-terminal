# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(762, 615)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBoxTx = QtGui.QGroupBox(self.centralwidget)
        self.groupBoxTx.setObjectName(_fromUtf8("groupBoxTx"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBoxTx)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.comboBoxCom = QtGui.QComboBox(self.groupBoxTx)
        self.comboBoxCom.setObjectName(_fromUtf8("comboBoxCom"))
        self.horizontalLayout.addWidget(self.comboBoxCom)
        self.lineEdit = QtGui.QLineEdit(self.groupBoxTx)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButtonSend = QtGui.QPushButton(self.groupBoxTx)
        self.pushButtonSend.setObjectName(_fromUtf8("pushButtonSend"))
        self.horizontalLayout.addWidget(self.pushButtonSend)
        self.verticalLayout.addWidget(self.groupBoxTx)
        self.groupBoxRx = QtGui.QGroupBox(self.centralwidget)
        self.groupBoxRx.setObjectName(_fromUtf8("groupBoxRx"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBoxRx)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.textBrowser = QtGui.QTextBrowser(self.groupBoxRx)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.verticalLayout_2.addWidget(self.textBrowser)
        self.pushButtonClr = QtGui.QPushButton(self.groupBoxRx)
        self.pushButtonClr.setObjectName(_fromUtf8("pushButtonClr"))
        self.verticalLayout_2.addWidget(self.pushButtonClr)
        self.verticalLayout.addWidget(self.groupBoxRx)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Terminal", None))
        self.groupBoxTx.setTitle(_translate("MainWindow", "TX", None))
        self.pushButtonSend.setText(_translate("MainWindow", "Send", None))
        self.groupBoxRx.setTitle(_translate("MainWindow", "RX", None))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>", None))
        self.pushButtonClr.setText(_translate("MainWindow", "Clear Rx Data", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

