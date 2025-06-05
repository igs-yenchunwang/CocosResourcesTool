import sys
import os
import json
import subprocess
from common.ToolSetting import Setting
from common.function import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

WINDOWS_WIDTH = 800
WINDOWS_HEIGHT = 600

class ChangeColor(QWidget):
	def __init__(self):
		super().__init__()

		self.init_var()

		# 創建UI們
		self.create_ui()

		# 初始化應用程式視窗排版
		self.init_ui()

		# 載入存檔設定
		self.load_setting()

		self.Show()

	def Show(self):
		self.show()

	def Hide(self):
		self.hide()
	
	def init_var(self):
		pass

	def create_ui(self):
		self.path_label = QLabel('csd資料夾路徑:')
		self.path_input = MLineEdit()

		self.info_label = QLabel('轉換的顏色:')
		self.add_new_block_btn = QPushButton('+新增')
		self.add_new_block_btn.clicked.connect(self.add_more_color_setting)
		self.add_new_block_btn.setFixedWidth(50)

		self.log_label = QLabel('LOG:')
		self.log_text_edit = QTextEdit()
		self.log_text_edit.setReadOnly(True)

		self.start_compress = QPushButton('開始轉換')
		self.start_compress.clicked.connect(self.start_change_color)
		self.start_compress.setFixedHeight(50)
		self.start_compress.setFixedWidth(150)

	def init_ui(self):
		self.color_setting = QVBoxLayout()
		add_layer = QVBoxLayout()
		add_layer.addWidget(self.add_new_block_btn)
		add_layer.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

		setting_layer = QVBoxLayout()
		setting_layer.addWidget(self.path_label)
		setting_layer.addWidget(self.path_input)
		setting_layer.addWidget(self.info_label)
		setting_layer.addLayout(self.color_setting)	
		spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
		setting_layer.addLayout(add_layer)	
		setting_layer.addItem(spacerItem)
		setting_layer.addWidget(self.start_compress)	

		log_layer = QVBoxLayout()
		log_layer.addWidget(self.log_label)
		log_layer.addWidget(self.log_text_edit)

		main_layer = QHBoxLayout()
		main_layer.addLayout(setting_layer, 2)
		main_layer.addLayout(log_layer, 1)

		# 設定視窗佈局
		self.setLayout(main_layer)

		# 設定視窗屬性
		self.setWindowTitle('批次換色')
		self.setGeometry(100, 100, WINDOWS_WIDTH, WINDOWS_HEIGHT)

	def start_change_color(self):
		pass

	def add_more_color_setting(self):
		newLayer = QHBoxLayout()
		before_color_hashTag_label = QLabel('#')
		before_color_hax_input = MLineEdit()
		before_color_red_label = QLabel('R')
		before_color_red_input = MLineEdit()
		before_color_red_input.setFixedWidth(30)
		before_color_green_label = QLabel('G')
		before_color_green_input = MLineEdit()
		before_color_green_input.setFixedWidth(30)
		before_color_blue_label = QLabel('B')
		before_color_blue_input = MLineEdit()
		before_color_blue_input.setFixedWidth(30)

		color_to = QLabel('-->')

		after_color_hashTag_label = QLabel('#')
		after_color_hax_input = MLineEdit()
		after_color_red_label = QLabel('R')
		after_color_red_input = MLineEdit()
		after_color_red_input.setFixedWidth(30)
		after_color_green_label = QLabel('G')
		after_color_green_input = MLineEdit()
		after_color_green_input.setFixedWidth(30)
		after_color_blue_label = QLabel('B')
		after_color_blue_input = MLineEdit()
		after_color_blue_input.setFixedWidth(30)

		newLayer.addWidget(before_color_hashTag_label)
		newLayer.addWidget(before_color_hax_input)
		newLayer.addWidget(before_color_red_label)
		newLayer.addWidget(before_color_red_input)
		newLayer.addWidget(before_color_green_label)
		newLayer.addWidget(before_color_green_input)
		newLayer.addWidget(before_color_blue_label)
		newLayer.addWidget(before_color_blue_input)
		newLayer.addWidget(color_to)
		newLayer.addWidget(after_color_hashTag_label)
		newLayer.addWidget(after_color_hax_input)
		newLayer.addWidget(after_color_red_label)
		newLayer.addWidget(after_color_red_input)
		newLayer.addWidget(after_color_green_label)
		newLayer.addWidget(after_color_green_input)
		newLayer.addWidget(after_color_blue_label)
		newLayer.addWidget(after_color_blue_input)

		self.color_setting.addLayout(newLayer)
		pass

	def load_setting(self):
		self.m_settingMgr = Setting()
		self.m_setting = self.m_settingMgr.get_setting()

	def save_setting(self):

		self.m_settingMgr.save_setting(self.m_setting)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = ChangeColor()
	sys.exit(app.exec_())