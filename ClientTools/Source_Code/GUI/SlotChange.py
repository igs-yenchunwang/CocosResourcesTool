import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)).replace('\GUI', '')
sys.path.append(os.path.dirname(SCRIPT_DIR))

import json
import subprocess
from functools import partial
from Source_Code.common.ToolSetting import *
from Source_Code.common.function import *
from Source_Code.adjustFont import *
from Source_Code.adjustCsd import *
from Source_Code.FontToPlist import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


WINDOWS_WIDTH = 500
WINDOWS_HEIGHT = 800

class SlotChange(QWidget):
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
		self.texturePacker_label = QLabel('自訂 TexturePacker.exe 的位置 (如果沒有設定環境變數，需要自定義texturepacker路徑)(需附上TexturePacker.exe)')
		self.texturePacker_input = MLineEdit()
		self.texturePacker_browse_button = QPushButton('瀏覽')
		self.texturePacker_browse_button.clicked.connect(self.browse_folder_texturePacker)

		self.cocos_label = QLabel('Cocos 專案資料夾 (含有.ccs的那一層)')
		self.cocos_input = MLineEdit()
		self.cocos_browse_button = QPushButton('瀏覽')
		self.cocos_browse_button.clicked.connect( partial(self.browse_folder, inputComponent= self.cocos_input))

		# 語系選單部分
		self.language_label = QLabel('選擇語系(cn、en為預設語系，如果找不到語系會用en作替代)：')
		self.language_options = QGroupBox('語系')
		self.language_layout = QVBoxLayout()
		self.language_checkboxes = {
			"cn": QCheckBox("簡體中文 (cn)"),
			"en": QCheckBox("英文 (en)"),
			"th": QCheckBox("泰文 (th)"),
			"kh": QCheckBox("高棉文 (kh)"),
			"mm": QCheckBox("緬甸文 (mm)"),
			"ph": QCheckBox("菲律賓文 (ph)"),
			"vi": QCheckBox("越南文 (vi)"),
		}
		for checkbox in self.language_checkboxes.values():
			checkbox.setChecked(True)
			self.language_layout.addWidget(checkbox)
		self.language_checkboxes["cn"].setEnabled(False) 
		self.language_checkboxes["en"].setEnabled(False) 
		self.language_options.setLayout(self.language_layout)

		self.note_label = QLabel('備註: 語系資料夾名稱要為 font or fonts，如果命名錯誤工具會運作錯誤')
		self.start_compress = QPushButton('開始轉換')
		self.start_compress.clicked.connect(self.start_change)
		self.start_compress.setFixedHeight(40)
		self.start_compress.setFixedWidth(70)

		self.log_label = QLabel('LOG:')
		self.log_text_edit = QTextEdit()
		self.log_text_edit.setReadOnly(True)

	def init_ui(self):
		cocos_intput_layout = QHBoxLayout()
		cocos_intput_layout.addWidget(self.cocos_input)
		cocos_intput_layout.addWidget(self.cocos_browse_button)

		textpacker_intput_layout = QHBoxLayout()
		textpacker_intput_layout.addWidget(self.texturePacker_input)
		textpacker_intput_layout.addWidget(self.texturePacker_browse_button)

		option_layer = QVBoxLayout()
		option_layer.addWidget(self.texturePacker_label)
		option_layer.addLayout(textpacker_intput_layout)
		option_layer.addWidget(self.cocos_label)
		option_layer.addLayout(cocos_intput_layout)
		option_layer.addWidget(self.language_label)
		option_layer.addWidget(self.language_options)
		option_layer.addWidget(self.note_label)
		option_layer.addWidget(self.start_compress)
		log_layer = QVBoxLayout()
		log_layer.addWidget(self.log_label)
		log_layer.addWidget(self.log_text_edit)

		main_layer = QVBoxLayout()
		main_layer.addLayout(option_layer)
		main_layer.addLayout(log_layer)

		# 設定視窗佈局
		self.setLayout(main_layer)

		# 設定視窗屬性
		self.setWindowTitle('Slot 轉換工具')
		self.setGeometry(100, 100, WINDOWS_WIDTH, WINDOWS_HEIGHT)

	def start_change(self):
		if not os.path.exists(self.cocos_input.text()):
			self.update_log_text(f'路徑錯誤 X_X\n')
			return

		self.update_log_text(f'需要一段時間 請稍後......\n')

		fontPath = self.FindFontFolder(self.cocos_input.text())
		# 獲取已勾選的語系並加入陣列
		langList = [key for key, checkbox in self.language_checkboxes.items() if checkbox.isChecked()]
		AdjustFont(fontPath, langList)
		self.update_log_text(f'font 格式轉換OK\n')
		FontToPlist(fontPath, self.texturePacker_input.text(), langList)
		self.update_log_text(f'包 plist OK\n')
		# shutil.copytree( os.path.join(fontPath, "en"), os.path.join(fontPath, "ph"))
		# self.update_log_text(f'多複製一份ph資料夾OK\n')
		AdjustCsd(self.cocos_input.text())
		self.update_log_text(f'csd重指路徑OK\n')

		self.update_log_text(f'轉換結束!!!\n')

	def FindFontFolder(self, rootPath:str)->str:
		print(rootPath)
		def searchFolder(path):
			if not os.path.isdir(path):
				return
			items = os.listdir(path)

			for item in items:
				if item.lower() == "font" or item.lower() == "fonts":
					return os.path.join(path,item)

				if os.path.isdir(os.path.join(path,item)):
					fontPath = searchFolder(os.path.join(path,item))
					if fontPath != None:
						return fontPath

		res = searchFolder(rootPath)

		return res
		
	def browse_folder(self, inputComponent):
		startPath =  inputComponent.text() if url_format_check(inputComponent.text()) else "~"
		folder_path = QFileDialog.getExistingDirectory(self, '選擇資料夾', startPath)
		if folder_path:
			inputComponent.setText(folder_path)
		self.save_setting()

	def browse_folder_texturePacker(self):
		startPath = self.texturePacker_input.text() if url_format_check(self.texturePacker_input.text()) else "~"
		selected_file, _ = QFileDialog.getOpenFileUrl(self, '選擇texture packer執行檔', QUrl.fromLocalFile(startPath), 'Executable Files (*.exe)')
		if selected_file:
			self.texturePacker_input.setText(selected_file.toLocalFile())
		self.save_setting()

	def update_log_text(self, text):
		self.log_text_edit.append(text)
		QApplication.processEvents()

	def load_setting(self):
		self.m_settingMgr = Setting()
		self.m_setting = self.m_settingMgr.get_setting()

		self.texturePacker_input.setText(self.m_setting["texturepacker_path"])
		
	def save_setting(self):
		self.m_setting["texturepacker_path"] = self.texturePacker_input.text()

		self.m_settingMgr.save_setting(self.m_setting)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = SlotChange()
	sys.exit(app.exec_())
