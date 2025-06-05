import sys
import os
import json
from functools import partial

from common.ToolSetting import Setting
from common.function import *

from ImgToPlist import ImgToPlist
from FileMoveTool import FileMove
from CsdFindPath import CsdFindPath
from GUI.CompressionGUI import CompressionGUI
from GUI.SlotChange import SlotChange
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

WINDOWS_WIDTH = 500
WINDOWS_HEIGHT = 350

class ToolApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_var()
        self.init_ui()

    def init_var(self):
        self.m_plistController = None
        self.m_fileMoveController = None
        self.m_csdFindPngPath = None
        self.m_tinyPNGCompress = None
        self.m_structChange = None

    def init_ui(self):
        self.m_openFileMoveBtn  = QPushButton('檔案移動(圖片)')
        self.m_pngToPlistBtn    = QPushButton('以資料夾打包plist')
        self.m_csdFindPng       = QPushButton('csd 自動重新找路徑')
        self.m_structChangeBtn  = QPushButton('Slot 轉換工具')
        self.m_tinyCompressBtn  = QPushButton('以TinyPNG壓縮 (TrustView底下不可用)')


        # 設定按鈕的固定寬度，佔父容器寬度的60%
        button_width_percentage = 60
        parent_width = WINDOWS_WIDTH
        button_width = int(parent_width * (button_width_percentage / 100))
        
        self.m_openFileMoveBtn.setFixedWidth(button_width)
        self.m_openFileMoveBtn.clicked.connect(self.open_move_file_windows)

        self.m_pngToPlistBtn.setFixedWidth(button_width)
        self.m_pngToPlistBtn.clicked.connect(self.open_img_to_plist)

        self.m_csdFindPng.setFixedWidth(button_width)
        self.m_csdFindPng.clicked.connect(self.open_csd_find_png)

        self.m_tinyCompressBtn.setFixedWidth(button_width)
        self.m_tinyCompressBtn.clicked.connect(self.open_compress)

        self.m_structChangeBtn.setFixedWidth(button_width)
        self.m_structChangeBtn.clicked.connect(self.open_IR_to_Evo)

        # 將按鈕添加到 QVBoxLayout 中
        self.m_mainLayout = QVBoxLayout(self)
        self.m_mainLayout.addWidget(self.m_openFileMoveBtn)
        self.m_mainLayout.addWidget(self.m_pngToPlistBtn)
        self.m_mainLayout.addWidget(self.m_csdFindPng)
        self.m_mainLayout.addWidget(self.m_structChangeBtn)
        self.m_mainLayout.addWidget(self.m_tinyCompressBtn)

        self.m_mainLayout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        # 設定視窗屬性
        self.setWindowTitle('總工具')
        self.setGeometry(200, 200, WINDOWS_WIDTH, WINDOWS_HEIGHT)

        # 顯示應用程式視窗
        self.show()

    def open_IR_to_Evo(self):
        if not self.m_structChange:
            self.m_structChange = SlotChange()

        self.m_structChange.Show()

    def open_compress(self):
        if not self.m_tinyPNGCompress:
            self.m_tinyPNGCompress = CompressionGUI()

        self.m_tinyPNGCompress.Show()

    def open_csd_find_png(self):
        if not self.m_csdFindPngPath:
            self.m_csdFindPngPath = CsdFindPath()

        self.m_csdFindPngPath.Show()

    def open_img_to_plist(self):
        if not self.m_plistController:
            self.m_plistController = ImgToPlist()

        self.m_plistController.Show()

    def open_move_file_windows(self):
        if not self.m_fileMoveController:
            self.m_fileMoveController = FileMove()

        self.m_fileMoveController.Show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ToolApp()
    sys.exit(app.exec_())
