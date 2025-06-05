import sys
import os
import json
import subprocess
import re
from functools import partial
from common.ToolSetting import Setting
from common.function import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

WINDOWS_WIDTH = 600
WINDOWS_HEIGHT = 700

LANG_LIST = [ "cn", "en", "kh", "ph", "th", "vi" ]
EXCEPT_FOLDER = ["plist"]
DEFAULT_LANG = "cn"

class CsdFindPath(QWidget):
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
		self.m_pngFileData = {}
		self.m_jpgFileData = {}
		self.m_csdFileData = {}
		self.m_plistFileData = {}
		self.m_disapearFile = []

	def create_ui(self):
		self.setting_label = QLabel('要尋找路徑的類型')
		self.check_box_find_png = QCheckBox('.png(圖)', self)
		self.check_box_find_jpg = QCheckBox('.jpg(圖)', self)
		self.check_box_find_plist = QCheckBox('.plist(特效)', self)
		self.check_box_find_csd = QCheckBox('.csd(perfab)', self)

		self.project_label = QLabel('Cocos專案資料夾路徑\nEx. R:\\iRich_Evo\\Inanna\\CocoStudioProject_PH\\Inanna\\cocosstudio')
		self.project_input = MLineEdit()
		self.project_browse = QPushButton('瀏覽')
		self.project_browse.clicked.connect( partial(self.browse_folder, inputComponent= self.project_input))

		self.start_btn = QPushButton('開始尋找')
		self.start_btn.clicked.connect( self.start_find )
		self.start_btn.setFixedWidth(120)
		self.start_btn.setFixedHeight(35)

		self.log_text_label = QLabel('Log 輸出:')
		self.log_text_edit = QTextEdit()
		self.log_text_edit.setReadOnly(True)

	def init_ui(self):
		self.option_layout = QHBoxLayout()
		self.option_layout.addWidget(self.check_box_find_png)
		self.option_layout.addWidget(self.check_box_find_jpg)
		self.option_layout.addWidget(self.check_box_find_plist)
		self.option_layout.addWidget(self.check_box_find_csd)
	
		self.proj_intput_layout = QHBoxLayout()
		self.proj_intput_layout.addWidget(self.project_input)
		self.proj_intput_layout.addWidget(self.project_browse)

		self.setting_layout = QVBoxLayout()
		self.setting_layout.addWidget(self.setting_label)
		self.setting_layout.addLayout(self.option_layout)
		self.setting_layout.addWidget(self.project_label)
		self.setting_layout.addLayout(self.proj_intput_layout)
		self.setting_layout.addWidget(self.start_btn)

		self.log_layout = QVBoxLayout()
		self.log_layout.addWidget(self.log_text_label)
		self.log_layout.addWidget(self.log_text_edit)

		self.main_layout = QVBoxLayout(self)
		self.main_layout.addLayout(self.setting_layout)
		self.main_layout.addLayout(self.log_layout)

		# 設定視窗屬性
		self.setWindowTitle('csd 圖片自動找路徑')
		self.setGeometry(200, 200, WINDOWS_WIDTH, WINDOWS_HEIGHT)
		pass

	def start_find(self):
		self.save_setting()

		log_message = f'開始尋找\n'
		self.log_text_edit.append(log_message)
		QApplication.processEvents()

		# 讀取圖片資料
		log_message = f'掃描檔案\n這需要一點時間...\n'
		self.log_text_edit.append(log_message)
		QApplication.processEvents()
		self.find_search_files()

		# 讀取csd資料 以及替換png路徑
		log_message = f'替換 csd 檔案路徑\n這需要一點時間...\n'
		self.log_text_edit.append(log_message)
		QApplication.processEvents()
		self.csd_node_find_path(self.project_input.text().replace('\\','/'))

		log_message = f'結束!\n'
		self.log_text_edit.append(log_message)
		
		log_message = f"找不到路徑的相關檔案:\n------------------\n"
		for pngName in self.m_disapearFile:
			log_message = log_message + pngName + '\n'
		log_message = log_message + '------------------\n'
		self.log_text_edit.append(log_message)

	def find_search_files(self):
		proj_path = self.project_input.text().replace('\\','/')

		def search_folder(folder_path:str):
			try:
				# 使用 os.listdir() 获取文件夹下的所有文件和文件夹
				items = os.listdir(folder_path)
				
				for item in items:
					item_path = os.path.join(folder_path, item)
					# 如果是文件夹，递归搜索
					if os.path.isdir(item_path):
						if item in LANG_LIST:
							if item != DEFAULT_LANG:
								continue

						if item in EXCEPT_FOLDER:
							continue

						search_folder(item_path)
					
					# 非文件夾資料 查看是否需要紀錄
					self.record_file(item, folder_path)
						
			except OSError as e:
				print("Error accessing folder e:{}".format(e))

		# 开始搜索
		search_folder(proj_path)

	def record_file(self, item:str, folder_path:str):

		def record_to_dict(endChar:str, saveDict:dict, item:str, folder_path:str):
			if item.endswith(endChar):
				saveDict[item] = os.path.join(folder_path, item).replace('\\','/')
				# log_message = f"找到 {item}{endChar} 位置:{saveDict[item]}"
				# self.log_text_edit.append(log_message)
				# QApplication.processEvents()

		# PNG
		if self.check_box_find_png.isChecked():
			record_to_dict('.png', self.m_pngFileData, item, folder_path)
			
		# JPG
		if self.check_box_find_jpg.isChecked():
			record_to_dict('.jpg', self.m_jpgFileData, item, folder_path)

		# PLIST
		if self.check_box_find_plist.isChecked():
			record_to_dict('.plist', self.m_plistFileData, item, folder_path)
			
		# CSD
		if self.check_box_find_csd.isChecked():
			record_to_dict('.csd', self.m_csdFileData, item, folder_path)
			

	# key 為檔名, value 為路徑
	def find_img_files(self, path:str)->dict:
		img_file = {}

		def search_folder(folder_path:str):
			try:
				# 使用 os.listdir() 获取文件夹下的所有文件和文件夹
				items = os.listdir(folder_path)
				
				for item in items:
					item_path = os.path.join(folder_path, item)
					
					# 如果是文件夹，递归搜索
					if os.path.isdir(item_path):
						if item in LANG_LIST:
							if item != DEFAULT_LANG:
								return

						if item in EXCEPT_FOLDER:
							return

						search_folder(item_path)
					
					# 如果是 .png 文件，加入列表
					elif item.endswith('.png'):
						img_file[item] = os.path.join(folder_path, item).replace('\\','/')
						
			except OSError as e:
				print("Error accessing folder e:{}".format(e))

		# 开始搜索
		search_folder(path)

		return img_file

	def csd_node_find_path(self, path:str):

		def search_folder(folder_path:str):
			try:
				# 使用 os.listdir() 获取文件夹下的所有文件和文件夹
				items = os.listdir(folder_path)
				
				for item in items:
					item_path = os.path.join(folder_path, item).replace('\\','/')
					
					# 如果是文件夹，递归搜索
					if os.path.isdir(item_path):
						search_folder(item_path)
					
					# 如果是 .csd 文件，替換
					elif item.endswith('.csd'):
						self.replace_img_path(item_path)

			except OSError as e:
				print("Error accessing folder e:{}".format(e))

		# 如果事前有先搜索過csd檔案這邊就不用再找一次了
		if self.check_box_find_csd.isChecked():
			for csdFileName, csdFilePath in self.m_csdFileData.items():
				self.replace_img_path(csdFilePath)

		# 开始搜索
		search_folder(path)


	def replace_img_path(self, item_path:str)->bool:
		csdContent = ""
		# 讀取檔案內容
		try:
			with open(item_path, 'r', encoding='utf-8') as file:
				csdContent = file.read()
				
		except:
			print(f'{item_path} can\'t read')
			return False

		need_replace = False
		def replace_by_type(reType:str, replaceDict:dict, csdContent:str, item_path:str, need_replace:bool)->str:
			replace_pattern = f'Path="(.+\\.{reType})"'
			all_replace_list = re.findall(replace_pattern, csdContent)

			for oldPath in all_replace_list:
				rootFolder = oldPath.split('/')[0]
				oldPng = oldPath.split('/')[-1]

				if not replaceDict.get(oldPng):
					# log_message = f'找不到 {oldPng} 的路徑\n'
					# self.log_text_edit.append(log_message)
					# QApplication.processEvents()
					if not oldPng in self.m_disapearFile:
						self.m_disapearFile.append(oldPng)
					continue

				newPath = self.get_path_after_string( replaceDict.get(oldPng), rootFolder)
				if newPath == None:
					# log_message = f'找不到 {oldPng} 的路徑\n'
					# self.log_text_edit.append(log_message)
					# QApplication.processEvents()
					if not oldPng in self.m_disapearFile:
						self.m_disapearFile.append(oldPng)
					continue

				# 如果有需要替換
				if oldPath != newPath:
					log_message = f'替換 {oldPng} 的路徑\n 從 {oldPath} 改成 {newPath}\n'
					self.log_text_edit.append(log_message)
					QApplication.processEvents()
					csdContent = csdContent.replace(oldPath, newPath)
					need_replace = True

			return csdContent, need_replace

		if self.check_box_find_png.isChecked():
			csdContent, need_replace = replace_by_type( "png",   self.m_pngFileData,   csdContent, item_path, need_replace )
		if self.check_box_find_jpg.isChecked():
			csdContent, need_replace = replace_by_type( "jpg",   self.m_jpgFileData,   csdContent, item_path, need_replace )
		if self.check_box_find_plist.isChecked():
			csdContent, need_replace = replace_by_type( "plist", self.m_plistFileData, csdContent, item_path, need_replace )
		if self.check_box_find_csd.isChecked():
			csdContent, need_replace = replace_by_type( "csd",   self.m_csdFileData,   csdContent, item_path, need_replace )
		
		if need_replace:
			# 覆蓋寫回檔案
			with open(item_path, 'w', encoding='utf-8') as file:
				file.write(csdContent)

			log_message = f'Csd 檔案 {item_path} 已更新\n'
			self.log_text_edit.append(log_message)
			QApplication.processEvents()

		return need_replace

	def get_path_after_string(self, path:str, tatget:str):
		# 找到目標字串在完整路徑中的索引
		index = path.find(tatget)
		result_path = ""

		# 如果找到目標字串
		if index != -1:
			# 提取目標字串之後的部分
			result_path = path[index:]
			return result_path
		else:
			return None  # 如果沒找到目標字串，返回 None 

	def check_stop(self, msg:str)->bool:
		msg_box = QMessageBox(self)
		msg_box.setText(msg)
		# 0
		msg_box.addButton('暫停', QMessageBox.ButtonRole.ActionRole)
		# 1
		msg_box.addButton('繼續', QMessageBox.ButtonRole.ActionRole)

		# 顯示消息框，並等待用戶的選擇
		result = msg_box.exec_()

		if result == 0:
			self.m_forceStop = True
		else:
			return

	def browse_folder(self, inputComponent):
		startPath =  inputComponent.text() if url_format_check(inputComponent.text()) else "~"
		folder_path = QFileDialog.getExistingDirectory(self, '選擇資料夾', startPath)
		if folder_path:
			inputComponent.setText(folder_path)


	def load_setting(self):
		self.m_settingMgr = Setting()
		self.m_setting = self.m_settingMgr.get_setting()

		self.check_box_find_png.setChecked(self.m_setting["check_find_png"])
		self.check_box_find_jpg.setChecked(self.m_setting["check_find_jpg"])
		self.check_box_find_plist.setChecked(self.m_setting["check_find_plist"])
		self.check_box_find_csd.setChecked(self.m_setting["check_find_csd"])
		self.project_input.setText(self.m_setting["find_path_proj"])

	def save_setting(self):
		self.m_setting["check_find_png"]   = self.check_box_find_png.isChecked()
		self.m_setting["check_find_jpg"]   = self.check_box_find_jpg.isChecked()
		self.m_setting["check_find_plist"] = self.check_box_find_plist.isChecked()
		self.m_setting["check_find_csd"]   = self.check_box_find_csd.isChecked()
		self.m_setting["find_path_proj"]   = self.project_input.text()

		self.m_settingMgr.save_setting(self.m_setting)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = CsdFindPath()
	sys.exit(app.exec_())