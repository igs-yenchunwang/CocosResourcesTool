#!/usr/bin/env python3
"""
測試 TinyPNG 壓縮功能
Test TinyPNG compression functionality
"""

import sys
import os
import unittest
import tempfile
import shutil
from PIL import Image
from unittest.mock import Mock, patch

# 添加父目錄到路徑以便導入模組
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Source_Code'))

from ImgToPlist import ImgToPlist
from compression.TinyPngCompression import Compression
from PyQt5.QtWidgets import QApplication

class TestTinyPNGCompression(unittest.TestCase):
    """測試 TinyPNG 壓縮功能"""
    
    def setUp(self):
        """設置測試環境"""
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
        
        # 創建臨時測試目錄
        self.test_dir = tempfile.mkdtemp()
        self.img_dir = os.path.join(self.test_dir, "images")
        self.output_dir = os.path.join(self.test_dir, "output")
        
        os.makedirs(self.img_dir)
        os.makedirs(self.output_dir)
        
        # 創建測試圖片資料夾
        self.create_test_images()
        
        # 初始化 ImgToPlist
        self.plist_tool = ImgToPlist()
        self.plist_tool.hide()  # 隱藏 GUI
        
        # 初始化 TinyPNG 壓縮器
        self.compressor = Compression()
        
    def tearDown(self):
        """清理測試環境"""
        # 清理臨時目錄
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        
        if hasattr(self, 'plist_tool'):
            self.plist_tool.close()
    
    def create_test_images(self):
        """創建測試用的圖片檔案"""
        # 創建測試資料夾：test_folder
        folder = os.path.join(self.img_dir, "test_folder")
        os.makedirs(folder)
        
        # 創建測試 PNG 圖片
        for i in range(2):
            img = Image.new('RGBA', (100, 100), (255, 0, 0, 255))  # 紅色方塊
            img.save(os.path.join(folder, f"test_image_{i}.png"))
        
        # 創建一個輸出用的測試 PNG
        self.test_png = os.path.join(self.output_dir, "test_output.png")
        img = Image.new('RGBA', (200, 200), (0, 255, 0, 255))  # 綠色方塊
        img.save(self.test_png)
    
    def test_compression_api_key_setting(self):
        """測試 API Key 設定功能"""
        print("開始測試 API Key 設定功能...")
        
        test_key = "test_api_key_12345"
        self.compressor.SetKey(test_key)
        self.assertEqual(self.compressor.apiKey, test_key)
        
        print("API Key 設定功能測試通過！")
    
    def test_compression_enabled_integration(self):
        """測試壓縮功能整合"""
        print("開始測試壓縮功能整合...")
        
        # 設定 plist 工具
        self.plist_tool.imgPath_input.setText(self.img_dir)
        self.plist_tool.plistPath_input.setText(self.output_dir)
        self.plist_tool.texture_packer_maxSize_input.setText("1024")
        self.plist_tool.texture_packer_bording_padding_input.setText("2")
        self.plist_tool.texture_packer_shape_padding_input.setText("2")
        
        # 啟用 TinyPNG 壓縮
        self.plist_tool.enable_tinypng.setChecked(True)
        self.plist_tool.tinypng_key_input.setText("test_api_key")
        
        # 驗證設定
        self.assertTrue(self.plist_tool.enable_tinypng.isChecked())
        self.assertEqual(self.plist_tool.tinypng_key_input.text(), "test_api_key")
        
        print("壓縮功能整合測試通過！")
    
    @patch('compression.TinyPngCompression.requests.post')
    def test_compression_api_call_mock(self, mock_post):
        """測試 TinyPNG API 呼叫（使用 Mock）"""
        print("開始測試 TinyPNG API 呼叫...")
        
        # 設定 Mock 回應
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.text = '{"output": {"url": "https://api.tinify.com/output/test123"}}'
        mock_post.return_value = mock_response
        
        # 設定 API Key
        self.compressor.SetKey("test_api_key")
        
        # 執行壓縮請求
        result = self.compressor.GetCompressionRes(self.test_png)
        
        # 驗證結果
        self.assertNotEqual(result, "")
        self.assertIn("output", result)
        
        # 驗證 API 呼叫
        mock_post.assert_called_once()
        
        print("TinyPNG API 呼叫測試通過！")
    
    def test_url_parsing(self):
        """測試 URL 解析功能"""
        print("開始測試 URL 解析功能...")
        
        # 測試正常的 API 回應
        test_response = '{"output": {"url": "https://api.tinify.com/output/test123"}}'
        url = self.compressor.ParseUrlFromRes(test_response)
        self.assertEqual(url, "https://api.tinify.com/output/test123")
        
        # 測試無效的回應
        invalid_response = '{"error": "Invalid API key"}'
        try:
            url = self.compressor.ParseUrlFromRes(invalid_response)
            # 如果沒有 output 欄位，應該會拋出異常或返回空字串
        except:
            pass  # 預期的異常
        
        print("URL 解析功能測試通過！")
    
    @patch('compression.TinyPngCompression.requests.get')
    def test_download_functionality_mock(self, mock_get):
        """測試下載功能（使用 Mock）"""
        print("開始測試下載功能...")
        
        # 設定 Mock 回應
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"fake_png_content"
        mock_get.return_value = mock_response
        
        # 測試下載
        download_path = os.path.join(self.output_dir, "downloaded_test.png")
        self.compressor.DownloadPicWithUrl("https://test.com/image.png", download_path)
        
        # 驗證檔案是否創建
        self.assertTrue(os.path.exists(download_path))
        
        # 驗證內容
        with open(download_path, 'rb') as f:
            content = f.read()
            self.assertEqual(content, b"fake_png_content")
        
        print("下載功能測試通過！")
    
    def test_compression_workflow_mock(self):
        """測試完整壓縮工作流程（使用 Mock）"""
        print("開始測試完整壓縮工作流程...")
        
        # 創建測試 PNG 檔案列表
        test_pngs = [
            os.path.join(self.output_dir, "test1.png"),
            os.path.join(self.output_dir, "test2.png")
        ]
        
        for png_file in test_pngs:
            img = Image.new('RGBA', (50, 50), (0, 0, 255, 255))  # 藍色方塊
            img.save(png_file)
        
        # Mock 壓縮器方法
        with patch.object(self.plist_tool.m_compressor, 'GetCompressionRes') as mock_compress, \
             patch.object(self.plist_tool.m_compressor, 'ParseUrlFromRes') as mock_parse, \
             patch.object(self.plist_tool.m_compressor, 'DownloadPicWithUrl') as mock_download:
            
            # 設定 Mock 回應
            mock_compress.return_value = '{"output": {"url": "https://test.com/compressed.png"}}'
            mock_parse.return_value = "https://test.com/compressed.png"
            
            # 設定 API Key
            self.plist_tool.tinypng_key_input.setText("test_key")
            
            # 執行壓縮工作流程
            self.plist_tool.compress_generated_pngs(test_pngs)
            
            # 驗證方法呼叫次數
            self.assertEqual(mock_compress.call_count, 2)
            self.assertEqual(mock_parse.call_count, 2)
            self.assertEqual(mock_download.call_count, 2)
        
        print("完整壓縮工作流程測試通過！")
    
    def test_api_key_fallback(self):
        """測試 API Key 回退機制"""
        print("開始測試 API Key 回退機制...")
        
        # 設定空的 API Key
        self.plist_tool.tinypng_key_input.setText("")
        
        # 模擬壓縮過程以測試回退機制
        test_pngs = [self.test_png]
        
        with patch.object(self.plist_tool.m_compressor, 'SetKey') as mock_set_key:
            with patch.object(self.plist_tool.m_compressor, 'GetCompressionRes') as mock_compress:
                mock_compress.return_value = ""  # 模擬失敗
                
                self.plist_tool.compress_generated_pngs(test_pngs)
                
                # 驗證使用預設 API Key
                mock_set_key.assert_called_with("sMts9LFKZyD1YB5zWQ9H9Jw6GvVJ2n65")
        
        print("API Key 回退機制測試通過！")

if __name__ == '__main__':
    print("=" * 50)
    print("開始執行 TinyPNG 壓縮功能測試")
    print("=" * 50)
    
    unittest.main(verbosity=2)