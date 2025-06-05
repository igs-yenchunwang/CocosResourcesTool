import os
import sys
import json
import argparse
import requests

TINYPNG_COMMAND = "curl --user api:{key} --data-binary @{pic} -i https://api.tinify.com/shrink"

class Compression():
    def __init__(self):
        super(Compression, self).__init__()
        self.apiKey = ""

    def SetKey(self, key:str):
        self.apiKey = key

    # 獲取 tinyPNG api 結果  
    def GetCompressionRes(self, picPath:str)->str:
        if self.apiKey == "":
            print("[error] please retry after set apikey.")
            return ""

        # 將原本的 curl 取法改為以 requests 套件獲取 (convert tool: https://curlconverter.com/python/)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        try:
            with open(picPath, 'rb') as f:
                data = f.read()

                response = requests.post('https://api.tinify.com/shrink', headers=headers, data=data, auth=('api', self.apiKey))

                if response.status_code == 201:
                    return response.text
                else:
                    print(f"[error] api response failed {response.status_code} {response.text}")
                    return ""
        except Exception as e:
            print(f"[error] Ask response failed. {e}")
            return ""

    def ParseUrlFromRes(self, apiRes:str)->str:
        output_url = ""

        # 使用 json.loads 解析 JSON 字符串
        parsed_response = json.loads(apiRes)

        # 提取 output 字典中的 url 值
        if parsed_response['output'] and parsed_response['output']['url']:
            output_url = parsed_response['output']['url']

        return output_url

    # 以url下載圖片
    def DownloadPicWithUrl(self, url:str, downloadTarget:str='./pic.png'):
        try:
            # 獲取圖片數據
            response = requests.get(url)

            # 檢查response是否成功
            if response.status_code == 200:
                # 将图像数据写入文件
                with open(downloadTarget, 'wb') as file:
                    file.write(response.content)

                print(f"[Success] download picture to {downloadTarget}")
            else:
                print(f"[error] get picture response failed from {url}")

        except Exception as e:
            print(f"[error] Ask response failed. {e}")

# get input 
def parse_args():
    parser = argparse.ArgumentParser(description = "Use TinyPNG api to compression picture")
    
    parser.add_argument("-k", "--key",         dest = "apiKey",     default = "sMts9LFKZyD1YB5zWQ9H9Jw6GvVJ2n65", type = str, help = "TinyPNG api key" )
    parser.add_argument("-fp", "--folderPath", dest = "folderPath", default = "./",                               type = str, help = "compression all picture wtihin this folder" )
    parser.add_argument("-pp", "--picPath",    dest = "picPath",    default = ""  ,                               type = str, help = "compression only one picture" )


    args = parser.parse_args()
    return args


def main(args):
    compressController = Compression()
    compressController.SetKey(args.apiKey)

    # only one pic
    if args.picPath != "":
        res = compressController.GetCompressionRes(args.picPath)
        if res == "":
            sys.exit(1)
            return
        url = compressController.ParseUrlFromRes(res)
        if url == "":
            sys.exit(1)
            return
        compressController.DownloadPicWithUrl(url, args.picPath)

    # compression all pic in target folder
    else:
        for file in os.listdir(args.folderPath):
            if not ( ".png" in file or ".jpg" in file ):
                continue

            res = compressController.GetCompressionRes(os.path.join(args.folderPath, file))
            if res == "":
                sys.exit(1)
                return
            url = compressController.ParseUrlFromRes(res)
            if url == "":
                sys.exit(1)
                return
            compressController.DownloadPicWithUrl(url, args.picPath)

if __name__ == "__main__":
    args = parse_args()
    main(args)
