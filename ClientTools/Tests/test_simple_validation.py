#!/usr/bin/env python3
"""
簡單驗證測試 - 確保測試框架正常運作
Simple validation test to ensure the test framework works
"""

import sys
import os
import unittest

# 添加父目錄到路徑以便導入模組
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Source_Code'))

class TestSimpleValidation(unittest.TestCase):
    """簡單驗證測試"""
    
    def test_basic_imports(self):
        """測試基本模組導入"""
        print("開始測試基本模組導入...")
        
        try:
            # 測試導入 compression 模組
            from compression.TinyPngCompression import Compression
            compressor = Compression()
            self.assertIsNotNone(compressor)
            print("✓ TinyPngCompression 模組導入成功")
        except ImportError as e:
            self.fail(f"無法導入 TinyPngCompression: {e}")
        
        try:
            # 測試導入 common 模組
            from common.ToolSetting import Setting
            setting = Setting()
            self.assertIsNotNone(setting)
            print("✓ ToolSetting 模組導入成功")
        except ImportError as e:
            self.fail(f"無法導入 ToolSetting: {e}")
        
        print("基本模組導入測試通過！")
    
    def test_basic_functionality(self):
        """測試基本功能"""
        print("開始測試基本功能...")
        
        # 測試基本 Python 功能
        self.assertEqual(2 + 2, 4)
        self.assertTrue(True)
        self.assertFalse(False)
        
        # 測試字串操作
        test_string = "test_folder_8888"
        self.assertIn("8888", test_string)
        self.assertTrue(test_string.endswith("8888"))
        
        print("基本功能測試通過！")
    
    def test_file_operations(self):
        """測試檔案操作"""
        print("開始測試檔案操作...")
        
        import tempfile
        import shutil
        
        # 創建臨時目錄
        temp_dir = tempfile.mkdtemp()
        
        try:
            # 測試目錄是否存在
            self.assertTrue(os.path.exists(temp_dir))
            self.assertTrue(os.path.isdir(temp_dir))
            
            # 測試檔案建立
            test_file = os.path.join(temp_dir, "test.txt")
            with open(test_file, 'w') as f:
                f.write("test content")
            
            self.assertTrue(os.path.exists(test_file))
            
            # 測試檔案讀取
            with open(test_file, 'r') as f:
                content = f.read()
                self.assertEqual(content, "test content")
                
        finally:
            # 清理
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        
        print("檔案操作測試通過！")

if __name__ == '__main__':
    print("=" * 50)
    print("開始執行簡單驗證測試")
    print("=" * 50)
    
    unittest.main(verbosity=2)