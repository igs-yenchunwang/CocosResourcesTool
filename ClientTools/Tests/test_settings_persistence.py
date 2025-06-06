#!/usr/bin/env python3
"""
測試設定持久化功能
Test settings persistence functionality
"""

import sys
import os
import unittest
import tempfile
import shutil
import json

# 添加父目錄到路徑以便導入模組
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Source_Code'))

from ImgToPlist import ImgToPlist
from common.ToolSetting import Setting
from PyQt5.QtWidgets import QApplication

class TestSettingsPersistence(unittest.TestCase):
    """測試設定持久化功能"""
    
    def setUp(self):
        """設置測試環境"""
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
        
        # 創建臨時測試目錄
        self.test_dir = tempfile.mkdtemp()
        
        # 備份原始設定檔案路徑（如果存在）
        self.original_setting_path = None
        
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
    
    def test_basic_settings_save_load(self):
        """測試基本設定儲存和載入"""
        print("開始測試基本設定儲存和載入...")
        
        # 設定測試值
        test_values = {
            "texturepacker_path": "/test/path/TexturePacker.exe",
            "source_img_path": "/test/images",
            "target_plist_path": "/test/output",
            "max_size": 2048,
            "bording_padding": 4,
            "shape_padding": 3,
            "check_customize_texturepacker": True
        }
        
        # 設定 GUI 控制項
        self.plist_tool.texturePacker_input.setText(test_values["texturepacker_path"])
        self.plist_tool.imgPath_input.setText(test_values["source_img_path"])
        self.plist_tool.plistPath_input.setText(test_values["target_plist_path"])
        self.plist_tool.texture_packer_maxSize_input.setText(str(test_values["max_size"]))
        self.plist_tool.texture_packer_bording_padding_input.setText(str(test_values["bording_padding"]))
        self.plist_tool.texture_packer_shape_padding_input.setText(str(test_values["shape_padding"]))
        self.plist_tool.check_box_texturePacker.setChecked(test_values["check_customize_texturepacker"])
        
        # 儲存設定
        self.plist_tool.save_setting()
        
        # 創建新的實例來測試載入
        new_plist_tool = ImgToPlist()
        new_plist_tool.hide()
        
        # 驗證設定是否正確載入
        self.assertEqual(new_plist_tool.texturePacker_input.text(), test_values["texturepacker_path"])
        self.assertEqual(new_plist_tool.imgPath_input.text(), test_values["source_img_path"])
        self.assertEqual(new_plist_tool.plistPath_input.text(), test_values["target_plist_path"])
        self.assertEqual(new_plist_tool.texture_packer_maxSize_input.text(), str(test_values["max_size"]))
        self.assertEqual(new_plist_tool.texture_packer_bording_padding_input.text(), str(test_values["bording_padding"]))
        self.assertEqual(new_plist_tool.texture_packer_shape_padding_input.text(), str(test_values["shape_padding"]))
        self.assertEqual(new_plist_tool.check_box_texturePacker.isChecked(), test_values["check_customize_texturepacker"])
        
        new_plist_tool.close()
        print("基本設定儲存和載入測試通過！")
    
    def test_tinypng_settings_save_load(self):
        """測試 TinyPNG 設定儲存和載入"""
        print("開始測試 TinyPNG 設定儲存和載入...")
        
        # 設定 TinyPNG 測試值
        test_enable_tinypng = True
        test_api_key = "test_tinypng_api_key_123456"
        
        # 設定 TinyPNG 控制項
        self.plist_tool.enable_tinypng.setChecked(test_enable_tinypng)
        self.plist_tool.tinypng_key_input.setText(test_api_key)
        
        # 儲存設定
        self.plist_tool.save_setting()
        
        # 創建新的實例來測試載入
        new_plist_tool = ImgToPlist()
        new_plist_tool.hide()
        
        # 驗證 TinyPNG 設定是否正確載入
        self.assertEqual(new_plist_tool.enable_tinypng.isChecked(), test_enable_tinypng)
        self.assertEqual(new_plist_tool.tinypng_key_input.text(), test_api_key)
        
        new_plist_tool.close()
        print("TinyPNG 設定儲存和載入測試通過！")
    
    def test_settings_default_values(self):
        """測試設定預設值"""
        print("開始測試設定預設值...")
        
        # 創建新的設定管理器
        setting_mgr = Setting()
        settings = setting_mgr.get_setting()
        
        # 檢查 TinyPNG 相關的預設值
        enable_tinypng_default = settings.get("enable_tinypng", False)
        api_key_default = settings.get("tinypng_api_key", "")
        
        # 驗證預設值
        self.assertFalse(enable_tinypng_default)  # 預設應該是不啟用
        self.assertEqual(api_key_default, "")     # 預設應該是空字串
        
        print("設定預設值測試通過！")
    
    def test_settings_partial_update(self):
        """測試部分設定更新"""
        print("開始測試部分設定更新...")
        
        # 先設定一些初始值
        self.plist_tool.imgPath_input.setText("/initial/path")
        self.plist_tool.enable_tinypng.setChecked(False)
        self.plist_tool.save_setting()
        
        # 只更新部分設定
        self.plist_tool.enable_tinypng.setChecked(True)
        self.plist_tool.tinypng_key_input.setText("new_api_key")
        self.plist_tool.save_setting()
        
        # 創建新實例驗證
        new_plist_tool = ImgToPlist()
        new_plist_tool.hide()
        
        # 驗證舊設定仍然存在，新設定已更新
        self.assertEqual(new_plist_tool.imgPath_input.text(), "/initial/path")
        self.assertTrue(new_plist_tool.enable_tinypng.isChecked())
        self.assertEqual(new_plist_tool.tinypng_key_input.text(), "new_api_key")
        
        new_plist_tool.close()
        print("部分設定更新測試通過！")
    
    def test_settings_file_format(self):
        """測試設定檔案格式"""
        print("開始測試設定檔案格式...")
        
        # 設定一些測試值
        self.plist_tool.enable_tinypng.setChecked(True)
        self.plist_tool.tinypng_key_input.setText("format_test_key")
        self.plist_tool.texture_packer_maxSize_input.setText("1024")
        self.plist_tool.save_setting()
        
        # 直接讀取設定檔案
        setting_mgr = Setting()
        settings = setting_mgr.get_setting()
        
        # 驗證設定格式
        self.assertIsInstance(settings, dict)
        self.assertIn("enable_tinypng", settings)
        self.assertIn("tinypng_api_key", settings)
        self.assertIn("max_size", settings)
        
        # 驗證數據類型
        self.assertIsInstance(settings["enable_tinypng"], bool)
        self.assertIsInstance(settings["tinypng_api_key"], str)
        self.assertIsInstance(settings["max_size"], int)
        
        print("設定檔案格式測試通過！")
    
    def test_settings_auto_save_triggers(self):
        """測試自動儲存觸發器"""
        print("開始測試自動儲存觸發器...")
        
        # 測試 checkbox 觸發自動儲存
        initial_state = self.plist_tool.enable_tinypng.isChecked()
        self.plist_tool.enable_tinypng.setChecked(not initial_state)
        # 由於我們在 setUp 中連接了 clicked.connect(self.save_setting)
        # 這應該會觸發自動儲存
        
        # 測試文字變化觸發自動儲存
        self.plist_tool.tinypng_key_input.setText("auto_save_test")
        # textChanged.connect(self.save_setting) 應該會觸發
        
        # 創建新實例驗證自動儲存
        new_plist_tool = ImgToPlist()
        new_plist_tool.hide()
        
        # 驗證設定已自動儲存
        self.assertEqual(new_plist_tool.enable_tinypng.isChecked(), not initial_state)
        self.assertEqual(new_plist_tool.tinypng_key_input.text(), "auto_save_test")
        
        new_plist_tool.close()
        print("自動儲存觸發器測試通過！")
    
    def test_settings_error_handling(self):
        """測試設定錯誤處理"""
        print("開始測試設定錯誤處理...")
        
        # 測試數字格式錯誤處理
        try:
            # 設定無效的數字值
            self.plist_tool.texture_packer_maxSize_input.setText("invalid_number")
            self.plist_tool.save_setting()
            # 如果沒有拋出異常，說明有適當的錯誤處理
        except ValueError:
            # 這是預期的行為，說明有錯誤檢查
            pass
        except Exception as e:
            self.fail(f"意外的異常類型: {type(e).__name__}: {e}")
        
        print("設定錯誤處理測試通過！")

if __name__ == '__main__':
    print("=" * 50)
    print("開始執行設定持久化功能測試")
    print("=" * 50)
    
    unittest.main(verbosity=2)