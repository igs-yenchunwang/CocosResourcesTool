# Pull Request: 優化包plist功能：整合TinyPNG壓縮

## 🎯 功能概述

本PR優化了CocosResourcesTool專案中的"以資料夾打包plist"功能，整合了TinyPNG圖片壓縮功能。現在在生成plist文件後，可以自動對生成的PNG圖片進行壓縮，大幅減少檔案大小。

## ✨ 主要改進

### 🖼️ TinyPNG壓縮整合
- ✅ 在plist打包完成後自動對生成的PNG檔案進行TinyPNG壓縮
- ✅ 大幅減少PNG檔案大小，節省儲存空間和傳輸時間
- ✅ 透過UI勾選方式啟用，使用簡便

### 🔐 API Key管理
- ✅ 新增TinyPNG API Key設置界面
- ✅ API Key輸入框採用密碼模式隱藏顯示，提升安全性
- ✅ API Key設置持久化保存到配置文件

### 📝 錯誤處理與日誌
- ✅ 壓縮過程中提供詳細的進度和結果日誌
- ✅ 當API Key未設定或壓縮失敗時，提供清楚的錯誤提示
- ✅ 容錯機制：即使壓縮失敗，不會影響plist的正常生成

## 🛠️ 技術實現

### 修改的檔案
- `ClientTools/Source_Code/ImgToPlist.py` - 主要功能實現
- `ClientTools/Source_Code/common/ToolSetting.py` - 設置管理

### 新增方法
- `compress_png_with_tinypng()` - PNG壓縮核心方法
- UI元素：TinyPNG壓縮選項開關、API Key輸入框

### 整合方式
- 完全整合在現有的plist打包流程中
- 不影響原有功能的穩定性
- 可選擇性啟用，保持向後兼容

## 🎯 使用方式

1. **設置API Key**
   - 打開ImgToPlist工具
   - 點擊"<<更多"按鈕展開選項
   - 勾選"啟用 TinyPNG 壓縮"
   - 在"TinyPNG API Key"欄位輸入API密鑰

2. **執行打包與壓縮**
   - 設置img資料夾路徑和plist輸出路徑
   - 確保已勾選"啟用 TinyPNG 壓縮"
   - 點擊"開始包plist"
   - 工具會自動完成plist打包和PNG壓縮

## ✅ 測試狀況

- [x] 語法檢查通過（Python編譯檢查）
- [x] 功能邏輯完整性檢查
- [x] UI元素正確整合
- [x] 設置保存和讀取功能正常
- [x] 錯誤處理機制完備

## 🔄 影響範圍

- **向後兼容**: ✅ 完全向後兼容，不影響現有使用者
- **新功能**: ✅ 可選擇啟用，不強制使用
- **穩定性**: ✅ 不影響原有plist打包功能
- **性能**: ✅ 僅在啟用壓縮時才執行相關操作

## 📁 相關文件

- `FEATURE_SUMMARY.md` - 詳細功能總結文檔
- 主要修改在 `ImgToPlist.py` 和 `ToolSetting.py`

## 🎉 預期效益

1. **效率提升**: 自動化壓縮流程，節省手動操作時間
2. **檔案減少**: PNG檔案大小平均減少50-80%
3. **儲存節省**: 大幅減少專案儲存空間需求
4. **傳輸優化**: 更快的檔案傳輸和部署速度

---

請審核此PR，如有任何問題或建議，歡迎留言討論！