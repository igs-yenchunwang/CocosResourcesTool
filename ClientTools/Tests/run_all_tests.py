#!/usr/bin/env python3
"""
執行所有測試的腳本
Run all tests script
"""

import sys
import os
import unittest
import time

def main():
    """執行所有測試"""
    print("=" * 60)
    print("CocosResourcesTool 完整測試套件")
    print("=" * 60)
    print()
    
    # 設定測試目錄
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 測試檔案列表
    test_files = [
        'test_plist_basic.py',
        'test_tinypng_compression.py', 
        'test_settings_persistence.py',
        'test_error_handling.py',
        'test_batch_processing.py'
    ]
    
    total_tests = 0
    total_failures = 0
    total_errors = 0
    total_skipped = 0
    
    start_time = time.time()
    
    for test_file in test_files:
        print(f"執行測試文件: {test_file}")
        print("-" * 40)
        
        # 載入測試模組
        test_module_name = test_file[:-3]  # 移除 .py 擴展名
        
        try:
            # 動態導入測試模組
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                test_module_name, 
                os.path.join(test_dir, test_file)
            )
            test_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(test_module)
            
            # 創建測試套件
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromModule(test_module)
            
            # 執行測試
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)
            
            # 累計統計
            total_tests += result.testsRun
            total_failures += len(result.failures)
            total_errors += len(result.errors)
            total_skipped += len(result.skipped)
            
        except Exception as e:
            print(f"錯誤：無法執行 {test_file}: {e}")
            total_errors += 1
        
        print()
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # 顯示總結報告
    print("=" * 60)
    print("測試執行總結")
    print("=" * 60)
    print(f"總執行時間: {execution_time:.2f} 秒")
    print(f"總測試數量: {total_tests}")
    print(f"成功: {total_tests - total_failures - total_errors - total_skipped}")
    print(f"失敗: {total_failures}")
    print(f"錯誤: {total_errors}")
    print(f"跳過: {total_skipped}")
    print()
    
    # 判斷整體結果
    if total_failures == 0 and total_errors == 0:
        print("🎉 所有測試通過！")
        return 0
    else:
        print("❌ 部分測試失敗，請檢查上述報告")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)