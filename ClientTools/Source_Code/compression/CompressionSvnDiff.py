import os
import subprocess
import sys
import json
import argparse
import requests
from datetime import datetime, timedelta
from TinyPngCompression import Compression

GET_SVN_DIFF_COMMAND = r"svn log -r {`date -d '7 days ago' +%Y-%m-%d`}:HEAD -v | grep -E '\.png$|\.jpg$'"
DIFF_DAYS = 6

def parse_args():
    parser = argparse.ArgumentParser(description = "find target path svn differnce wihin 7 days")
    
    parser.add_argument("-tf", "--targetFolder", dest = "targetFolder", default = "./",                               type = str, help = "target folder path" )
    parser.add_argument("-k", "--key",           dest = "apiKey",       default = "sMts9LFKZyD1YB5zWQ9H9Jw6GvVJ2n65", type = str, help = "TinyPNG api key" )

    args = parser.parse_args()
    return args

def main(args):
    # 拼指令
    os.chdir(args.targetFolder)

    # 先update
    updateOutput = subprocess.run('svn update', shell=True, capture_output=True, text=True)
    print(updateOutput)
    print(updateOutput.stdout)

    targetFolderName = args.targetFolder.replace('\\','/').split('/')[-1]
    seven_days_ago = (datetime.now() - timedelta(days=DIFF_DAYS)).strftime('%Y-%m-%d')
    get_svn_diff_command = f"svn log -r {{{seven_days_ago}}}:HEAD -v"
    # 使用 subprocess 獲取输出
    output = subprocess.run(get_svn_diff_command, shell=True, capture_output=True, text=True)
    print(output.stdout)

    # 整理出所有圖片
    allPicList = []
    for line in output.stdout.split('\n'):
        if (line.endswith('.png') or line.endswith('.jpg')) and (not "8888" in line):
            picPath = line.split(targetFolderName)[-1]
            fullPath = os.getcwd().replace('\\','/') + picPath
            allPicList.append(fullPath)
            print(fullPath)


    compressController = Compression()
    compressController.SetKey(args.apiKey)

    # 開始轉
    for picPath in allPicList:
        res = compressController.GetCompressionRes(picPath)
        if res == "":
            # sys.exit(1)
            continue
        url = compressController.ParseUrlFromRes(res)
        if url == "":
            # sys.exit(1)
            continue
        compressController.DownloadPicWithUrl(url, picPath)

    # commit 差異
    commitOutput = subprocess.run('svn commit -m "auto commit compression picture"', shell=True, capture_output=True, text=True)
    print(commitOutput.stdout)

if __name__ == "__main__":
    args = parse_args()
    main(args)