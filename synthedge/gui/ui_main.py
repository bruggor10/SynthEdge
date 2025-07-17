# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitledxQvLuJ.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QMainWindow,
    QMenuBar, QRadioButton, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(60, 30, 181, 89))
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.model_type_classifiers = QRadioButton(self.groupBox)
        self.model_type_classifiers.setObjectName(u"model_type_classifiers")

        self.verticalLayout.addWidget(self.model_type_classifiers)

        self.model_selector_regressors = QRadioButton(self.groupBox)
        self.model_selector_regressors.setObjectName(u"model_selector_regressors")
        self.model_selector_regressors.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

        self.verticalLayout.addWidget(self.model_selector_regressors)

        self.models = QComboBox(self.centralwidget)
        self.models.setObjectName(u"models")
        self.models.setGeometry(QRect(70, 150, 281, 61))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 20))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Select type of models", None))
        self.model_type_classifiers.setText(QCoreApplication.translate("MainWindow", u"Classifiers", None))
        self.model_selector_regressors.setText(QCoreApplication.translate("MainWindow", u"Regressors", None))
    # retranslateUi

