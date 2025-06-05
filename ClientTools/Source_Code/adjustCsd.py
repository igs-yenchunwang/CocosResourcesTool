# -*- coding: utf-8 -*-
import os
import re
import subprocess
import shutil

def find_csd_files(root_path):
	csd_files = []  # 存儲找到的 .csd 文件的列表

	def search_folder(folder_path):
		try:
			# 使用 os.listdir() 获取文件夹下的所有文件和文件夹
			items = os.listdir(folder_path)
			
			for item in items:
				item_path = os.path.join(folder_path, item)
				
				# 如果是文件夹，递归搜索
				if os.path.isdir(item_path):
					search_folder(item_path)
				
				# 如果是 .csd 文件，加入列表
				elif item.endswith('.csd'):
					csd_files.append(item_path)
					
		except OSError as e:
			print("Error accessing folder e:{}".format(e))

	# 开始搜索
	search_folder(root_path)

	return csd_files

def ReplaceFontPath(csdFilePath):
	print(csdFilePath)
	content = ""
	# 讀取檔案內容
	with open(csdFilePath, 'r', encoding='utf-8') as file:
		content = file.read()

		# 使用正則表達式進行替換和捕獲
		pattern = re.compile('font(s*)/(.+)/(cn|en|kh|th|vi)/', re.MULTILINE)
		allMatch = pattern.findall(content)
		print(allMatch)
		for matchStr in allMatch:
			content = content.replace('font'+matchStr[0]+'/'+matchStr[1]+'/'+matchStr[2]+'/', 'font'+matchStr[0]+'/'+matchStr[2]+'/'+matchStr[1]+'/')			

	# 覆蓋寫回檔案
	with open(csdFilePath, 'w', encoding='utf-8') as file:
		file.write(content)


def AdjustCsd(path):
	csdList = find_csd_files(path)
	for csdFile in csdList:
		ReplaceFontPath(csdFile)

def main():
	csdList = find_csd_files(os.path.join(os.getcwd(), './cocosstudio/InannaResource/Inanna/ui'))
	for csdFile in csdList:
		ReplaceFontPath(os.path.join(os.getcwd(), './cocosstudio/InannaResource/Inanna/ui',csdFile))

if __name__ == '__main__':
	main()