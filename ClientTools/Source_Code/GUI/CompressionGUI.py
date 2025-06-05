import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)).replace('\GUI', '')
sys.path.append(os.path.dirname(SCRIPT_DIR))

import json
import subprocess
from Source_Code.common.ToolSetting import *
from Source_Code.common.function import *
from Source_Code.compression.TinyPngCompression import Compression
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

WINDOWS_WIDTH = 800
WINDOWS_HEIGHT = 600

class CompressionGUI(QWidget):
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
		self.compressController = Compression()
		pass

	def create_ui(self):
		self.key_label = QLabel('TinyPNG key')
		self.key_input = MLineEdit()

		self.folder_label = QLabel('壓縮的圖片位置(資料夾)')
		self.folder_input = MLineEdit()
		self.folder_input.textChanged.connect(self.update_folder_list)  # 偵測文字變化

		self.folder_all_select = QPushButton('All')
		self.folder_all_select.setFixedWidth(40)
		self.folder_none_select = QPushButton('None')
		self.folder_none_select.setFixedWidth(40)
		self.folder_all_select.clicked.connect(self.enable_all_folder)
		self.folder_none_select.clicked.connect(self.disable_all_folder)
		self.folder_list = QListWidget(self)

		self.log_label = QLabel('LOG:')
		self.log_text_edit = QTextEdit()
		self.log_text_edit.setReadOnly(True)

		self.start_compress = QPushButton('開始壓縮')
		self.start_compress.clicked.connect(self.start_compress_pic)
		self.start_compress.setFixedHeight(50)
		self.start_compress.setFixedWidth(150)

	def init_ui(self):
		option_layer = QHBoxLayout()
		option_layer.addWidget(self.folder_all_select)
		option_layer.addWidget(self.folder_none_select)
		option_layer.setAlignment(Qt.AlignLeft)

		compress_layer = QVBoxLayout()
		compress_layer.addWidget(self.key_label)
		compress_layer.addWidget(self.key_input)
		compress_layer.addWidget(self.folder_label)
		compress_layer.addWidget(self.folder_input)
		compress_layer.addLayout(option_layer)
		compress_layer.addWidget(self.folder_list)
		compress_layer.addWidget(self.start_compress)

		log_layer = QVBoxLayout()
		log_layer.addWidget(self.log_label)
		log_layer.addWidget(self.log_text_edit)

		main_layer = QHBoxLayout()
		main_layer.addLayout(compress_layer, 2)
		main_layer.addLayout(log_layer, 1)

		# 設定視窗佈局
		self.setLayout(main_layer)

		# 設定視窗屬性
		self.setWindowTitle('壓縮工具')
		self.setGeometry(100, 100, WINDOWS_WIDTH, WINDOWS_HEIGHT)

	def start_compress_pic(self):
		log_message = f'需要一段時間 請稍後......\n'
		self.log_text_edit.append(log_message)
		QApplication.processEvents()

		picsList = self.get_all_select_folder()
		picsPathList = []
		for file in picsList:
			picsPathList.append( os.path.join(self.folder_input.text(),file).replace('\\', '/') )
		
		self.compressController.SetKey(self.key_input.text())

		for picPath in picsPathList:
			res = self.compressController.GetCompressionRes(picPath)
			if res == "":
				log_message = f'壓縮失敗 可能因為在TrustView底下\n'
				self.log_text_edit.append(log_message)
				QApplication.processEvents()
				break
			url = self.compressController.ParseUrlFromRes(res)
			if url == "":
				log_message = f'壓縮失敗 {picPath}\n'
				self.log_text_edit.append(log_message)
				QApplication.processEvents()
				break

			self.compressController.DownloadPicWithUrl(url, picPath)
			log_message = f'已壓縮{picPath}\n'
			self.log_text_edit.append(log_message)
			QApplication.processEvents()

		log_message = f'轉換結束!!!\n'
		self.log_text_edit.append(log_message)
		QApplication.processEvents()

	def update_folder_list(self):
		path = self.folder_input.text()

		if os.path.isdir(path):
			self.folder_list.clear()
			pics = [file for file in os.listdir(path) if file.endswith('.png') or file.endswith('.jpg')]
			for pic in pics:
				item = QListWidgetItem(pic)  # 創建新的 QListWidgetItem
				item.setFlags(item.flags() | Qt.ItemIsUserCheckable)  # 添加可選擇標記
				item.setCheckState(Qt.Checked)  # 設置預設為選中狀態
				self.folder_list.addItem(item)  # 添加項目到 QListWidget

			self.save_setting()

	def get_all_select_folder(self)->list:
		selected_folders = []
		for index in range(self.folder_list.count()):
			item = self.folder_list.item(index)
			if item.checkState() == Qt.Checked:  # Qt.Checked 代表選中
				selected_folders.append(item.text())
		return selected_folders

	def disable_all_folder(self):
		if self.folder_list.count() <= 0:
			return
		for index in range(self.folder_list.count()):
			item = self.folder_list.item(index)
			item.setCheckState(False)

	def enable_all_folder(self):
		if self.folder_list.count() <= 0:
			return
		for index in range(self.folder_list.count()):
			item = self.folder_list.item(index)
			item.setCheckState(Qt.Checked)

	def load_setting(self):
		self.m_settingMgr = Setting()
		self.m_setting = self.m_settingMgr.get_setting()
		
		self.key_input.setText(self.m_setting["compress_key"])
		self.folder_input.setText(self.m_setting["compress_path"])

		self.update_folder_list()

	def save_setting(self):
		self.m_setting["compress_key"] = self.key_input.text()
		self.m_setting["compress_path"] = self.folder_input.text()

		self.m_settingMgr.save_setting(self.m_setting)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = CompressionGUI()
	sys.exit(app.exec_())