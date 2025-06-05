# -*- coding: utf-8 -*-
import os
import re
import subprocess
import shutil

LANG_LIST = [ "cn", "en", "kh", "th", "vi" ]
MAIN_LANG = "cn"

def CreateFolderIfNotExist(folderName, path = "./"):
	if not os.path.exists( os.path.join(path, folderName) ):
		os.makedirs(os.path.join(path, folderName) )


def GetAllFolder(path = "./"):
	resultList = []

	dirList = os.listdir(path)
	for fileName in dirList:
		if os.path.isdir(os.path.join(path, fileName) ) and not fileName in LANG_LIST:
			resultList.append(fileName)
		elif not fileName in LANG_LIST:
			os.remove( os.path.join(path, fileName) )

	return resultList


def AdjustFont( path, langList ):
	LANG_LIST = langList
	folderList = GetAllFolder(path)
	pngDict = {}

	for folderName in folderList:
		lang = MAIN_LANG
		sourcePath = os.path.join(path,folderName,lang)
		if not os.path.exists(sourcePath):
			continue
		pngList = os.listdir(sourcePath)
		for png in pngList:
			pngDict[png] = folderName

	for lang in LANG_LIST:
		CreateFolderIfNotExist(lang, path)
		langFolderPath = os.path.join(path, lang)  # 語系資料夾路徑
		hasFiles = False  # 用來記錄該語系資料夾是否有檔案

		for folderName in folderList:
			# 把外面的圖片複製一份近來
			sourcePath = os.path.join(path,folderName,lang)
			if not os.path.exists(sourcePath):
				continue
			pngList = os.listdir(sourcePath)

			# **新增檢查點：如果 pngList 為空，跳過處理**
			if not pngList:
				continue  # 沒有檔案直接略過這個資料夾

			# 若有檔案則進行複製操作
			hasFiles = True  # 設置標記，表示此語系資料夾有內容

			for png in pngList:
				targetPath = os.path.join(path,lang,pngDict[png])
				if not os.path.exists(targetPath):
					os.makedirs( targetPath )
				
				shutil.copyfile(os.path.join(sourcePath ,png), os.path.join(targetPath ,png))
		
		if not hasFiles:  # 如果該語系資料夾沒有檔案
			shutil.rmtree(langFolderPath)  # 刪除語系資料夾
			shutil.copytree( os.path.join(path, "en"), os.path.join(path, lang)) # 沒有的資料夾用en替代
			print(f"{lang} 資料夾沒有檔案，用en替代")

	for folderName in folderList:
		# 刪除舊的資料夾
		shutil.rmtree(os.path.join(path,folderName))

def main():
	AdjustFont('R:\\GameCocos\\KingArthur\\cocosstudio\\KingArthur\\font')

if __name__ == '__main__':
	main()