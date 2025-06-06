import sys
import os
import json
import threading

SETTING_FILE_NAME = "tool_setting.json"
# --------- 預設資料 ---------	
DEFAULT_SETTING = {\
# 移動檔案用
"check_change_csd":False, "change_csd_path":"",\
# 包plist用
"check_customize_texturepacker":False, "texturepacker_path":"",\
"target_plist_path":"",\
"source_img_path":"",\
"max_size":1024,\
"bording_padding":1,\
"shape_padding":1,\
"enable_tinypng_compress":False,\
# csd 找路徑用
"check_find_png":True,\
"check_find_jpg":False,\
"check_find_plist":False,\
"check_find_csd":False,\
"find_path_proj":"",\
# 壓縮圖片用
"compress_key":"",\
"compress_path":"",\
# 換顏色用
"change_color_path":"",\
}


class Singleton(object):
	_instance_lock = threading.Lock()

	def __init__(self):
		pass
	def __new__(cls, *args, **kwargs):
		if not hasattr(Singleton, '_instance'):
			with Singleton._instance_lock:
				if not hasattr(Singleton, '_instance'):
					Singleton._instance = object.__new__(cls, *args, **kwargs)
		return Singleton._instance

class Setting(Singleton):
	"""docstring for Setting"""
	def __init__(self):		
		self.m_setting = DEFAULT_SETTING

		self.load_setting()

	# --------- 讀檔 ---------	
	def load_setting(self):
		self.m_setting = DEFAULT_SETTING
		settings = {}

		if os.path.exists(SETTING_FILE_NAME):
			# 如果檔案存在，讀取內容
			with open(SETTING_FILE_NAME, 'r') as file:
				settings = json.load(file)
				print("load tool_setting.json")

		else:
			# 如果檔案不存在，則創建一個新的
			settings = DEFAULT_SETTING
			with open(SETTING_FILE_NAME, 'w') as file:
				json.dump(settings, file, indent=4)
				print('create default setting file tool_setting.json:', settings)
			return

		for key, value in settings.items():
			self.m_setting[key] = value

	# --------- 存檔 ---------	
	def save_setting_with_key(self, key, value):
			self.m_setting[key] = value
			self.save_setting(self.m_setting)

	def save_setting(self, newSetting):
		with open(SETTING_FILE_NAME, 'w') as file:
			json.dump(newSetting, file, indent=4)

	# --------- 取資料 ---------
	def get_setting(self):
		return self.m_setting
		
	def get_data_with_key(self, key):
		if self.m_setting.get(key):
			return self.m_setting[key]
		else:
			return False


if __name__ == '__main__':
	main()