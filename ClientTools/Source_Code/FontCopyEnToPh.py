import os
import re
import subprocess
import shutil

DIR_LIST = [\
# 'AgentAce',\
'AliBaba',\
'BallSlam',\
'Boxer',\
'Crazy777',\
'DinoBall',\
'Dinosaur',\
'DoFuIII',\
'DoFuIV',\
'DragonTycoon',\
'ElfBingo',\
'EnrichGems',\
'EnrichGems2',\
'Fish5',\
'GoldenBank',\
'GoldenEmpire',\
'GoldenJoker',\
'HalloweenOneLineSlot',\
'HeroCat',\
'InfinityAce',\
'JiliCaishen',\
'LavaEruption',\
'MoneyComing',\
'NuggetRush',\
'OneLineSlot',\
'PharaohTreasure',\
'PinkPig2',\
'PowerBingo',\
'RomaSlot2',\
'Shooting3',\
'SuperRich',\
'SweetLand',\
'Thor',\
'UndeadCarnival',\
'WorldCup',\
]

MAIN_PATH = 'R:/GameCocos'

SOURCE_FOLDER = "en"
TARGET_FOLDER = "ph"

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
	for gameFolder in DIR_LIST:
		FormatPath = os.path.join(MAIN_PATH, gameFolder).replace('\\','/')
		os.chdir(FormatPath)

		svnAdd = subprocess.run("svn add . --force", shell=True, capture_output=True, text=True)
		print(svnAdd.stdout)

		svnCommit = subprocess.run('svn commit -m "#0 add ph font folder"', shell=True, capture_output=True, text=True)
		print(svnCommit.stdout)
		

		# print("----------")
		# print(FormatPath)
		
		# fontPath = FindFontFolder(FormatPath).replace('\\','/')
		# print(fontPath)

		# sourcePath = os.path.join(fontPath, SOURCE_FOLDER).replace('\\','/')
		# targetPath = os.path.join(fontPath, TARGET_FOLDER).replace('\\','/') 

		# if os.path.exists( targetPath ):
		# 	print(f"[Info]already have {TARGET_FOLDER} folder")
		# 	continue

		# if not os.path.exists( sourcePath ):
		# 	print(f"[Warnning] cant find {SOURCE_FOLDER} folder!")
		# 	continue

		# shutil.copytree(sourcePath, targetPath)
		# print(f"[Success] copy from {sourcePath} to {targetPath}")



if __name__ == '__main__':
	main()