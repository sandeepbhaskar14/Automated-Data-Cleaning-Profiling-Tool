# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainUI.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1217, 718)
        MainWindow.setStyleSheet(u"QMainWindow{\n"
"	background-color: rgb(45, 45, 45);\n"
"}\n"
"\n"
"/* Styles for the vertical scrollbar */\n"
"\n"
"QScrollBar:vertical {\n"
"	border-radius:5px;\n"
"    background-color: rgb(60, 60, 91);/* #F0F0F0; */\n"
"    width: 12px;\n"
"    margin: 0px 0px 0px 0px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    /*background-color: #4F9FFE;*/\n"
"	background-color:rgb(80, 80, 122);\n"
"	border-radius:5px;\n"
"    min-height: 20px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {\n"
"    /*background-color: #4F9FFE;*/\n"
"	/*background-color: rgb(170, 0, 255);*/\n"
"	background-color:rgb(0, 128, 255);\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical {\n"
"    height: 0px;\n"
"    subcontrol-position: bottom;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"    subcontrol-position: top;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"    width: 0px;\n"
"    height: 0px;\n"
""
                        "    background: none;\n"
"}\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}\n"
"\n"
"\n"
"/*stylesheet for horizontal scrollbar*/\n"
"\n"
"\n"
"QScrollBar:horizontal {\n"
"	border-radius:5px;\n"
"    background-color: rgb(60, 60, 91);/* #F0F0F0; */\n"
"    width: 12px;\n"
"    margin: 0px 0px 0px 0px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal {\n"
"    /*background-color: #4F9FFE;*/\n"
"	background-color:rgb(80, 80, 122);\n"
"	border-radius:5px;\n"
"    min-height: 20px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal:hover {\n"
"    /*background-color: #4F9FFE;*/\n"
"	background-color: rgb(170, 0, 255);;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal {\n"
"    height: 0px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal {\n"
"    height: 0px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:h"
                        "orizontal {\n"
"    width: 0px;\n"
"    height: 0px;\n"
"    background: none;\n"
"}\n"
"\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
"    background: none;\n"
"}\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.drop_shadow_frame = QFrame(self.centralwidget)
        self.drop_shadow_frame.setObjectName(u"drop_shadow_frame")
        self.drop_shadow_frame.setStyleSheet(u"QFrame{\n"
"	border-radius:10px;\n"
"}")
        self.drop_shadow_frame.setFrameShape(QFrame.StyledPanel)
        self.drop_shadow_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.drop_shadow_frame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.Top_Bar = QFrame(self.drop_shadow_frame)
        self.Top_Bar.setObjectName(u"Top_Bar")
        self.Top_Bar.setMaximumSize(QSize(16777215, 38))
        self.Top_Bar.setStyleSheet(u"QFrame{\n"
"	background-color: rgb(243, 243, 243)\n"
"}")
        self.Top_Bar.setFrameShape(QFrame.StyledPanel)
        self.Top_Bar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.Top_Bar)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.top_bar_frame = QFrame(self.Top_Bar)
        self.top_bar_frame.setObjectName(u"top_bar_frame")
        self.top_bar_frame.setStyleSheet(u"QFrame{\n"
"	border-bottom-left-radius:0px;\n"
"}")
        self.top_bar_frame.setFrameShape(QFrame.StyledPanel)
        self.top_bar_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.top_bar_frame)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(5, 0, 0, 0)
        self.pushButton = QPushButton(self.top_bar_frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 35))
        self.pushButton.setMaximumSize(QSize(50, 16777215))
        self.pushButton.setStyleSheet(u"background:none;\n"
"border:none;")
        icon = QIcon()
        icon.addFile(u"../assets/icons/app_icon.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QSize(30, 30))

        self.horizontalLayout_5.addWidget(self.pushButton)

        self.top_bar_label = QLabel(self.top_bar_frame)
        self.top_bar_label.setObjectName(u"top_bar_label")
        font = QFont()
        font.setFamily(u"Roboto")
        font.setPointSize(9)
        self.top_bar_label.setFont(font)
        self.top_bar_label.setStyleSheet(u"background:none;\n"
"color:rgb(49, 49, 49)")
        self.top_bar_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.top_bar_label)


        self.horizontalLayout.addWidget(self.top_bar_frame)

        self.top_bar_button_frame = QFrame(self.Top_Bar)
        self.top_bar_button_frame.setObjectName(u"top_bar_button_frame")
        self.top_bar_button_frame.setMinimumSize(QSize(200, 0))
        self.top_bar_button_frame.setMaximumSize(QSize(200, 16777215))
        self.top_bar_button_frame.setStyleSheet(u"background-color: rgb(239, 239, 239);\n"
"border-top-left-radius:0px;\n"
"border-bottom-left-radius:0px;\n"
"border-bottom-right-radius:0px;")
        self.top_bar_button_frame.setFrameShape(QFrame.StyledPanel)
        self.top_bar_button_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.top_bar_button_frame)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.button_minimize = QPushButton(self.top_bar_button_frame)
        self.button_minimize.setObjectName(u"button_minimize")
        self.button_minimize.setMinimumSize(QSize(0, 38))
        self.button_minimize.setStyleSheet(u"QPushButton{\n"
"	border:none;\n"
"	background:none;\n"
"	border-radius:0px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(218, 218, 218)\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u"../assets/icons/minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_minimize.setIcon(icon1)

        self.horizontalLayout_3.addWidget(self.button_minimize)

        self.button_restore = QPushButton(self.top_bar_button_frame)
        self.button_restore.setObjectName(u"button_restore")
        self.button_restore.setMinimumSize(QSize(0, 38))
        self.button_restore.setStyleSheet(u"QPushButton{\n"
"	border:none;\n"
"	background:none;\n"
"	border-radius:0px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color:  rgb(218, 218, 218)\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u"../assets/icons/maximize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_restore.setIcon(icon2)
        self.button_restore.setIconSize(QSize(20, 20))

        self.horizontalLayout_3.addWidget(self.button_restore)

        self.button_close = QPushButton(self.top_bar_button_frame)
        self.button_close.setObjectName(u"button_close")
        self.button_close.setMinimumSize(QSize(0, 38))
        self.button_close.setStyleSheet(u"QPushButton{\n"
"	border:none;\n"
"	background:none;\n"
"	border-radius:0px;\n"
"	border-top-right-radius:10px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color:rgb(200, 0, 0)\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u"../assets/icons/close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_close.setIcon(icon3)

        self.horizontalLayout_3.addWidget(self.button_close)


        self.horizontalLayout.addWidget(self.top_bar_button_frame)


        self.verticalLayout_2.addWidget(self.Top_Bar)

        self.Content = QFrame(self.drop_shadow_frame)
        self.Content.setObjectName(u"Content")
        self.Content.setStyleSheet(u"border-bottom-left-radius:10px;\n"
"border-bottom-right-radius:10px;")
        self.Content.setFrameShape(QFrame.StyledPanel)
        self.Content.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.Content)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.toggle_frame_left = QFrame(self.Content)
        self.toggle_frame_left.setObjectName(u"toggle_frame_left")
        self.toggle_frame_left.setMinimumSize(QSize(75, 0))
        self.toggle_frame_left.setMaximumSize(QSize(75, 16777215))
        self.toggle_frame_left.setStyleSheet(u"background-color: #272C36;\n"
"border-radius:0px;\n"
"border-bottom-left-radius:10px;\n"
"")
        self.toggle_frame_left.setFrameShape(QFrame.StyledPanel)
        self.toggle_frame_left.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.toggle_frame_left)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_9 = QFrame(self.toggle_frame_left)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMaximumSize(QSize(16777215, 60))
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 20, 0)
        self.button_toggle = QPushButton(self.frame_9)
        self.button_toggle.setObjectName(u"button_toggle")
        self.button_toggle.setMinimumSize(QSize(85, 50))
        self.button_toggle.setMaximumSize(QSize(85, 60))
        font1 = QFont()
        font1.setFamily(u"Noto Sans")
        font1.setPointSize(10)
        self.button_toggle.setFont(font1)
        self.button_toggle.setLayoutDirection(Qt.LeftToRight)
        self.button_toggle.setStyleSheet(u"QPushButton{\n"
"	background:none;\n"
"	border:none;\n"
"	color: rgba(255, 255, 255, 180);\n"
"	border-radius:0px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color: rgb(49, 55, 68);\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u"../assets/icons/toggle.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_toggle.setIcon(icon4)
        self.button_toggle.setIconSize(QSize(30, 30))

        self.horizontalLayout_8.addWidget(self.button_toggle)

        self.frame_10 = QFrame(self.frame_9)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_8.addWidget(self.frame_10)


        self.verticalLayout_3.addWidget(self.frame_9)

        self.frame_status = QFrame(self.toggle_frame_left)
        self.frame_status.setObjectName(u"frame_status")
        self.frame_status.setMaximumSize(QSize(16777215, 60))
        self.frame_status.setStyleSheet(u"QFrame{\n"
"	border-radius: 0px;\n"
"}\n"
"QFrame:hover{\n"
"	background-color: rgb(55, 62, 76);\n"
"	border:2px solid rgba(0, 159, 238, 140);\n"
"	border-radius:5px;\n"
"}")
        self.frame_status.setFrameShape(QFrame.StyledPanel)
        self.frame_status.setFrameShadow(QFrame.Raised)
        self.button_home = QPushButton(self.frame_status)
        self.button_home.setObjectName(u"button_home")
        self.button_home.setGeometry(QRect(0, 0, 241, 60))
        self.button_home.setMinimumSize(QSize(70, 0))
        self.button_home.setMaximumSize(QSize(16777215, 60))
        font2 = QFont()
        font2.setFamily(u"Roboto")
        font2.setPointSize(10)
        self.button_home.setFont(font2)
        self.button_home.setLayoutDirection(Qt.LeftToRight)
        self.button_home.setStyleSheet(u"background:none;\n"
"border:none;\n"
"color: rgba(255, 255, 255, 180);")
        icon5 = QIcon()
        icon5.addFile(u"../assets/icons/home.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_home.setIcon(icon5)
        self.button_home.setIconSize(QSize(30, 30))

        self.verticalLayout_3.addWidget(self.frame_status)

        self.frame_privacy = QFrame(self.toggle_frame_left)
        self.frame_privacy.setObjectName(u"frame_privacy")
        self.frame_privacy.setMaximumSize(QSize(16777215, 60))
        self.frame_privacy.setStyleSheet(u"QFrame{\n"
"	border-radius: 0px;\n"
"}\n"
"QFrame:hover{\n"
"	background-color: rgb(55, 62, 76);\n"
"	border:2px solid rgba(0, 159, 238, 140);\n"
"	border-radius:5px;\n"
"}")
        self.frame_privacy.setFrameShape(QFrame.StyledPanel)
        self.frame_privacy.setFrameShadow(QFrame.Raised)
        self.button_dashboard = QPushButton(self.frame_privacy)
        self.button_dashboard.setObjectName(u"button_dashboard")
        self.button_dashboard.setGeometry(QRect(0, 0, 241, 60))
        self.button_dashboard.setMinimumSize(QSize(70, 60))
        self.button_dashboard.setMaximumSize(QSize(16777215, 60))
        self.button_dashboard.setFont(font2)
        self.button_dashboard.setStyleSheet(u"background:none;\n"
"border:none;\n"
"color: rgba(255, 255, 255, 180);")
        icon6 = QIcon()
        icon6.addFile(u"../assets/icons/dashboard.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_dashboard.setIcon(icon6)
        self.button_dashboard.setIconSize(QSize(30, 30))

        self.verticalLayout_3.addWidget(self.frame_privacy)

        self.frame_protection = QFrame(self.toggle_frame_left)
        self.frame_protection.setObjectName(u"frame_protection")
        self.frame_protection.setMaximumSize(QSize(16777215, 60))
        self.frame_protection.setStyleSheet(u"QFrame{\n"
"	border-radius: 0px;\n"
"}\n"
"QFrame:hover{\n"
"	background-color: rgb(55, 62, 76);\n"
"	border:2px solid rgba(0, 159, 238, 140);\n"
"	border-radius:5px;\n"
"}")
        self.frame_protection.setFrameShape(QFrame.StyledPanel)
        self.frame_protection.setFrameShadow(QFrame.Raised)
        self.button_cleaning = QPushButton(self.frame_protection)
        self.button_cleaning.setObjectName(u"button_cleaning")
        self.button_cleaning.setGeometry(QRect(0, 0, 241, 60))
        self.button_cleaning.setMinimumSize(QSize(60, 60))
        self.button_cleaning.setFont(font2)
        self.button_cleaning.setStyleSheet(u"background:none;\n"
"border:none;\n"
"color: rgba(255, 255, 255, 180);")
        icon7 = QIcon()
        icon7.addFile(u"../assets/icons/cleaning.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_cleaning.setIcon(icon7)
        self.button_cleaning.setIconSize(QSize(30, 30))

        self.verticalLayout_3.addWidget(self.frame_protection)

        self.frame_performance = QFrame(self.toggle_frame_left)
        self.frame_performance.setObjectName(u"frame_performance")
        self.frame_performance.setMaximumSize(QSize(16777215, 60))
        self.frame_performance.setStyleSheet(u"QFrame{\n"
"	border-radius: 0px;\n"
"}\n"
"QFrame:hover{\n"
"	background-color: rgb(55, 62, 76);\n"
"	border:2px solid rgba(0, 159, 238, 140);\n"
"	border-radius:5px;\n"
"}")
        self.frame_performance.setFrameShape(QFrame.StyledPanel)
        self.frame_performance.setFrameShadow(QFrame.Raised)
        self.button_report = QPushButton(self.frame_performance)
        self.button_report.setObjectName(u"button_report")
        self.button_report.setGeometry(QRect(0, 0, 241, 60))
        self.button_report.setMinimumSize(QSize(70, 60))
        self.button_report.setMaximumSize(QSize(16777215, 60))
        self.button_report.setFont(font2)
        self.button_report.setStyleSheet(u"background:none;\n"
"border:none;\n"
"color: rgba(255, 255, 255, 180);")
        icon8 = QIcon()
        icon8.addFile(u"../assets/icons/report.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_report.setIcon(icon8)
        self.button_report.setIconSize(QSize(30, 30))

        self.verticalLayout_3.addWidget(self.frame_performance)

        self.frame_wifi_protection = QFrame(self.toggle_frame_left)
        self.frame_wifi_protection.setObjectName(u"frame_wifi_protection")
        self.frame_wifi_protection.setMaximumSize(QSize(16777215, 60))
        self.frame_wifi_protection.setStyleSheet(u"QFrame{\n"
"	border-radius: 0px;\n"
"}\n"
"QFrame:hover{\n"
"	background-color: rgb(55, 62, 76);\n"
"	border:2px solid rgba(0, 159, 238, 140);\n"
"	border-radius:5px;\n"
"}")
        self.frame_wifi_protection.setFrameShape(QFrame.StyledPanel)
        self.frame_wifi_protection.setFrameShadow(QFrame.Raised)
        self.button_about = QPushButton(self.frame_wifi_protection)
        self.button_about.setObjectName(u"button_about")
        self.button_about.setGeometry(QRect(0, 0, 251, 60))
        self.button_about.setMinimumSize(QSize(70, 60))
        self.button_about.setMaximumSize(QSize(16777215, 60))
        self.button_about.setFont(font2)
        self.button_about.setStyleSheet(u"background:none;\n"
"border:none;\n"
"color: rgba(255, 255, 255, 180);")
        icon9 = QIcon()
        icon9.addFile(u"../assets/icons/about.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_about.setIcon(icon9)
        self.button_about.setIconSize(QSize(30, 30))

        self.verticalLayout_3.addWidget(self.frame_wifi_protection)

        self.frame_driver_protection_2 = QFrame(self.toggle_frame_left)
        self.frame_driver_protection_2.setObjectName(u"frame_driver_protection_2")
        self.frame_driver_protection_2.setFrameShape(QFrame.StyledPanel)
        self.frame_driver_protection_2.setFrameShadow(QFrame.Raised)

        self.verticalLayout_3.addWidget(self.frame_driver_protection_2)

        self.frame_settings = QFrame(self.toggle_frame_left)
        self.frame_settings.setObjectName(u"frame_settings")
        self.frame_settings.setMaximumSize(QSize(16777215, 60))
        self.frame_settings.setStyleSheet(u"QFrame{\n"
"	border-radius: 0px;\n"
"}\n"
"QFrame:hover{\n"
"	background-color: rgb(55, 62, 76);\n"
"	border:2px solid rgba(0, 159, 238, 140);\n"
"	border-radius:5px;\n"
"}")
        self.frame_settings.setFrameShape(QFrame.StyledPanel)
        self.frame_settings.setFrameShadow(QFrame.Raised)
        self.button_settings = QPushButton(self.frame_settings)
        self.button_settings.setObjectName(u"button_settings")
        self.button_settings.setGeometry(QRect(0, 0, 241, 60))
        self.button_settings.setMinimumSize(QSize(0, 0))
        self.button_settings.setMaximumSize(QSize(250, 60))
        self.button_settings.setFont(font2)
        self.button_settings.setStyleSheet(u"background:none;\n"
"border:none;\n"
"color: rgba(255, 255, 255, 180);")
        icon10 = QIcon()
        icon10.addFile(u"../assets/icons/settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_settings.setIcon(icon10)
        self.button_settings.setIconSize(QSize(30, 30))

        self.verticalLayout_3.addWidget(self.frame_settings)


        self.horizontalLayout_4.addWidget(self.toggle_frame_left)

        self.content_page_frame = QFrame(self.Content)
        self.content_page_frame.setObjectName(u"content_page_frame")
        self.content_page_frame.setStyleSheet(u"background-color:#2C313C;\n"
"border-radius:0px;\n"
"border-bottom-right-radius:10px;\n"
"")
        self.content_page_frame.setFrameShape(QFrame.StyledPanel)
        self.content_page_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.content_page_frame)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.content_page_frame)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"")
        self.home_page = QWidget()
        self.home_page.setObjectName(u"home_page")
        self.verticalLayout_5 = QVBoxLayout(self.home_page)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_8 = QFrame(self.home_page)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.frame_8)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_2.addWidget(self.frame)

        self.frame_3 = QFrame(self.frame_8)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(550, 0))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_3)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 50, 0, 0)
        self.frame_4 = QFrame(self.frame_3)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame_4)
        self.label.setObjectName(u"label")
        font3 = QFont()
        font3.setFamily(u"Roboto Medium")
        font3.setPointSize(22)
        self.label.setFont(font3)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(False)

        self.horizontalLayout_7.addWidget(self.label)


        self.verticalLayout_6.addWidget(self.frame_4)

        self.frame_6 = QFrame(self.frame_3)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMaximumSize(QSize(16777215, 50))
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_2 = QLabel(self.frame_6)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_9.addWidget(self.label_2)


        self.verticalLayout_6.addWidget(self.frame_6)

        self.frame_11 = QFrame(self.frame_3)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.pushButton_2 = QPushButton(self.frame_11)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMaximumSize(QSize(16777215, 250))
        self.pushButton_2.setStyleSheet(u"border:none;\n"
"background:none;")
        icon11 = QIcon()
        icon11.addFile(u"../assets/icons/data-cleansing-1024x683.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_2.setIcon(icon11)
        self.pushButton_2.setIconSize(QSize(400, 400))

        self.horizontalLayout_10.addWidget(self.pushButton_2)


        self.verticalLayout_6.addWidget(self.frame_11)

        self.frame_12 = QFrame(self.frame_3)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_11.setSpacing(30)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.frame_14 = QFrame(self.frame_12)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_11.addWidget(self.frame_14)

        self.button_open_dataset = QPushButton(self.frame_12)
        self.button_open_dataset.setObjectName(u"button_open_dataset")
        self.button_open_dataset.setMinimumSize(QSize(150, 40))
        self.button_open_dataset.setMaximumSize(QSize(150, 40))
        font4 = QFont()
        font4.setFamily(u"Roboto Medium")
        font4.setPointSize(9)
        self.button_open_dataset.setFont(font4)
        self.button_open_dataset.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_open_dataset.setStyleSheet(u"QPushButton{\n"
"	border:none;\n"
"	color: rgb(244, 244, 244);\n"
"	background-color: rgb(1, 88, 203);\n"
"	border-radius:8px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color: rgb(0, 62, 186);\n"
"}")

        self.horizontalLayout_11.addWidget(self.button_open_dataset)

        self.button_view_dashboard = QPushButton(self.frame_12)
        self.button_view_dashboard.setObjectName(u"button_view_dashboard")
        self.button_view_dashboard.setMinimumSize(QSize(150, 40))
        self.button_view_dashboard.setMaximumSize(QSize(150, 40))
        self.button_view_dashboard.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_view_dashboard.setStyleSheet(u"QPushButton{\n"
"	border:none;\n"
"	border-radius:8px;\n"
"	border: 2px solid rgb(180, 180, 180)\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color: rgb(226, 226, 226);\n"
"}")

        self.horizontalLayout_11.addWidget(self.button_view_dashboard)

        self.frame_15 = QFrame(self.frame_12)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_11.addWidget(self.frame_15)


        self.verticalLayout_6.addWidget(self.frame_12)

        self.frame_13 = QFrame(self.frame_3)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)

        self.verticalLayout_6.addWidget(self.frame_13)


        self.horizontalLayout_2.addWidget(self.frame_3)

        self.frame_2 = QFrame(self.frame_8)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_2.addWidget(self.frame_2)


        self.verticalLayout_5.addWidget(self.frame_8)

        self.stackedWidget.addWidget(self.home_page)
        self.dashboard_page = QWidget()
        self.dashboard_page.setObjectName(u"dashboard_page")
        self.horizontalLayout_12 = QHBoxLayout(self.dashboard_page)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.frame_16 = QFrame(self.dashboard_page)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.frame_16.setFrameShape(QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_16)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.frame_17 = QFrame(self.frame_16)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setMaximumSize(QSize(16777215, 60))
        self.frame_17.setFrameShape(QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_17)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(-1, 20, -1, 0)
        self.label_3 = QLabel(self.frame_17)
        self.label_3.setObjectName(u"label_3")
        font5 = QFont()
        font5.setFamily(u"Roboto Medium")
        font5.setPointSize(14)
        self.label_3.setFont(font5)
        self.label_3.setStyleSheet(u"border-radius:0px;\n"
"border-bottom:1px solid rgb(177, 177, 177);")

        self.horizontalLayout_13.addWidget(self.label_3)


        self.verticalLayout_7.addWidget(self.frame_17)

        self.frame_18 = QFrame(self.frame_16)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setMaximumSize(QSize(16777215, 50))
        self.frame_18.setFrameShape(QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_18)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(18, -1, 15, -1)
        self.dataset_label = QLabel(self.frame_18)
        self.dataset_label.setObjectName(u"dataset_label")
        self.dataset_label.setFont(font)

        self.horizontalLayout_15.addWidget(self.dataset_label)

        self.dataset_row_col_num = QLabel(self.frame_18)
        self.dataset_row_col_num.setObjectName(u"dataset_row_col_num")
        self.dataset_row_col_num.setFont(font)
        self.dataset_row_col_num.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_15.addWidget(self.dataset_row_col_num)


        self.verticalLayout_7.addWidget(self.frame_18)

        self.frame_19 = QFrame(self.frame_16)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setMaximumSize(QSize(16777215, 120))
        self.frame_19.setFrameShape(QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_19)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.frame_22 = QFrame(self.frame_19)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setMaximumSize(QSize(150, 16777215))
        self.frame_22.setFrameShape(QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_16.addWidget(self.frame_22)

        self.frame_23 = QFrame(self.frame_19)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setMinimumSize(QSize(200, 0))
        self.frame_23.setMaximumSize(QSize(16777215, 16777215))
        self.frame_23.setStyleSheet(u"QFrame{\n"
"	border:1px solid rgb(193, 193, 193);\n"
"	border-radius:10px;\n"
"}")
        self.frame_23.setFrameShape(QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame_23)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(-1, 10, -1, 5)
        self.label_6 = QLabel(self.frame_23)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font4)
        self.label_6.setStyleSheet(u"border:none;")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_10.addWidget(self.label_6)

        self.missing_value_num = QLabel(self.frame_23)
        self.missing_value_num.setObjectName(u"missing_value_num")
        font6 = QFont()
        font6.setFamily(u"Roboto Medium")
        font6.setPointSize(18)
        self.missing_value_num.setFont(font6)
        self.missing_value_num.setStyleSheet(u"border:none;\n"
"padding-top:10px;\n"
"color: rgb(63, 0, 94)")
        self.missing_value_num.setAlignment(Qt.AlignCenter)

        self.verticalLayout_10.addWidget(self.missing_value_num)

        self.missing_value_percent = QLabel(self.frame_23)
        self.missing_value_percent.setObjectName(u"missing_value_percent")
        self.missing_value_percent.setStyleSheet(u"border:none;")
        self.missing_value_percent.setAlignment(Qt.AlignCenter)

        self.verticalLayout_10.addWidget(self.missing_value_percent)


        self.horizontalLayout_16.addWidget(self.frame_23)

        self.frame_25 = QFrame(self.frame_19)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setMinimumSize(QSize(200, 0))
        self.frame_25.setMaximumSize(QSize(16777215, 16777215))
        self.frame_25.setStyleSheet(u"QFrame{\n"
"	border:1px solid rgb(193, 193, 193);\n"
"	border-radius:10px;\n"
"}")
        self.frame_25.setFrameShape(QFrame.StyledPanel)
        self.frame_25.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.frame_25)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(-1, 10, -1, 5)
        self.label_9 = QLabel(self.frame_25)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font4)
        self.label_9.setStyleSheet(u"border:none;")
        self.label_9.setAlignment(Qt.AlignCenter)

        self.verticalLayout_11.addWidget(self.label_9)

        self.duplicate_rows_num = QLabel(self.frame_25)
        self.duplicate_rows_num.setObjectName(u"duplicate_rows_num")
        self.duplicate_rows_num.setFont(font6)
        self.duplicate_rows_num.setStyleSheet(u"border:none;\n"
"padding-top:10px;\n"
"color: rgb(0, 158, 0)")
        self.duplicate_rows_num.setAlignment(Qt.AlignCenter)

        self.verticalLayout_11.addWidget(self.duplicate_rows_num)

        self.duplicate_rows_percent = QLabel(self.frame_25)
        self.duplicate_rows_percent.setObjectName(u"duplicate_rows_percent")
        self.duplicate_rows_percent.setStyleSheet(u"border:none;")
        self.duplicate_rows_percent.setAlignment(Qt.AlignCenter)

        self.verticalLayout_11.addWidget(self.duplicate_rows_percent)


        self.horizontalLayout_16.addWidget(self.frame_25)

        self.frame_26 = QFrame(self.frame_19)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setMinimumSize(QSize(200, 0))
        self.frame_26.setMaximumSize(QSize(16777215, 16777215))
        self.frame_26.setStyleSheet(u"QFrame{\n"
"	border:1px solid rgb(193, 193, 193);\n"
"	border-radius:10px;\n"
"}")
        self.frame_26.setFrameShape(QFrame.StyledPanel)
        self.frame_26.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_26)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(-1, 10, -1, 5)
        self.label_12 = QLabel(self.frame_26)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font4)
        self.label_12.setStyleSheet(u"border:none;")
        self.label_12.setAlignment(Qt.AlignCenter)

        self.verticalLayout_12.addWidget(self.label_12)

        self.outlier_num = QLabel(self.frame_26)
        self.outlier_num.setObjectName(u"outlier_num")
        self.outlier_num.setFont(font6)
        self.outlier_num.setStyleSheet(u"border:none;\n"
"padding-top:10px;\n"
"color: rgb(255, 141, 1)")
        self.outlier_num.setAlignment(Qt.AlignCenter)

        self.verticalLayout_12.addWidget(self.outlier_num)

        self.outlier_percent = QLabel(self.frame_26)
        self.outlier_percent.setObjectName(u"outlier_percent")
        self.outlier_percent.setStyleSheet(u"border:none;")
        self.outlier_percent.setAlignment(Qt.AlignCenter)

        self.verticalLayout_12.addWidget(self.outlier_percent)


        self.horizontalLayout_16.addWidget(self.frame_26)

        self.frame_27 = QFrame(self.frame_19)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setMinimumSize(QSize(200, 0))
        self.frame_27.setMaximumSize(QSize(16777215, 16777215))
        self.frame_27.setStyleSheet(u"QFrame{\n"
"	border:1px solid rgb(193, 193, 193);\n"
"	border-radius:10px;\n"
"}")
        self.frame_27.setFrameShape(QFrame.StyledPanel)
        self.frame_27.setFrameShadow(QFrame.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.frame_27)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(-1, 10, -1, 5)
        self.label_15 = QLabel(self.frame_27)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font4)
        self.label_15.setStyleSheet(u"border:none;")
        self.label_15.setAlignment(Qt.AlignCenter)

        self.verticalLayout_13.addWidget(self.label_15)

        self.data_quality_score = QLabel(self.frame_27)
        self.data_quality_score.setObjectName(u"data_quality_score")
        self.data_quality_score.setFont(font6)
        self.data_quality_score.setStyleSheet(u"border:none;\n"
"padding-top:10px;\n"
"color:  rgb(0, 158, 0)")
        self.data_quality_score.setAlignment(Qt.AlignCenter)

        self.verticalLayout_13.addWidget(self.data_quality_score)

        self.data_quality_status = QLabel(self.frame_27)
        self.data_quality_status.setObjectName(u"data_quality_status")
        font7 = QFont()
        font7.setFamily(u"Roboto Medium")
        self.data_quality_status.setFont(font7)
        self.data_quality_status.setStyleSheet(u"border:none;\n"
"color: rgb(0, 170, 127);")
        self.data_quality_status.setAlignment(Qt.AlignCenter)

        self.verticalLayout_13.addWidget(self.data_quality_status)


        self.horizontalLayout_16.addWidget(self.frame_27)

        self.frame_28 = QFrame(self.frame_19)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setMaximumSize(QSize(150, 16777215))
        self.frame_28.setFrameShape(QFrame.StyledPanel)
        self.frame_28.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_16.addWidget(self.frame_28)


        self.verticalLayout_7.addWidget(self.frame_19)

        self.frame_20 = QFrame(self.frame_16)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setMinimumSize(QSize(0, 250))
        self.frame_20.setFrameShape(QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_20)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, -1, 0, -1)
        self.frame_29 = QFrame(self.frame_20)
        self.frame_29.setObjectName(u"frame_29")
        self.frame_29.setMaximumSize(QSize(150, 16777215))
        self.frame_29.setFrameShape(QFrame.StyledPanel)
        self.frame_29.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_17.addWidget(self.frame_29)

        self.bar_frame = QFrame(self.frame_20)
        self.bar_frame.setObjectName(u"bar_frame")
        self.bar_frame.setMinimumSize(QSize(450, 0))
        self.bar_frame.setStyleSheet(u"QFrame{\n"
"	border:1px solid rgb(193, 193, 193);\n"
"	border-radius:10px;\n"
"}")
        self.bar_frame.setFrameShape(QFrame.StyledPanel)
        self.bar_frame.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_17.addWidget(self.bar_frame)

        self.pie_chart_frame = QFrame(self.frame_20)
        self.pie_chart_frame.setObjectName(u"pie_chart_frame")
        self.pie_chart_frame.setMinimumSize(QSize(365, 0))
        self.pie_chart_frame.setMaximumSize(QSize(16777215, 16777215))
        self.pie_chart_frame.setStyleSheet(u"QFrame{\n"
"	border:1px solid rgb(193, 193, 193);\n"
"	border-radius:10px;\n"
"}")
        self.pie_chart_frame.setFrameShape(QFrame.StyledPanel)
        self.pie_chart_frame.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_17.addWidget(self.pie_chart_frame)

        self.frame_32 = QFrame(self.frame_20)
        self.frame_32.setObjectName(u"frame_32")
        self.frame_32.setMaximumSize(QSize(150, 16777215))
        self.frame_32.setFrameShape(QFrame.StyledPanel)
        self.frame_32.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_17.addWidget(self.frame_32)


        self.verticalLayout_7.addWidget(self.frame_20)

        self.frame_21 = QFrame(self.frame_16)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setFrameShape(QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QFrame.Raised)

        self.verticalLayout_7.addWidget(self.frame_21)


        self.horizontalLayout_12.addWidget(self.frame_16)

        self.stackedWidget.addWidget(self.dashboard_page)
        self.cleaning_page = QWidget()
        self.cleaning_page.setObjectName(u"cleaning_page")
        self.stackedWidget.addWidget(self.cleaning_page)
        self.report_page = QWidget()
        self.report_page.setObjectName(u"report_page")
        self.verticalLayout_8 = QVBoxLayout(self.report_page)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.frame_5 = QFrame(self.report_page)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_5)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.frame_7 = QFrame(self.frame_5)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMaximumSize(QSize(16777215, 16777215))
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.frame_7)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget_2 = QStackedWidget(self.frame_7)
        self.stackedWidget_2.setObjectName(u"stackedWidget_2")
        self.vulnerabilitiesFoundPage = QWidget()
        self.vulnerabilitiesFoundPage.setObjectName(u"vulnerabilitiesFoundPage")
        self.verticalLayout_17 = QVBoxLayout(self.vulnerabilitiesFoundPage)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.frame_58 = QFrame(self.vulnerabilitiesFoundPage)
        self.frame_58.setObjectName(u"frame_58")
        self.frame_58.setFrameShape(QFrame.StyledPanel)
        self.frame_58.setFrameShadow(QFrame.Raised)
        self.verticalLayout_30 = QVBoxLayout(self.frame_58)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.frame_59 = QFrame(self.frame_58)
        self.frame_59.setObjectName(u"frame_59")
        self.frame_59.setMaximumSize(QSize(16777215, 465))
        self.frame_59.setFrameShape(QFrame.StyledPanel)
        self.frame_59.setFrameShadow(QFrame.Raised)
        self.verticalLayout_29 = QVBoxLayout(self.frame_59)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.verticalLayout_29.setContentsMargins(100, 20, 100, -1)
        self.foundVulnerabilities = QTextEdit(self.frame_59)
        self.foundVulnerabilities.setObjectName(u"foundVulnerabilities")
        font8 = QFont()
        font8.setFamily(u"Roboto")
        font8.setPointSize(14)
        self.foundVulnerabilities.setFont(font8)
        self.foundVulnerabilities.setStyleSheet(u"color: rgb(192, 192, 197);")
        self.foundVulnerabilities.setReadOnly(True)
        self.foundVulnerabilities.setTextInteractionFlags(Qt.NoTextInteraction)

        self.verticalLayout_29.addWidget(self.foundVulnerabilities)


        self.verticalLayout_30.addWidget(self.frame_59)

        self.frame_60 = QFrame(self.frame_58)
        self.frame_60.setObjectName(u"frame_60")
        self.frame_60.setMinimumSize(QSize(0, 100))
        self.frame_60.setFrameShape(QFrame.StyledPanel)
        self.frame_60.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_29 = QHBoxLayout(self.frame_60)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.frame_61 = QFrame(self.frame_60)
        self.frame_61.setObjectName(u"frame_61")
        self.frame_61.setMinimumSize(QSize(500, 0))
        self.frame_61.setMaximumSize(QSize(16777215, 70))
        self.frame_61.setFrameShape(QFrame.StyledPanel)
        self.frame_61.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_61)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.buttonResolveNow_2 = QPushButton(self.frame_61)
        self.buttonResolveNow_2.setObjectName(u"buttonResolveNow_2")
        self.buttonResolveNow_2.setMinimumSize(QSize(0, 45))
        self.buttonResolveNow_2.setMaximumSize(QSize(200, 16777215))
        font9 = QFont()
        font9.setFamily(u"Roboto")
        font9.setPointSize(11)
        self.buttonResolveNow_2.setFont(font9)
        self.buttonResolveNow_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.buttonResolveNow_2.setStyleSheet(u"QPushButton{\n"
"	color:rgba(255, 255, 255, 180);\n"
"	background-color:rgb(27, 138, 58);\n"
"	border-radius: 6px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgba(27, 138, 58, 210);\n"
"}")

        self.horizontalLayout_14.addWidget(self.buttonResolveNow_2)

        self.buttonSkip_2 = QPushButton(self.frame_61)
        self.buttonSkip_2.setObjectName(u"buttonSkip_2")
        self.buttonSkip_2.setMinimumSize(QSize(0, 45))
        self.buttonSkip_2.setMaximumSize(QSize(200, 16777215))
        self.buttonSkip_2.setFont(font9)
        self.buttonSkip_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.buttonSkip_2.setStyleSheet(u"QPushButton{\n"
"	background-color:rgba(255, 255, 255, 180);\n"
"	color:rgba(0, 0, 0, 180);\n"
"	border-radius: 6px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color:rgba(255, 255, 255, 150);\n"
"}")

        self.horizontalLayout_14.addWidget(self.buttonSkip_2)


        self.horizontalLayout_29.addWidget(self.frame_61, 0, Qt.AlignHCenter)


        self.verticalLayout_30.addWidget(self.frame_60)


        self.verticalLayout_17.addWidget(self.frame_58)

        self.stackedWidget_2.addWidget(self.vulnerabilitiesFoundPage)
        self.checkForVulnerabilitiesPage = QWidget()
        self.checkForVulnerabilitiesPage.setObjectName(u"checkForVulnerabilitiesPage")
        self.verticalLayout_15 = QVBoxLayout(self.checkForVulnerabilitiesPage)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.frame_24 = QFrame(self.checkForVulnerabilitiesPage)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setFrameShape(QFrame.StyledPanel)
        self.frame_24.setFrameShadow(QFrame.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.frame_24)
        self.verticalLayout_16.setSpacing(10)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(-1, 0, -1, -1)

        self.verticalLayout_15.addWidget(self.frame_24)

        self.stackedWidget_2.addWidget(self.checkForVulnerabilitiesPage)

        self.verticalLayout_14.addWidget(self.stackedWidget_2)


        self.verticalLayout_9.addWidget(self.frame_7)


        self.verticalLayout_8.addWidget(self.frame_5)

        self.stackedWidget.addWidget(self.report_page)
        self.about_page = QWidget()
        self.about_page.setObjectName(u"about_page")
        self.stackedWidget.addWidget(self.about_page)
        self.settings_page = QWidget()
        self.settings_page.setObjectName(u"settings_page")
        self.verticalLayout_4 = QVBoxLayout(self.settings_page)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_48 = QFrame(self.settings_page)
        self.frame_48.setObjectName(u"frame_48")
        self.frame_48.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.frame_48.setFrameShape(QFrame.StyledPanel)
        self.frame_48.setFrameShadow(QFrame.Raised)
        self.verticalLayout_18 = QVBoxLayout(self.frame_48)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.frame_33 = QFrame(self.frame_48)
        self.frame_33.setObjectName(u"frame_33")
        self.frame_33.setMaximumSize(QSize(16777215, 60))
        self.frame_33.setFrameShape(QFrame.StyledPanel)
        self.frame_33.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_33)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(25, -1, -1, -1)
        self.label_18 = QLabel(self.frame_33)
        self.label_18.setObjectName(u"label_18")
        font10 = QFont()
        font10.setFamily(u"Roboto Medium")
        font10.setPointSize(16)
        self.label_18.setFont(font10)

        self.horizontalLayout_18.addWidget(self.label_18)


        self.verticalLayout_18.addWidget(self.frame_33)

        self.frame_35 = QFrame(self.frame_48)
        self.frame_35.setObjectName(u"frame_35")
        self.frame_35.setFrameShape(QFrame.StyledPanel)
        self.frame_35.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.frame_35)
        self.horizontalLayout_19.setSpacing(0)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.frame_34 = QFrame(self.frame_35)
        self.frame_34.setObjectName(u"frame_34")
        self.frame_34.setMaximumSize(QSize(350, 16777215))
        self.frame_34.setFrameShape(QFrame.StyledPanel)
        self.frame_34.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_19.addWidget(self.frame_34)

        self.frame_30 = QFrame(self.frame_35)
        self.frame_30.setObjectName(u"frame_30")
        self.frame_30.setMinimumSize(QSize(700, 0))
        self.frame_30.setStyleSheet(u"")
        self.frame_30.setFrameShape(QFrame.StyledPanel)
        self.frame_30.setFrameShadow(QFrame.Raised)
        self.verticalLayout_19 = QVBoxLayout(self.frame_30)
        self.verticalLayout_19.setSpacing(15)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.verticalLayout_19.setContentsMargins(0, 15, 0, 0)
        self.frame_37 = QFrame(self.frame_30)
        self.frame_37.setObjectName(u"frame_37")
        self.frame_37.setMinimumSize(QSize(0, 170))
        self.frame_37.setMaximumSize(QSize(16777215, 170))
        self.frame_37.setStyleSheet(u"QFrame{\n"
"	border:1px solid rgb(193, 193, 193);\n"
"	border-radius:10px;\n"
"	background-color: rgb(253, 253, 253)\n"
"}")
        self.frame_37.setFrameShape(QFrame.StyledPanel)
        self.frame_37.setFrameShadow(QFrame.Raised)
        self.verticalLayout_20 = QVBoxLayout(self.frame_37)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(-1, -1, 15, 20)
        self.frame_41 = QFrame(self.frame_37)
        self.frame_41.setObjectName(u"frame_41")
        self.frame_41.setStyleSheet(u"border:none;\n"
"border-radius:0px;")
        self.frame_41.setFrameShape(QFrame.StyledPanel)
        self.frame_41.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.frame_41)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_19 = QLabel(self.frame_41)
        self.label_19.setObjectName(u"label_19")
        font11 = QFont()
        font11.setFamily(u"Roboto Medium")
        font11.setPointSize(11)
        self.label_19.setFont(font11)
        self.label_19.setStyleSheet(u"")

        self.horizontalLayout_20.addWidget(self.label_19)


        self.verticalLayout_20.addWidget(self.frame_41)

        self.frame_40 = QFrame(self.frame_37)
        self.frame_40.setObjectName(u"frame_40")
        self.frame_40.setMinimumSize(QSize(0, 45))
        font12 = QFont()
        font12.setFamily(u"Segoe UI Emoji")
        self.frame_40.setFont(font12)
        self.frame_40.setStyleSheet(u"border:none;\n"
"border-radius:0px;")
        self.frame_40.setFrameShape(QFrame.StyledPanel)
        self.frame_40.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_21 = QHBoxLayout(self.frame_40)
        self.horizontalLayout_21.setSpacing(15)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(15, 0, 0, 0)
        self.label_20 = QLabel(self.frame_40)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setMinimumSize(QSize(240, 0))
        self.label_20.setMaximumSize(QSize(240, 16777215))
        self.label_20.setFont(font2)

        self.horizontalLayout_21.addWidget(self.label_20)

        self.theme_comboBox = QComboBox(self.frame_40)
        self.theme_comboBox.addItem("")
        self.theme_comboBox.addItem("")
        self.theme_comboBox.setObjectName(u"theme_comboBox")
        self.theme_comboBox.setMinimumSize(QSize(0, 42))
        self.theme_comboBox.setMaximumSize(QSize(200, 16777215))
        font13 = QFont()
        font13.setFamily(u"Roboto")
        self.theme_comboBox.setFont(font13)
        self.theme_comboBox.setCursor(QCursor(Qt.PointingHandCursor))
        self.theme_comboBox.setStyleSheet(u"QComboBox {\n"
"    background: white;\n"
"    border: 2px solid  rgb(199, 214, 255);\n"
"    border-radius: 8px;\n"
"\n"
"    padding-left: 16px;\n"
"    padding-right: 35px;\n"
"    min-height: 38px;\n"
"\n"
"    font-size: 16px;\n"
"    color: #2B2B2B;\n"
"\n"
"    outline: none;\n"
"}\n"
"\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid #D8D8D8;\n"
"}\n"
"\n"
"\n"
"QComboBox:focus {\n"
"    border: 1px solid #D0D0D0;\n"
"}\n"
"\n"
"\n"
"/* Arrow button area */\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    width: 28px;\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"}\n"
"\n"
"\n"
"/* Arrow icon */\n"
"QComboBox::down-arrow {\n"
"    image: url(../assests/arrow.png);   /* your arrow icon */\n"
"    width: 12px;\n"
"    height: 12px;\n"
"}\n"
"\n"
"\n"
"/* Popup list */\n"
"QComboBox QAbstractItemView {\n"
"    background: white;\n"
"\n"
"    border: 1px solid #EAEAEA;\n"
"    border-radius: 5px;\n"
"\n"
"    padding: 8px;\n"
"\n"
"    outline: none;\n"
"\n"
" "
                        "   selection-background-color: rgb(0, 170, 255);\n"
