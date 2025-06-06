#!/usr/bin/env python3
"""
檢查測試環境設定
Check test environment setup
"""

import sys
import os

def check_dependencies():
    """檢查必要的依賴套件"""
    print("檢查測試環境依賴...")
    print("-" * 30)
    
    dependencies = [
        ('requests', 'HTTP requests library'),
        ('PIL', 'Python Imaging Library (Pillow)'),
        ('PyQt5', 'GUI framework (optional for full tests)')
    ]
    
    missing_deps = []
    
    for dep_name, description in dependencies:
        try:
            if dep_name == 'PIL':
                import PIL
                from PIL import Image
                print(f"✓ {dep_name} ({description}) - 已安裝")
            elif dep_name == 'PyQt5':
                try:
                    from PyQt5.QtWidgets import QApplication
                    print(f"✓ {dep_name} ({description}) - 已安裝")
                except ImportError:
                    print(f"⚠ {dep_name} ({description}) - 未安裝 (GUI 測試將跳過)")
                    continue
            else:
                __import__(dep_name)
                print(f"✓ {dep_name} ({description}) - 已安裝")
        except ImportError:
            print(f"✗ {dep_name} ({description}) - 未安裝")
            missing_deps.append(dep_name)
    
    return missing_deps

def check_source_code():
    """檢查源碼模組是否可用"""
    print("\n檢查源碼模組...")
    print("-" * 30)
    
    # 添加源碼路徑
    source_path = os.path.join(os.path.dirname(__file__), '..', 'Source_Code')
    if source_path not in sys.path:
        sys.path.insert(0, source_path)
    
    modules = [
        ('compression.TinyPngCompression', 'TinyPNG 壓縮模組'),
        ('common.ToolSetting', '設定管理模組'),
        ('common.function', '通用功能模組')
    ]
    
    missing_modules = []
    
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"✓ {module_name} ({description}) - 可用")
        except ImportError as e:
            print(f"✗ {module_name} ({description}) - 無法導入: {e}")
            missing_modules.append(module_name)
    
    return missing_modules

def check_texturepacker():
    """檢查 TexturePacker 可用性"""
    print("\n檢查 TexturePacker...")
    print("-" * 30)
    
    import subprocess
    
    try:
        result = subprocess.run(['TexturePacker', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✓ TexturePacker - 已安裝且可用")
            return True
        else:
            print("⚠ TexturePacker - 安裝但無法正常執行")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("⚠ TexturePacker - 未安裝或不在 PATH 中 (相關測試將跳過)")
        return False

def main():
    """主檢查功能"""
    print("=" * 50)
    print("CocosResourcesTool 測試環境檢查")
    print("=" * 50)
    
    # 檢查 Python 版本
    print(f"Python 版本: {sys.version}")
    print(f"Python 路徑: {sys.executable}")
    print()
    
    # 檢查依賴
    missing_deps = check_dependencies()
    
    # 檢查源碼模組
    missing_modules = check_source_code()
    
    # 檢查 TexturePacker
    has_texturepacker = check_texturepacker()
    
    # 總結報告
    print("\n" + "=" * 50)
    print("環境檢查總結")
    print("=" * 50)
    
    if not missing_deps and not missing_modules:
        print("🎉 測試環境設定完整！")
        if has_texturepacker:
            print("✓ 包含 TexturePacker，可執行完整測試")
        else:
            print("⚠ 缺少 TexturePacker，部分測試將跳過")
        print("\n可以開始執行測試：")
        print("  python3 run_all_tests.py")
        return 0
    else:
        print("❌ 測試環境設定不完整")
        
        if missing_deps:
            print(f"\n缺少依賴套件: {', '.join(missing_deps)}")
            print("請執行以下命令安裝：")
            print("  pip install -r requirements.txt")
            print("或者：")
            print(f"  pip install {' '.join(missing_deps)}")
        
        if missing_modules:
            print(f"\n缺少源碼模組: {', '.join(missing_modules)}")
            print("請確認源碼結構完整")
        
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)