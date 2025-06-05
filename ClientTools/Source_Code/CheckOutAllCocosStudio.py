import os
import re
import subprocess

finalPath = False
GAME_ROOT_SVN_MAP = {}
GAME_COCOS_SVN_MAP = {}
RESOURCE_PATH = "R:\\Develop\\iRich_Evo\\SouthPark\\ClientCocos\\Resources"
PROJ_PATH = "iRich_Evo\\trunk"
CHECKOUT_PATH = "R:\\GameCocos\\"

# 確認有沒有這個路徑的SVN
def CheckIsRepositoryexist(path):
	try: 
		svnInfoOutput = subprocess.check_output(["svn", "info", path], universal_newlines=False)
		return True
	except Exception as e:
		return False

# 找出在svn中的根路徑
def GetRepositoryRoot(svnInfoOutput:str)->str or False:

	# 定義正則表達式
	pattern = re.compile('Repository Root: (.+)$', re.MULTILINE)

	match = pattern.findall(svnInfoOutput)

	# 如果找到匹配，返回 Repository Root 的值
	if match:
		return match[0]
	else:
		return False

# 找出 svn 資訊
def FindSvnInfo(folderPath:str)->str or False:
	# 取出 svn 庫路徑
	try: 
		svnInfoOutput = subprocess.run("svn info", shell=True, capture_output=True, text=True)
		return svnInfoOutput.stdout
	except Exception as e:
		print("[warning] " + folderPath+ " is not in svn")
		return False

def GetCocosPath(_svnPath:str)->str or False:
	svnPath = _svnPath.replace('\\', '/')
	global finalPath
	finalPath = False

	def search_folder(path):
		try:
			svnlist = subprocess.run(f"svn list {path}", shell=True, capture_output=True, text=True)
			items = svnlist.stdout.split('\n')[:-1]
			folderList = [item.replace('/','') for item in items if item.endswith('/')]

			for item in items:
				# 找到拉!
				if '.ccs' in item:
					global finalPath
					finalPath = path
					return
				
			for folder in folderList:
				# 如果可以往下搜索
				nextPath = path+'/'+folder
				if not finalPath:
					search_folder(nextPath)

						
		except OSError as e:
			print("Error accessing folder e:{}".format(e))

	search_folder(svnPath)

	return finalPath

def FindCocosPath( folderName:str ):
	originPath = os.getcwd()
	folderPath = os.path.join(os.getcwd(), folderName)
	os.chdir(folderPath)

	print("--------------")
	print(folderName)

	# 資料夾info
	svnInfo = FindSvnInfo(folderPath)
	if not svnInfo:
		os.chdir(originPath)
		return

	# 拿遊戲根svn
	rootPath = GetRepositoryRoot(svnInfo)
	if not rootPath:
		os.chdir(originPath)
		return

	# 取過了
	gameName = rootPath.split('/')[-1]
	if GAME_ROOT_SVN_MAP.get(gameName):
		os.chdir(originPath)
		return
	GAME_ROOT_SVN_MAP[gameName] = rootPath
	
	# svn 遞迴找到有 .ccs 的位置
	if GAME_COCOS_SVN_MAP.get(gameName):
		os.chdir(originPath)
		return
	cocosPath = GetCocosPath(os.path.join(rootPath, PROJ_PATH))
	GAME_COCOS_SVN_MAP[gameName] = cocosPath
	print(gameName)
	print(cocosPath)

	os.chdir(originPath)

def main():
	# testNum = 2
	# testCount = 0

	os.chdir(RESOURCE_PATH)
	listDir = os.listdir(os.getcwd())

	print(listDir)

	# 找出所有需要切的svn 資料夾
	for item in listDir:
		# 只找資料夾
		if not os.path.isdir(item):
			continue

		FindCocosPath( item )

		# testCount = testCount + 1
		# if testCount >= testNum:
		# 	break

	for gameName, svnPath in GAME_COCOS_SVN_MAP.items():
		print(f"svn checkout {svnPath} {os.path.join(CHECKOUT_PATH, gameName)}")

	# checkout 囉
	# for gameName, svnPath in GAME_COCOS_SVN_MAP.items():
	# 	if os.path.exists(os.path.join(CHECKOUT_PATH, gameName)):
	# 		print(f"[Info] already exist : {svnPath}")
	# 		continue

	# 	try:
	# 		checkOutput = subprocess.run(f"svn checkout {svnPath} {os.path.join(CHECKOUT_PATH, gameName)}", shell=True, capture_output=True, text=True)
	# 		print(f"[Info] checkout finish: {svnPath}")			
	# 	except OSError as e:
	# 		print("Error accessing folder e:{}".format(e))

if __name__ == '__main__':
	main()