"    selection-color: #2B2B2B;\n"
"\n"
"    font-size: 16px;\n"
"\n"
"}\n"
"\n"
"\n"
"/* Each item */\n"
"QComboBox QAbstractItemView::item {\n"
"    min-height: 50px;\n"
"\n"
"    border-radius: 8px;\n"
"\n"
"    padding-left: 14px;\n"
"    padding-right: 14px;\n"
"\n"
"    margin: 2px;\n"
"}\n"
"\n"
"\n"
"/* Hover item */\n"
"QComboBox QAbstractItemView::item:hover {\n"
"    background: #F7F7F7;\n"
"}\n"
"\n"
"\n"
"/* Selected item */\n"
"QComboBox QAbstractItemView::item:selected {\n"
"    background: #F5F5F5;\n"
"\n"
"    border-left: 4px solid #0078FF;\n"
"\n"
"    padding-left: 10px;\n"
"}\n"
"")

        self.horizontalLayout_21.addWidget(self.theme_comboBox)

        self.frame_46 = QFrame(self.frame_40)
        self.frame_46.setObjectName(u"frame_46")
        self.frame_46.setFrameShape(QFrame.StyledPanel)
        self.frame_46.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_21.addWidget(self.frame_46)


        self.verticalLayout_20.addWidget(self.frame_40)

        self.frame_42 = QFrame(self.frame_37)
        self.frame_42.setObjectName(u"frame_42")
        self.frame_42.setMinimumSize(QSize(0, 45))
        self.frame_42.setStyleSheet(u"border:none;\n"
"border-radius:0px;")
        self.frame_42.setFrameShape(QFrame.StyledPanel)
        self.frame_42.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_22 = QHBoxLayout(self.frame_42)
        self.horizontalLayout_22.setSpacing(15)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(15, 0, 0, 0)
        self.label_21 = QLabel(self.frame_42)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setMaximumSize(QSize(240, 35))
        self.label_21.setFont(font2)

        self.horizontalLayout_22.addWidget(self.label_21)

        self.frame_47 = QFrame(self.frame_42)
        self.frame_47.setObjectName(u"frame_47")
        self.frame_47.setMinimumSize(QSize(0, 0))
        self.frame_47.setMaximumSize(QSize(16777215, 16777215))
        self.frame_47.setFrameShape(QFrame.StyledPanel)
        self.frame_47.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_23 = QHBoxLayout(self.frame_47)
        self.horizontalLayout_23.setSpacing(0)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(0, 0, 0, 5)
        self.path_textEdit = QTextEdit(self.frame_47)
        self.path_textEdit.setObjectName(u"path_textEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.path_textEdit.sizePolicy().hasHeightForWidth())
        self.path_textEdit.setSizePolicy(sizePolicy)
        self.path_textEdit.setMinimumSize(QSize(0, 40))
        self.path_textEdit.setMaximumSize(QSize(16777215, 35))
        self.path_textEdit.setFont(font2)
        self.path_textEdit.setStyleSheet(u"QTextEdit{\n"
"	border:2px solid rgb(199, 214, 255);\n"
"	border-radius:8px;\n"
"	padding-top:5px;\n"
"}\n"
"QTextEdit:hover{\n"
"	background-color: rgb(247, 247, 247)\n"
"}")
        self.path_textEdit.setReadOnly(True)

        self.horizontalLayout_23.addWidget(self.path_textEdit)


        self.horizontalLayout_22.addWidget(self.frame_47)

        self.button_browse = QPushButton(self.frame_42)
        self.button_browse.setObjectName(u"button_browse")
        self.button_browse.setMinimumSize(QSize(0, 40))
        self.button_browse.setMaximumSize(QSize(100, 16777215))
        self.button_browse.setFont(font2)
        self.button_browse.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_browse.setStyleSheet(u"QPushButton{\n"
"	border:2px solid rgb(199, 214, 255);\n"
"	border-radius:8px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(247, 247, 247)\n"
"}")

        self.horizontalLayout_22.addWidget(self.button_browse)


        self.verticalLayout_20.addWidget(self.frame_42)


        self.verticalLayout_19.addWidget(self.frame_37)

        self.frame_36 = QFrame(self.frame_30)
        self.frame_36.setObjectName(u"frame_36")
        self.frame_36.setMinimumSize(QSize(0, 170))
        self.frame_36.setMaximumSize(QSize(16777215, 170))
        self.frame_36.setStyleSheet(u"QFrame{\n"
"	border:1px solid rgb(193, 193, 193);\n"
"	border-radius:10px;\n"
"	background-color: rgb(253, 253, 253)\n"
"}")
        self.frame_36.setFrameShape(QFrame.StyledPanel)
        self.frame_36.setFrameShadow(QFrame.Raised)
        self.verticalLayout_21 = QVBoxLayout(self.frame_36)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(-1, -1, -1, 25)
        self.frame_44 = QFrame(self.frame_36)
        self.frame_44.setObjectName(u"frame_44")
        self.frame_44.setStyleSheet(u"border:none;\n"
"border-radius:0px;")
        self.frame_44.setFrameShape(QFrame.StyledPanel)
        self.frame_44.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_24 = QHBoxLayout(self.frame_44)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.label_22 = QLabel(self.frame_44)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font11)
        self.label_22.setStyleSheet(u"")

        self.horizontalLayout_24.addWidget(self.label_22)


        self.verticalLayout_21.addWidget(self.frame_44)

        self.frame_45 = QFrame(self.frame_36)
        self.frame_45.setObjectName(u"frame_45")
        self.frame_45.setStyleSheet(u"border:none;\n"
"border-radius:0px;")
        self.frame_45.setFrameShape(QFrame.StyledPanel)
        self.frame_45.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_25 = QHBoxLayout(self.frame_45)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(-1, 0, -1, -1)
        self.settings_report_checkBox1 = QCheckBox(self.frame_45)
        self.settings_report_checkBox1.setObjectName(u"settings_report_checkBox1")
        self.settings_report_checkBox1.setMinimumSize(QSize(0, 40))
        self.settings_report_checkBox1.setFont(font2)

        self.horizontalLayout_25.addWidget(self.settings_report_checkBox1)


        self.verticalLayout_21.addWidget(self.frame_45)

        self.frame_43 = QFrame(self.frame_36)
        self.frame_43.setObjectName(u"frame_43")
        self.frame_43.setMinimumSize(QSize(0, 40))
        self.frame_43.setStyleSheet(u"border:none;\n"
"border-radius:0px;")
        self.frame_43.setFrameShape(QFrame.StyledPanel)
        self.frame_43.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_26 = QHBoxLayout(self.frame_43)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setContentsMargins(-1, 0, -1, -1)
        self.settings_report_checkBox2 = QCheckBox(self.frame_43)
        self.settings_report_checkBox2.setObjectName(u"settings_report_checkBox2")
        self.settings_report_checkBox2.setMinimumSize(QSize(0, 40))
        self.settings_report_checkBox2.setFont(font2)

        self.horizontalLayout_26.addWidget(self.settings_report_checkBox2)


        self.verticalLayout_21.addWidget(self.frame_43)


        self.verticalLayout_19.addWidget(self.frame_36)

        self.frame_39 = QFrame(self.frame_30)
        self.frame_39.setObjectName(u"frame_39")
        self.frame_39.setMaximumSize(QSize(16777215, 80))
        self.frame_39.setFrameShape(QFrame.StyledPanel)
        self.frame_39.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_27 = QHBoxLayout(self.frame_39)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(-1, 0, -1, -1)
        self.frame_49 = QFrame(self.frame_39)
        self.frame_49.setObjectName(u"frame_49")
        self.frame_49.setFrameShape(QFrame.StyledPanel)
        self.frame_49.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_27.addWidget(self.frame_49)

        self.button_save_settings = QPushButton(self.frame_39)
        self.button_save_settings.setObjectName(u"button_save_settings")
        self.button_save_settings.setMinimumSize(QSize(0, 40))
        self.button_save_settings.setMaximumSize(QSize(150, 16777215))
        self.button_save_settings.setFont(font2)
        self.button_save_settings.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_save_settings.setStyleSheet(u"QPushButton{\n"
"	border:none;\n"
"	color: rgb(244, 244, 244);\n"
"	background-color: rgb(1, 88, 203);\n"
"	border-radius:8px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color: rgb(0, 62, 186);\n"
"}")

        self.horizontalLayout_27.addWidget(self.button_save_settings)


        self.verticalLayout_19.addWidget(self.frame_39)

        self.frame_38 = QFrame(self.frame_30)
        self.frame_38.setObjectName(u"frame_38")
        self.frame_38.setFrameShape(QFrame.StyledPanel)
        self.frame_38.setFrameShadow(QFrame.Raised)

        self.verticalLayout_19.addWidget(self.frame_38)


        self.horizontalLayout_19.addWidget(self.frame_30)

        self.frame_31 = QFrame(self.frame_35)
        self.frame_31.setObjectName(u"frame_31")
        self.frame_31.setMaximumSize(QSize(350, 16777215))
        self.frame_31.setFrameShape(QFrame.StyledPanel)
        self.frame_31.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_19.addWidget(self.frame_31)


        self.verticalLayout_18.addWidget(self.frame_35)


        self.verticalLayout_4.addWidget(self.frame_48)

        self.stackedWidget.addWidget(self.settings_page)

        self.horizontalLayout_6.addWidget(self.stackedWidget)


        self.horizontalLayout_4.addWidget(self.content_page_frame)


        self.verticalLayout_2.addWidget(self.Content)


        self.verticalLayout.addWidget(self.drop_shadow_frame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText("")
        self.top_bar_label.setText(QCoreApplication.translate("MainWindow", u"Automated Data Cleaning & Profiling Tool", None))
        self.button_minimize.setText("")
        self.button_restore.setText("")
        self.button_close.setText("")
        self.button_toggle.setText("")
        self.button_home.setText(QCoreApplication.translate("MainWindow", u"      Home                     ", None))
        self.button_dashboard.setText(QCoreApplication.translate("MainWindow", u"      Dashboard              ", None))
        self.button_cleaning.setText(QCoreApplication.translate("MainWindow", u"      Cleaning                  ", None))
        self.button_report.setText(QCoreApplication.translate("MainWindow", u"      Report                    ", None))
        self.button_about.setText(QCoreApplication.translate("MainWindow", u"      About                        ", None))
        self.button_settings.setText(QCoreApplication.translate("MainWindow", u"      Settings                   ", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Automated Data Cleaning &<br>Profiling Tool", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Clean, profile and preprocess your datasets automatically ", None))
        self.pushButton_2.setText("")
        self.button_open_dataset.setText(QCoreApplication.translate("MainWindow", u"Open Dataset", None))
        self.button_view_dashboard.setText(QCoreApplication.translate("MainWindow", u"View Dashboard", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.dataset_label.setText(QCoreApplication.translate("MainWindow", u"Dataset: sample_data.csv", None))
        self.dataset_row_col_num.setText(QCoreApplication.translate("MainWindow", u"Rows: 1000     Columns 12", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Missing Values", None))
        self.missing_value_num.setText(QCoreApplication.translate("MainWindow", u"120", None))
        self.missing_value_percent.setText(QCoreApplication.translate("MainWindow", u"(1.20%)", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Duplicate Rows", None))
        self.duplicate_rows_num.setText(QCoreApplication.translate("MainWindow", u"15", None))
        self.duplicate_rows_percent.setText(QCoreApplication.translate("MainWindow", u"(1.50%)", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Outlier Detected", None))
        self.outlier_num.setText(QCoreApplication.translate("MainWindow", u"34", None))
        self.outlier_percent.setText(QCoreApplication.translate("MainWindow", u"(1.20%)", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Data Quality Score", None))
        self.data_quality_score.setText(QCoreApplication.translate("MainWindow", u"87%", None))
        self.data_quality_status.setText(QCoreApplication.translate("MainWindow", u"Good", None))
        self.foundVulnerabilities.setDocumentTitle("")
        self.foundVulnerabilities.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Roboto'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.foundVulnerabilities.setPlaceholderText("")
        self.buttonResolveNow_2.setText(QCoreApplication.translate("MainWindow", u"Resolve Now", None))
        self.buttonSkip_2.setText(QCoreApplication.translate("MainWindow", u"Skip", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"General", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Theme", None))
        self.theme_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Light", None))
        self.theme_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Dark", None))

        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Default Save Location", None))
        self.path_textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Roboto'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:7.8pt;\"><br /></p></body></html>", None))
        self.button_browse.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Reports", None))
        self.settings_report_checkBox1.setText(QCoreApplication.translate("MainWindow", u"Include Data profile in Report", None))
        self.settings_report_checkBox2.setText(QCoreApplication.translate("MainWindow", u"Include charts in Report", None))
        self.button_save_settings.setText(QCoreApplication.translate("MainWindow", u"Save Settings", None))
    # retranslateUi

