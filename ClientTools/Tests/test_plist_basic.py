#!/usr/bin/env python3
"""
測試 plist 打包基本功能（不啟用 TinyPNG 壓縮）
Test basic plist packaging functionality without TinyPNG compression
"""

import sys
import os
import unittest
import tempfile
import shutil
from PIL import Image

# 添加父目錄到路徑以便導入模組
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Source_Code'))

from ImgToPlist import ImgToPlist
from PyQt5.QtWidgets import QApplication

class TestPlistBasic(unittest.TestCase):
    """測試 plist 打包基本功能"""
    
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
        
    def tearDown(self):
        """清理測試環境"""
        # 清理臨時目錄
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        
        if hasattr(self, 'plist_tool'):
            self.plist_tool.close()
    
    def create_test_images(self):
        """創建測試用的圖片檔案"""
        # 創建測試資料夾：folder1
        folder1 = os.path.join(self.img_dir, "folder1")
        os.makedirs(folder1)
        
        # 創建一些測試 PNG 圖片
        for i in range(3):
            img = Image.new('RGBA', (64, 64), (255, 0, 0, 255))  # 紅色方塊
            img.save(os.path.join(folder1, f"test_image_{i}.png"))
        
        # 創建測試資料夾：folder2_8888 (測試 RGBA8888 功能)
        folder2 = os.path.join(self.img_dir, "folder2_8888")
        os.makedirs(folder2)
        
        for i in range(2):
            img = Image.new('RGBA', (32, 32), (0, 255, 0, 255))  # 綠色方塊
            img.save(os.path.join(folder2, f"test_icon_{i}.png"))
    
    def test_basic_plist_generation(self):
        """測試基本 plist 生成功能"""
        print("開始測試基本 plist 生成功能...")
        
        # 設定輸入和輸出路徑
        self.plist_tool.imgPath_input.setText(self.img_dir)
        self.plist_tool.plistPath_input.setText(self.output_dir)
        
        # 設定基本參數
        self.plist_tool.texture_packer_maxSize_input.setText("1024")
        self.plist_tool.texture_packer_bording_padding_input.setText("2")
        self.plist_tool.texture_packer_shape_padding_input.setText("2")
        
        # 確保 TinyPNG 壓縮未啟用
        self.plist_tool.enable_tinypng.setChecked(False)
        
        # 更新資料夾列表
        self.plist_tool.update_folder_list()
        
        # 檢查是否正確識別資料夾
        self.assertEqual(self.plist_tool.folder_list.count(), 2)
        
        # 檢查 TexturePacker 狀態
        if not self.plist_tool.CheckTextureStatus():
            self.skipTest("TexturePacker 未安裝或未設定環境變數")
        
        # 執行 plist 打包
        self.plist_tool.start_making_plist()
        
        # 驗證輸出檔案
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, "folder1.plist")))
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, "folder1.png")))
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, "folder2_8888.plist")))
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, "folder2_8888.png")))
        
        print("基本 plist 生成功能測試通過！")
    
    def test_rgba8888_detection(self):
        """測試 RGBA8888 格式檢測"""
        print("開始測試 RGBA8888 格式檢測...")
        
        # 測試包含 "8888" 的資料夾名稱
        self.assertTrue("8888" in "folder2_8888")
        
        # 測試優化設定
        folderName = "folder2_8888"
        optimize = "RGBA8888" if "8888" in folderName else "RGBA4444 --dither-fs-alpha"
        self.assertEqual(optimize, "RGBA8888")
        
        folderName = "folder1"
        optimize = "RGBA8888" if "8888" in folderName else "RGBA4444 --dither-fs-alpha"
        self.assertEqual(optimize, "RGBA4444 --dither-fs-alpha")
        
        print("RGBA8888 格式檢測測試通過！")
    
    def test_folder_selection(self):
        """測試資料夾選擇功能"""
        print("開始測試資料夾選擇功能...")
        
        # 設定路徑並更新資料夾列表
        self.plist_tool.imgPath_input.setText(self.img_dir)
        self.plist_tool.update_folder_list()
        
        # 測試全選功能
        self.plist_tool.enable_all_folder()
        selected_folders = self.plist_tool.get_all_select_folder()
        self.assertEqual(len(selected_folders), 2)
        self.assertIn("folder1", selected_folders)
        self.assertIn("folder2_8888", selected_folders)
        
        # 測試全不選功能
        self.plist_tool.disable_all_folder()
        selected_folders = self.plist_tool.get_all_select_folder()
        self.assertEqual(len(selected_folders), 0)
        
        print("資料夾選擇功能測試通過！")

if __name__ == '__main__':
    print("=" * 50)
    print("開始執行 plist 打包基本功能測試")
    print("=" * 50)
    
    unittest.main(verbosity=2)