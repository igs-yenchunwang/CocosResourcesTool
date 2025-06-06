# CocosResourcesTool 測試說明文件

## 概述

本目錄包含了針對 CocosResourcesTool 中 plist 打包和 TinyPNG 壓縮整合功能的完整測試套件。

## 測試結構

```
Tests/
├── README.md                     # 測試說明文件（本文件）
├── test_plist_basic.py          # 基本 plist 打包功能測試
├── test_tinypng_compression.py  # TinyPNG 壓縮功能測試
├── test_settings_persistence.py # 設定持久化測試
├── test_error_handling.py       # 錯誤處理機制測試
├── test_batch_processing.py     # 批次處理功能測試
├── test_data/                   # 測試資料目錄
└── test_output/                 # 測試輸出目錄
```

## 測試涵蓋範圍

### 1. 基本 plist 打包功能測試 (`test_plist_basic.py`)

**測試目標：** 驗證未啟用 TinyPNG 壓縮時的基本 plist 打包功能

**測試項目：**
- ✅ 基本 plist 生成功能
- ✅ RGBA8888 格式檢測（資料夾名稱包含 "8888"）
- ✅ 資料夾選擇功能（全選/全不選）
- ✅ 輸出檔案驗證（.plist 和 .png 檔案）

**執行方式：**
```bash
cd ClientTools/Tests
python test_plist_basic.py
```

### 2. TinyPNG 壓縮功能測試 (`test_tinypng_compression.py`)

**測試目標：** 驗證 TinyPNG 壓縮功能的完整工作流程

**測試項目：**
- ✅ API Key 設定功能
- ✅ 壓縮功能整合
- ✅ TinyPNG API 呼叫（使用 Mock）
- ✅ URL 解析功能
- ✅ 下載功能（使用 Mock）
- ✅ 完整壓縮工作流程
- ✅ API Key 回退機制

**執行方式：**
```bash
cd ClientTools/Tests
python test_tinypng_compression.py
```

### 3. 設定持久化測試 (`test_settings_persistence.py`)

**測試目標：** 驗證應用程式設定的儲存和載入功能

**測試項目：**
- ✅ 基本設定儲存和載入
- ✅ TinyPNG 設定儲存和載入
- ✅ 設定預設值驗證
- ✅ 部分設定更新
- ✅ 設定檔案格式驗證
- ✅ 自動儲存觸發器
- ✅ 設定錯誤處理

**執行方式：**
```bash
cd ClientTools/Tests
python test_settings_persistence.py
```

### 4. 錯誤處理機制測試 (`test_error_handling.py`)

**測試目標：** 驗證各種錯誤情況下的處理機制

**測試項目：**
- ✅ 無效路徑處理
- ✅ 缺少 TexturePacker 的處理
- ✅ 空輸入驗證
- ✅ 壓縮 API 錯誤處理
- ✅ 網路錯誤處理
- ✅ API 回應錯誤處理
- ✅ 無效 JSON 回應處理
- ✅ 工作流程中的壓縮失敗處理
- ✅ 下載錯誤處理
- ✅ 異常處理

**執行方式：**
```bash
cd ClientTools/Tests
python test_error_handling.py
```

### 5. 批次處理功能測試 (`test_batch_processing.py`)

**測試目標：** 驗證多資料夾批次處理功能

**測試項目：**
- ✅ 多資料夾 plist 生成
- ✅ 選擇性資料夾處理
- ✅ 批次壓縮工作流程
- ✅ 混合成功失敗的批次處理
- ✅ 大批次處理效能
- ✅ 混合 RGBA 格式批次處理
- ✅ 批次處理中斷機制

**執行方式：**
```bash
cd ClientTools/Tests
python test_batch_processing.py
```

## 執行所有測試

### 方式一：逐個執行
```bash
cd ClientTools/Tests
python test_plist_basic.py
python test_tinypng_compression.py
python test_settings_persistence.py
python test_error_handling.py
python test_batch_processing.py
```

### 方式二：使用 unittest discover
```bash
cd ClientTools
python -m unittest discover Tests -v
```

### 方式三：使用測試運行腳本
```bash
cd ClientTools/Tests
python run_all_tests.py
```

## 測試環境需求

### 系統需求
- Python 3.6+
- PyQt5
- PIL (Pillow)
- requests

### 可選需求
- TexturePacker（用於完整功能測試）
- 有效的 TinyPNG API Key（用於實際 API 測試）

### 安裝依賴

#### 方式一：使用 requirements.txt
```bash
pip install -r requirements.txt
```

#### 方式二：手動安裝
```bash
pip install PyQt5 Pillow requests
```

#### 方式三：使用 conda（如果您使用 Anaconda）
```bash
conda install requests pillow
conda install -c anaconda pyqt
```

## 測試資料

測試會自動建立和清理臨時測試資料，包括：
- 測試圖片檔案（PNG 格式）
- 測試資料夾結構
- 暫存設定檔案

## Mock 和實際測試

### Mock 測試
大部分涉及外部服務（TinyPNG API、檔案系統操作）的測試都使用 Mock 來確保：
- 測試執行速度
- 測試穩定性
- 不依賴外部服務

### 實際測試
部分基本功能測試會進行實際的檔案操作來驗證完整功能。

## 測試結果解讀

### 成功輸出範例
```
======================================================================
開始執行 plist 打包基本功能測試
======================================================================
test_basic_plist_generation (__main__.TestPlistBasic) ... ok
test_folder_selection (__main__.TestPlistBasic) ... ok
test_rgba8888_detection (__main__.TestPlistBasic) ... ok

----------------------------------------------------------------------
Ran 3 tests in 2.345s

OK
```

### 失敗處理
如果測試失敗，請檢查：
1. 是否安裝了所有必要的依賴
2. TexturePacker 是否正確安裝（如適用）
3. 測試環境是否有足夠的檔案系統權限

## 持續整合

這些測試設計為可以整合到 CI/CD 流程中：
- 所有測試都是自動化的
- 使用 Mock 減少外部依賴
- 提供詳細的測試報告

## 測試擴展

如需新增測試：
1. 在相應的測試檔案中新增測試方法
2. 遵循現有的命名慣例 `test_功能名稱`
3. 提供清楚的測試說明和驗證邏輯
4. 更新本文件的測試涵蓋範圍

## 已知限制

1. **TexturePacker 依賴：** 部分測試需要安裝 TexturePacker，如未安裝會跳過相關測試
2. **GUI 測試限制：** 由於使用 PyQt5，某些 GUI 相關測試可能在無頭環境中需要特殊配置
3. **平台相依性：** 檔案路徑和某些系統操作可能在不同作業系統間有差異

## 貢獻指南

如需改進測試：
1. 確保新的測試遵循現有模式
2. 提供充分的測試說明
3. 考慮各種邊緣情況
4. 更新相關文件

---

**注意：** 這些測試是為了確保 plist 打包和 TinyPNG 壓縮整合功能的品質和穩定性。定期執行這些測試有助於及早發現和修復問題。