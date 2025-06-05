# -*- coding: utf-8 -*-
import os
import re
import subprocess
import shutil

LANG_LIST = ["cn","en","kh","th","vi"]

def CreatePlistWithFolder( texturePackerPath, folderName ):
	cmd = f'{texturePackerPath} \
 --sheet {folderName}.png \
 --data {folderName}.plist \
 --format cocos2d \
 --dither-fs-alpha \
 --border-padding 2\
 --shape-padding 2\
 --force-squared \
 --max-width 1024 \
 --max-height 1024 \
 --enable-rotation\
 --size-constraints AnySize \
 ./{folderName}/'

	print(cmd)
	result = subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True) 

	log_message = ""
	if result.returncode == 0:
		log_message = f'已輸出 plist: {folderName}\n'
	elif result.returncode == 1:
		log_message = f'路徑中的 TexturePacker.exe 錯誤，可能缺少填入"TexturePacker.exe，請在路徑後面補上"\n'
	else:
		log_message = f'錯誤!! plist: {folderName} 錯誤代號:{result.returncode} 錯誤訊息:{result.stderr}\n'
	print(log_message)

	return result.returncode

def FontToPlist(path, texturePackerPath, langList):
	LANG_LIST = langList
	path = path.replace('\\','/')
	originPath = os.getcwd()
	print(path, originPath)
	os.chdir(path)

	for lang in LANG_LIST:
		# 防呆檢查：確認資料夾存在
		if not os.path.exists(lang):
			print(f"資料夾 {lang} 不存在，略過該語系。")
			continue

		os.chdir(lang)
		print(os.getcwd())
		dirList = os.listdir(os.path.join( os.getcwd() ))

		for folderName in dirList:
			CreatePlistWithFolder( texturePackerPath, folderName )

		os.chdir('..')
	
	os.chdir(originPath)

def FindFontFolder(rootPath):
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

def main():
	FontToPlist('R:\\GameCocos\\KingArthur\\cocosstudio\\KingArthur\\font')


if __name__ == '__main__':
	main()