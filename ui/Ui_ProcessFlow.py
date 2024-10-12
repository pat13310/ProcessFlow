# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'flowprocessHQiJWP.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGraphicsView, QHBoxLayout, QHeaderView,
    QListView, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QSplitter,
    QStatusBar, QTableView, QVBoxLayout, QWidget)

class Ui_ProcessFlow(object):
    def setupUi(self, ProcessFlow):
        if not ProcessFlow.objectName():
            ProcessFlow.setObjectName(u"ProcessFlow")
        ProcessFlow.resize(1259, 709)
        ProcessFlow.setStyleSheet(u"color:white;\n"
"background-color: #444444;")
        self.actionA_propos_de = QAction(ProcessFlow)
        self.actionA_propos_de.setObjectName(u"actionA_propos_de")
        self.actionNouveau = QAction(ProcessFlow)
        self.actionNouveau.setObjectName(u"actionNouveau")
        self.actionSAuver = QAction(ProcessFlow)
        self.actionSAuver.setObjectName(u"actionSAuver")
        self.actionSauver_sous = QAction(ProcessFlow)
        self.actionSauver_sous.setObjectName(u"actionSauver_sous")
        self.actionQuitter = QAction(ProcessFlow)
        self.actionQuitter.setObjectName(u"actionQuitter")
        self.actionExporter = QAction(ProcessFlow)
        self.actionExporter.setObjectName(u"actionExporter")
        self.centralwidget = QWidget(ProcessFlow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setHandleWidth(4)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.listView = QListView(self.widget)
        self.listView.setObjectName(u"listView")
        self.listView.setStyleSheet(u"background-color: #313131;")

        self.verticalLayout_3.addWidget(self.listView)

        self.splitter.addWidget(self.widget)
        self.main = QWidget(self.splitter)
        self.main.setObjectName(u"main")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(2)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.main.sizePolicy().hasHeightForWidth())
        self.main.setSizePolicy(sizePolicy1)
        self.main.setStyleSheet(u"background-color: #999;")
        self.verticalLayout_4 = QVBoxLayout(self.main)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, -1, -1, 2)
        self.graphicsView = QGraphicsView(self.main)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setMinimumSize(QSize(530, 0))
        self.graphicsView.setStyleSheet(u"QPushButton{\n"
"	color:white;\n"
"}\n"
"QPushButton:hover{\n"
"\n"
"background-color: #999;\n"
"}\n"
"")

        self.verticalLayout_4.addWidget(self.graphicsView)

        self.widget_4 = QWidget(self.main)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setMinimumSize(QSize(0, 35))
        self.widget_4.setMaximumSize(QSize(16777215, 35))
        self.widget_4.setStyleSheet(u"background-color: #686868;")
        self.horizontalLayout = QHBoxLayout(self.widget_4)
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.btn_play = QPushButton(self.widget_4)
        self.btn_play.setObjectName(u"btn_play")
        self.btn_play.setStyleSheet(u"QPushButton::hover{\n"
"	color: rgb(0, 255, 127);\n"
"	background-color: #00ff7f;\n"
"}")
        icon = QIcon(QIcon.fromTheme(u"media-playback-start"))
        self.btn_play.setIcon(icon)
        self.btn_play.setFlat(True)

        self.horizontalLayout.addWidget(self.btn_play)

        self.btn_pause = QPushButton(self.widget_4)
        self.btn_pause.setObjectName(u"btn_pause")
        self.btn_pause.setStyleSheet(u"QPushButton::hover{\n"
"	color: rgb(0, 255, 127);\n"
"	background-color: #00ff7f;\n"
"}")
        icon1 = QIcon(QIcon.fromTheme(u"media-playback-pause"))
        self.btn_pause.setIcon(icon1)
        self.btn_pause.setFlat(True)

        self.horizontalLayout.addWidget(self.btn_pause)

        self.btn_stop = QPushButton(self.widget_4)
        self.btn_stop.setObjectName(u"btn_stop")
        self.btn_stop.setStyleSheet(u"QPushButton::hover{\n"
"	color: rgb(0, 255, 127);\n"
"	background-color: #00ff7f;\n"
"}")
        icon2 = QIcon(QIcon.fromTheme(u"media-playback-stop"))
        self.btn_stop.setIcon(icon2)
        self.btn_stop.setFlat(True)

        self.horizontalLayout.addWidget(self.btn_stop)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_4.addWidget(self.widget_4)

        self.splitter.addWidget(self.main)
        self.widget_3 = QWidget(self.splitter)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setMinimumSize(QSize(250, 0))
        self.widget_3.setStyleSheet(u"background-color: #616161;")
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(2, 2, 2, -1)
        self.tableView = QTableView(self.widget_3)
        self.tableView.setObjectName(u"tableView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy2)
        self.tableView.setStyleSheet(u"background-color: rgb(61, 61, 61);\n"
"color:white;")
        self.tableView.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.tableView)

        self.splitter.addWidget(self.widget_3)

        self.verticalLayout.addWidget(self.splitter)

        ProcessFlow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(ProcessFlow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1259, 33))
        self.menuFichier = QMenu(self.menubar)
        self.menuFichier.setObjectName(u"menuFichier")
        self.menuAide = QMenu(self.menubar)
        self.menuAide.setObjectName(u"menuAide")
        ProcessFlow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(ProcessFlow)
        self.statusbar.setObjectName(u"statusbar")
        ProcessFlow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFichier.menuAction())
        self.menubar.addAction(self.menuAide.menuAction())
        self.menuFichier.addAction(self.actionNouveau)
        self.menuFichier.addSeparator()
        self.menuFichier.addAction(self.actionSAuver)
        self.menuFichier.addAction(self.actionSauver_sous)
        self.menuFichier.addAction(self.actionExporter)
        self.menuFichier.addSeparator()
        self.menuFichier.addAction(self.actionQuitter)
        self.menuAide.addAction(self.actionA_propos_de)

        self.retranslateUi(ProcessFlow)

        QMetaObject.connectSlotsByName(ProcessFlow)
    # setupUi

    def retranslateUi(self, ProcessFlow):
        ProcessFlow.setWindowTitle(QCoreApplication.translate("ProcessFlow", u"MainWindow", None))
        self.actionA_propos_de.setText(QCoreApplication.translate("ProcessFlow", u"A propos de ...", None))
        self.actionNouveau.setText(QCoreApplication.translate("ProcessFlow", u"Nouveau", None))
        self.actionSAuver.setText(QCoreApplication.translate("ProcessFlow", u"Sauver", None))
        self.actionSauver_sous.setText(QCoreApplication.translate("ProcessFlow", u"Sauver sous", None))
        self.actionQuitter.setText(QCoreApplication.translate("ProcessFlow", u"Quitter", None))
        self.actionExporter.setText(QCoreApplication.translate("ProcessFlow", u"Exporter", None))
        self.btn_play.setText("")
        self.btn_pause.setText("")
        self.btn_stop.setText("")
        self.menuFichier.setTitle(QCoreApplication.translate("ProcessFlow", u"Fichier", None))
        self.menuAide.setTitle(QCoreApplication.translate("ProcessFlow", u"Aide", None))
    # retranslateUi

