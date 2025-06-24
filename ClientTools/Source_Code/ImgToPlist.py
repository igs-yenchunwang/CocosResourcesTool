import sys
import os
import json
import time
import subprocess
from functools import partial
from common.ToolSetting import Setting
from common.function import *
from compression.TinyPngCompression import Compression
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


WINDOWS_WIDTH = 1100
WINDOWS_HEIGHT = 400

class ImgToPlist(QWidget):
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
		self.m_forceStop = False		# 是否強制停止打包
		self.m_texturePackerPath = ""	# texturePacker位置
		self.m_plistMaxSize = 0			# 包plist的最大上限
		self.m_outOfLimitList = []		# 超出上限的清單
		self.m_folderListShow = False

	def create_ui(self):
		self.check_box_texturePacker = QCheckBox('自訂 TexturePacker.exe 的位置 (如果沒有設定環境變數，需要自定義texturepacker路徑)(需附上TexturePacker.exe)')
		self.check_box_texturePacker.clicked.connect(self.save_setting)
		self.texturePacker_input = MLineEdit()
		self.texturePacker_browse_button = QPushButton('瀏覽')
		self.texturePacker_browse_button.clicked.connect(self.browse_folder_texturePacker)

		self.imgPath_label = QLabel('img 資料夾位置')
		self.imgPath_input = MLineEdit()
		self.imgPath_input.textChanged.connect(self.update_folder_list)  # 偵測文字變化
		self.imgPath_browse_button = QPushButton('瀏覽')
		self.imgPath_browse_button.clicked.connect(self.browse_folder_imgPath)

		self.plistPath_label = QLabel('plist 輸出位置')
		self.plistPath_input = MLineEdit()
		self.plistPath_input.textChanged.connect( partial(self.check_path_exist, intputLine = self.plistPath_input) )
		self.plistPath_browse_button = QPushButton('瀏覽')
		self.plistPath_browse_button.clicked.connect(self.browse_folder_listPath)

		self.more_option_button = QPushButton('<<更多')
		self.more_option_button.clicked.connect(self.switch_more_option_show)
		self.more_option_button.setFixedWidth(40)

		self.folder_all_select = QPushButton('All')
		self.folder_all_select.setFixedWidth(40)
		self.folder_none_select = QPushButton('None')
		self.folder_none_select.setFixedWidth(40)
		self.fore_8888 = QCheckBox('強制包RGBA8888')

		# TinyPNG 壓縮相關UI
		self.enable_tinypng = QCheckBox('啟用 TinyPNG 壓縮 (打包完成後自動壓縮PNG檔案)')
		self.enable_tinypng.clicked.connect(self.save_setting)
		self.tinypng_key_label = QLabel('TinyPNG API Key:')
		self.tinypng_key_input = QLineEdit()
		self.tinypng_key_input.setEchoMode(QLineEdit.Password)  # 隱藏輸入的API key
		self.tinypng_key_input.textChanged.connect(self.save_setting)

		self.folder_list = QListWidget(self)
		self.folder_list.hide()
		self.folder_all_select.hide()
		self.folder_none_select.hide()  # 初始化時隱藏
		self.fore_8888.hide()
		self.enable_tinypng.hide()
		self.tinypng_key_label.hide()
		self.tinypng_key_input.hide()
		self.folder_all_select.clicked.connect(self.enable_all_folder)
		self.folder_none_select.clicked.connect(self.disable_all_folder)

		self.start_button = QPushButton('開始包plist')
		self.start_button.clicked.connect(self.start_making_plist)
		self.start_button.setFixedWidth(150)
		self.start_button.setFixedHeight(40)

		self.texture_packer_setting_label = QLabel('目前 texture packer 包圖設定為:\n\
\tData format: cocos2d\n\
\tPixel format: RGBA4444 + FloydSteinbergAlpha or RGBA8888(看資料夾名稱)\n\
\tSize constraints: AnySize\n\
\tScale: 1\n\
\tForce Squared\n\
\tTrim mode: Trim\n\
\tTrim Margin: 1\
')
		self.texture_packer_setting_label2 		  = QLabel('\n\n自定義區 (目前主觀認為要拉出來的)\n')
		self.texture_packer_maxSize_Label 		  = QLabel('Max size:		   ')
		self.texture_packer_maxSize_input 		  = QLineEdit()
		self.texture_packer_bording_padding_label = QLabel('Border padding:')
		self.texture_packer_bording_padding_input = QLineEdit()
		self.texture_packer_shape_padding_label   = QLabel('Shape padding:  ')
		self.texture_packer_shape_padding_input   = QLineEdit()

		self.log_label = QLabel('LOG:')
		self.log_text_edit = QTextEdit()
		self.log_text_edit.setReadOnly(True)

	def init_ui(self):

		texture_layer = QHBoxLayout()
		texture_layer.addWidget(self.texturePacker_input)
		texture_layer.addWidget(self.texturePacker_browse_button)

		imgPath_layer = QHBoxLayout()
		imgPath_layer.addWidget(self.imgPath_input)
		imgPath_layer.addWidget(self.imgPath_browse_button)		

		plistPath_layer = QHBoxLayout()
		plistPath_layer.addWidget(self.plistPath_input)
		plistPath_layer.addWidget(self.plistPath_browse_button)		

		max_size = QHBoxLayout()
		max_size.addWidget(self.texture_packer_maxSize_Label)
		max_size.addWidget(self.texture_packer_maxSize_input)	

		bording_padding = QHBoxLayout()
		bording_padding.addWidget(self.texture_packer_bording_padding_label)
		bording_padding.addWidget(self.texture_packer_bording_padding_input)	

		shape_padding = QHBoxLayout()
		shape_padding.addWidget(self.texture_packer_shape_padding_label)
		shape_padding.addWidget(self.texture_packer_shape_padding_input)	

		label1 = QHBoxLayout()
		label1.addWidget(self.texture_packer_setting_label)
		label2 = QHBoxLayout()
		label2.addWidget(self.texture_packer_setting_label2)

		folder_setting = QVBoxLayout()
		folder_setting.addWidget(self.check_box_texturePacker)
		folder_setting.addLayout(texture_layer)
		folder_setting.addWidget(self.imgPath_label)
		folder_setting.addLayout(imgPath_layer)
		folder_setting.addWidget(self.plistPath_label)
		folder_setting.addLayout(plistPath_layer)

		self.setting_layer = QVBoxLayout()
		self.setting_layer.addLayout(folder_setting)

		self.start_layer = QHBoxLayout()
		self.start_layer.setAlignment(Qt.AlignLeft)
		self.start_layer.addWidget(self.more_option_button)
		self.start_layer.addWidget(self.start_button)	

		self.setting_layer.addLayout(label1)
		self.setting_layer.addLayout(label2)
		self.setting_layer.addLayout(max_size)
		self.setting_layer.addLayout(bording_padding)
		self.setting_layer.addLayout(shape_padding)
		self.setting_layer.addLayout(self.start_layer)
		
		self.setting_layer.addStretch(1)

		self.log_layer = QVBoxLayout()
		self.log_layer.addWidget(self.log_label)
		self.log_layer.addWidget(self.log_text_edit)

		self.more_option_btn = QHBoxLayout()
		self.more_option_btn.setAlignment(Qt.AlignLeft)
		self.more_option_btn.addWidget(self.folder_all_select)
		self.more_option_btn.addWidget(self.folder_none_select)
		self.more_option_btn.addWidget(self.fore_8888)

		# TinyPNG 設定區域
		self.tinypng_option_layer = QVBoxLayout()
		self.tinypng_option_layer.addWidget(self.enable_tinypng)
		tinypng_key_layer = QHBoxLayout()
		tinypng_key_layer.addWidget(self.tinypng_key_label)
		tinypng_key_layer.addWidget(self.tinypng_key_input)
		self.tinypng_option_layer.addLayout(tinypng_key_layer)

		self.more_option_layer = QVBoxLayout()
		self.more_option_layer.addLayout(self.more_option_btn)
		self.more_option_layer.addLayout(self.tinypng_option_layer)
		self.more_option_layer.addWidget(self.folder_list)

		self.main_layer = QHBoxLayout()
		self.main_layer.addLayout(self.more_option_layer)
		self.main_layer.addLayout(self.setting_layer)
		self.main_layer.addLayout(self.log_layer)

		# 設定視窗佈局
		self.setLayout(self.main_layer)

		# 設定視窗屬性
		self.setWindowTitle('包plist工具')
		self.setGeometry(100, 100, WINDOWS_WIDTH, WINDOWS_HEIGHT)

		pass

	# 確定路徑是否存在
	def check_path_exist(self, intputLine:QLineEdit):
		if intputLine.text() == "":
			return
		if not os.path.exists(intputLine.text()):
			ret = QMessageBox.information(
				self, '提示',
				'路徑不存在，請重新選擇路徑',
				QMessageBox.Ok)
			intputLine.setText("")

	# 確定 texturepacker 指令是否為可用
	def CheckTextureStatus(self):
		texturePakerPath = "TexturePacker"
		if self.check_box_texturePacker.isChecked():
			texturePakerPath = self.m_texturePackerPath

		cmd = f"{texturePakerPath} --help"
		try:
			result = subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True) 
			if result.returncode != 0:
				return False	
		except:
			return False

		return True

	def start_making_plist(self):
		if not self.imgPath_input.text():
			self.show_message_box("沒有填入img路徑")
			return

		if not self.plistPath_input.text():
			self.show_message_box("沒有填入plist路徑")
			return

		if self.check_box_texturePacker.isChecked() and not self.texturePacker_input.text():
			self.show_message_box("沒有填入 texture packer 路徑")
			return

		if self.check_box_texturePacker.isChecked() and self.texturePacker_input.text():
			texturePakerPath = self.texturePacker_input.text()
			texturePakerPath = texturePakerPath.replace('..', '\\'.join( os.getcwd().split('\\')[:-1] ))
			self.m_texturePackerPath = texturePakerPath

		self.save_setting()
		self.m_forceStop = False
		self.m_outOfLimitList = []

		res = self.CheckTextureStatus()
		if not res:
			ret = QMessageBox.information(
				self, '提示',
				'texture packer 指令失效\n請至texture packer資料夾點擊TexturePackerGUI.exe安裝相關套件，以及啟用\n或是你的執行路徑中含有空白',
				QMessageBox.Ok)
			return

		log_message = f'需要一段時間 請稍後......\n'
		self.log_text_edit.append(log_message)
		QApplication.processEvents()

		originPath = os.getcwd()
		imgPath = self.imgPath_input.text()
		outputPath = self.plistPath_input.text()
		os.chdir(imgPath)

		dirList = self.get_all_select_folder()
		for folderName in dirList:
			if not os.path.isdir(folderName):
				continue
			res = self.CreatePlistWithFolder(folderName, outputPath)

			if res == 1 or self.m_forceStop:
				break

		os.chdir(originPath)
		log_message = f'轉換結束!!!\n'
		self.log_text_edit.append(log_message)
		QApplication.processEvents()

		log_message = f'超出範圍包不下的清單:\n---------------------\n'
		for folderName in self.m_outOfLimitList:
			log_message = log_message + f'{folderName}\n'
		log_message = log_message + f'---------------------\n'
		self.log_text_edit.append(log_message)
		QApplication.processEvents()

		ret = QMessageBox.information(
			self, '提示',
			'轉換結束!!!',
			QMessageBox.Ok)

	def update_folder_list(self):
		path = self.imgPath_input.text()
		if os.path.isdir(path):
			self.folder_list.clear()
			folders = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]
			for folder in folders:
				item = QListWidgetItem(folder)  # 創建新的 QListWidgetItem
				item.setFlags(item.flags() | Qt.ItemIsUserCheckable)  # 添加可選擇標記
				item.setCheckState(Qt.Checked)  # 設置預設為選中狀態
				self.folder_list.addItem(item)  # 添加項目到 QListWidget
		else:
			if path == "":
				return
			ret = QMessageBox.information(
			self, '提示',
			'路徑不存在，請重新選擇路徑',
			QMessageBox.Ok)
			self.imgPath_input.setText("")

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

	def switch_more_option_show(self):
		if self.m_folderListShow:
			self.folder_list.hide()
			self.folder_all_select.hide()
			self.folder_none_select.hide()
			self.fore_8888.hide()
			self.enable_tinypng.hide()
			self.tinypng_key_label.hide()
			self.tinypng_key_input.hide()
		else:
			self.folder_list.show()
			self.folder_all_select.show()
			self.folder_none_select.show()
			self.fore_8888.show()
			self.enable_tinypng.show()
			self.tinypng_key_label.show()
			self.tinypng_key_input.show()

		self.m_folderListShow = not self.m_folderListShow

	def CreatePlistUnlimitedSizeWithFolder( self, folderName:str, outputPath:str )->int:
		texturePakerPath = "TexturePacker"
		if self.check_box_texturePacker.isChecked():
			texturePakerPath = self.m_texturePackerPath

		optimize = "RGBA8888" if ("8888" in folderName) or (self.fore_8888.isChecked()) else "RGBA4444 --dither-fs-alpha"
		cmd = f'{texturePakerPath} \
	 --sheet {os.path.join(outputPath, folderName)}.png \
	 --data {os.path.join(outputPath, folderName)}.plist \
	 --format cocos2d \
	 --opt {optimize} \
	 --force-squared \
	 --border-padding {self.texture_packer_bording_padding_input.text()}\
	 --shape-padding {self.texture_packer_shape_padding_input.text()}\
	 --size-constraints AnySize \
	 --extrude 1\
	 --trim-mode Trim\
	 --trim-threshold 1\
	 --algorithm MaxRects\
	 --maxrects-heuristics Best\
	 --pack-mode Best\
	 --enable-rotation\
	 ./{folderName}/'

		result = subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True) 

		log_message = ""
		if result.returncode == 0:
			log_message = f'已輸出 plist: {folderName}\n'
			
			# 如果plist創建成功且啟用了TinyPNG壓縮，則壓縮PNG檔案
			png_file_path = os.path.join(outputPath, folderName + '.png')
			if self.enable_tinypng.isChecked() and os.path.exists(png_file_path):
				self.compress_png_with_tinypng(png_file_path)
				
		elif result.returncode == 1:
			log_message = f'路徑中的 TexturePacker.exe 錯誤，可能缺少填入"TexturePacker.exe，請在路徑後面補上"\n'
		else:
			log_message = f'錯誤!! plist: {folderName} 錯誤代號:{result.returncode}\n錯誤訊息:{result.stderr}\n'
		self.log_text_edit.append(log_message)
		QApplication.processEvents()

		return result.returncode

	def compress_png_with_tinypng(self, png_file_path:str)->bool:
		"""使用TinyPNG壓縮PNG檔案"""
		if not self.enable_tinypng.isChecked():
			return True
			
		api_key = self.tinypng_key_input.text().strip()
		if not api_key:
			log_message = f'TinyPNG API Key 未設定，跳過壓縮\n'
			self.log_text_edit.append(log_message)
			QApplication.processEvents()
			return True
			
		if not os.path.exists(png_file_path):
			log_message = f'PNG檔案不存在: {png_file_path}\n'
			self.log_text_edit.append(log_message)
			QApplication.processEvents()
			return False
			
		try:
			log_message = f'開始壓縮 PNG: {os.path.basename(png_file_path)}\n'
			self.log_text_edit.append(log_message)
			QApplication.processEvents()
			
			compressor = Compression()
			compressor.SetKey(api_key)
			
			# 獲取壓縮結果
			compression_result = compressor.GetCompressionRes(png_file_path)
			if not compression_result:
				log_message = f'TinyPNG 壓縮失敗: {os.path.basename(png_file_path)}\n'
				self.log_text_edit.append(log_message)
				QApplication.processEvents()
				return False
				
			# 解析下載URL
			download_url = compressor.ParseUrlFromRes(compression_result)
			if not download_url:
				log_message = f'無法獲取壓縮後的下載URL: {os.path.basename(png_file_path)}\n'
				self.log_text_edit.append(log_message)
				QApplication.processEvents()
				return False
				
			# 下載壓縮後的檔案
			compressor.DownloadPicWithUrl(download_url, png_file_path)
			
			log_message = f'TinyPNG 壓縮完成: {os.path.basename(png_file_path)}\n'
			self.log_text_edit.append(log_message)
			QApplication.processEvents()
			return True
			
		except Exception as e:
			log_message = f'TinyPNG 壓縮錯誤: {str(e)}\n'
			self.log_text_edit.append(log_message)
			QApplication.processEvents()
			return False

	def CreatePlistWithFolder( self, folderName:str, outputPath:str )->int:
		# 先刪掉原本的檔案
		plistFile = os.path.join(outputPath, folderName+'.plist')
		if os.path.exists(plistFile):
			os.remove(plistFile)
		pngFile = os.path.join(outputPath, folderName+'.png')
		if os.path.exists(pngFile):
			os.remove(pngFile)

		texturePakerPath = "TexturePacker"
		if self.check_box_texturePacker.isChecked():
			texturePakerPath = self.m_texturePackerPath

		optimize = "RGBA8888" if "8888" in folderName else "RGBA4444 --dither-fs-alpha"

		cmd = f'{texturePakerPath} \
	 --sheet {os.path.join(outputPath, folderName)}.png \
	 --data {os.path.join(outputPath, folderName)}.plist \
	 --format cocos2d \
	 --opt {optimize} \
	 --force-squared \
	 --max-width {self.texture_packer_maxSize_input.text()} \
	 --max-height {self.texture_packer_maxSize_input.text()} \
	 --border-padding {self.texture_packer_bording_padding_input.text()}\
	 --shape-padding {self.texture_packer_shape_padding_input.text()}\
	 --size-constraints AnySize \
	 --extrude 1\
	 --trim-mode Trim\
	 --trim-threshold 1\
	 --algorithm MaxRects\
	 --maxrects-heuristics Best\
	 --pack-mode Best\
	 --enable-rotation\
	 ./{folderName}/'

		result = subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True) 

		log_message = ""
		if result.returncode == 0:
			log_message = f'已輸出 plist: {folderName} 路徑:{outputPath}\n'
			
			# 如果plist創建成功且啟用了TinyPNG壓縮，則壓縮PNG檔案
			png_file_path = os.path.join(outputPath, folderName + '.png')
			if self.enable_tinypng.isChecked() and os.path.exists(png_file_path):
				self.compress_png_with_tinypng(png_file_path)
				
		elif result.returncode == 1:
			log_message = f'路徑中的 TexturePacker.exe 錯誤，可能缺少填入"TexturePacker.exe，請在路徑後面補上"\n'
		else:
			log_message = f'錯誤!! plist: {folderName} 錯誤代號:{result.returncode} 錯誤訊息:{result.stderr}\n'
		self.log_text_edit.append(log_message)
		QApplication.processEvents()

		# Not all sprites could be packed into the texture
		# res = -1
		# 1024*1024 放不下額外要處理的動作
		if "Not all sprites could be" in result.stderr:
			self.m_outOfLimitList.append(folderName)
			# res = self.check_stop(f'看來 {folderName} 中的圖片塞不進 {self.texture_packer_maxSize_input.text()} * {self.texture_packer_maxSize_input.text()}，你需要先中斷去修改嗎?')
		# if res == 2:
		# 	self.CreatePlistUnlimitedSizeWithFolder(folderName, outputPath)

		return result.returncode

	def check_stop(self, msg:str)->int:
		msg_box = QMessageBox(self)
		msg_box.setText(msg)

		# 0
		msg_box.addButton('中斷', QMessageBox.ButtonRole.ActionRole)
		# 1
		msg_box.addButton('略過這張繼續', QMessageBox.ButtonRole.ActionRole)
		# 2
		msg_box.addButton('不管上限強制包', QMessageBox.ButtonRole.ActionRole)

		# 顯示消息框，並等待用戶的選擇
		result = msg_box.exec_()

		if result == 0:
			self.m_forceStop = True
		
		return result

	def show_message_box(self, msg:str):
		# 創建一個 QMessageBox
		msg_box = QMessageBox()
		msg_box.setWindowTitle('提示')
		msg_box.setText(msg)
		
		# 使用 StandardButtons 來指定按鈕
		msg_box.setStandardButtons(QMessageBox.Ok)
		
		# 顯示訊息框並等待用戶操作
		result = msg_box.exec_()

	def browse_folder_texturePacker(self):
		startPath = self.texturePacker_input.text() if url_format_check(self.texturePacker_input.text()) else "~"
		selected_file, _ = QFileDialog.getOpenFileUrl(self, '選擇texture packer執行檔', QUrl.fromLocalFile(startPath), 'Executable Files (*.exe)')
		if selected_file:
			self.texturePacker_input.setText(selected_file.toLocalFile())
		self.save_setting()

	def browse_folder_imgPath(self):
		startPath =  self.imgPath_input.text() if url_format_check(self.imgPath_input.text()) else "~"
		folder_path = QFileDialog.getExistingDirectory(self, '選擇img資料夾', startPath)
		if folder_path:
			self.imgPath_input.setText(folder_path)
		self.save_setting()

	def browse_folder_listPath(self):
		startPath = self.plistPath_input.text() if url_format_check(self.plistPath_input.text()) else "~"
		folder_path = QFileDialog.getExistingDirectory(self, '選擇plist輸出資料夾', startPath)
		if folder_path:
			self.plistPath_input.setText(folder_path)
		self.save_setting()

	def load_setting(self):
		self.m_settingMgr = Setting()
		self.m_setting = self.m_settingMgr.get_setting()

		self.check_box_texturePacker.setChecked(self.m_setting["check_customize_texturepacker"])
		self.texturePacker_input.setText(self.m_setting["texturepacker_path"])
		self.imgPath_input.setText(self.m_setting["source_img_path"])
		self.plistPath_input.setText(self.m_setting["target_plist_path"])

		self.texture_packer_maxSize_input.setText(str(self.m_setting["max_size"]))
		self.texture_packer_bording_padding_input.setText(str(self.m_setting["bording_padding"]))
		self.texture_packer_shape_padding_input.setText(str(self.m_setting["shape_padding"]))

		# 載入TinyPNG相關設置
		self.enable_tinypng.setChecked(self.m_setting.get("enable_tinypng_compression", False))
		self.tinypng_key_input.setText(self.m_setting.get("compress_key", ""))

		self.update_folder_list()
		
	def save_setting(self):
		self.m_setting["check_customize_texturepacker"] = self.check_box_texturePacker.isChecked()
		self.m_setting["texturepacker_path"] = self.texturePacker_input.text()
		self.m_setting["source_img_path"] = self.imgPath_input.text()
		self.m_setting["target_plist_path"] = self.plistPath_input.text()

		self.m_setting["max_size"] = int(self.texture_packer_maxSize_input.text()) if self.texture_packer_maxSize_input.text() else 1024
		self.m_setting["bording_padding"] = int(self.texture_packer_bording_padding_input.text()) if self.texture_packer_bording_padding_input.text() else 1
		self.m_setting["shape_padding"] = int(self.texture_packer_shape_padding_input.text()) if self.texture_packer_shape_padding_input.text() else 1

		# 保存TinyPNG相關設置
		self.m_setting["enable_tinypng_compression"] = self.enable_tinypng.isChecked()
		self.m_setting["compress_key"] = self.tinypng_key_input.text()

		self.m_settingMgr.save_setting(self.m_setting)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = ImgToPlist()
	sys.exit(app.exec_())