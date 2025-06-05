import sys
import os
import json
from common.ToolSetting import Setting
from common.function import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

COL_MAX_SHOW_IMG = 3
SHOW_IMG_MAX = 21

WINDOWS_WIDTH = 1450
WINDOWS_HEIGHT = 700


class FileMove(QWidget):
    def __init__(self):
        super().__init__()
        # 初始化參數
        self.init_var()

        # 創建UI們
        self.create_ui()

        # 初始化應用程式視窗排版
        self.init_ui()

        # 載入存檔設定
        self.load_setting()

        self.Show()

    def init_var(self):
        self.csd_file_data = {}     # 儲存 csd檔案
        self.dynamic_img = []       # 用於存儲動態生成的 QLabel
        self.select_img = []        # 用於存儲左側選擇的 img
        self.left_tree_finish = False
        self.right_tree_finish = False

    def create_ui(self):
        # 建立元件
        self.check_box_need_change_csd = QCheckBox('是否需要更改csd中的路徑(下方填入涵蓋需要更改範圍的資料夾路徑)', self)
        self.csd_path = MLineEdit()
        self.csd_path.textChanged.connect(self.save_setting)

        self.left_label = QLabel('來源資料夾:')
        self.left_path_input = MLineEdit()
        self.left_path_confirm = QPushButton('確定')
        self.left_browse_button = QPushButton('瀏覽')
        self.left_tree_view = QTreeView()
        # 啟用多選
        self.left_tree_view.setSelectionMode(QTreeView.MultiSelection)

        self.right_label = QLabel('目標資料夾:')
        self.right_path_input = MLineEdit()
        self.right_path_confirm = QPushButton('確定')
        self.right_browse_button = QPushButton('瀏覽')
        self.right_tree_view = QTreeView()

        self.log_label = QLabel('LOG:')
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)

        self.png_view_label = QLabel('預覽:')
        self.png_view = QLabel(self)
        self.png_view.setFixedSize(200, 1)

        # 設定按鈕點擊事件處理函式
        self.check_box_need_change_csd.clicked.connect(self.save_setting)
        self.left_browse_button.clicked.connect(self.browse_folder_left)
        self.right_browse_button.clicked.connect(self.browse_folder_right)
        self.left_path_confirm.clicked.connect(self.path_confirm_left)
        self.right_path_confirm.clicked.connect(self.path_confirm_right)

        # 設定左邊 QTreeView 的雙擊事件處理函式
        # self.left_tree_view.clicked.connect(self.view_multi_png)
        # self.left_tree_view.doubleClicked.connect(self.confirm_move_file)

        self.right_tree_view.clicked.connect(self.view_single_png)

        # 傳送btn
        self.start_move_btn = QPushButton('>>')
        self.start_move_btn.setFixedWidth(30)
        self.start_move_btn.clicked.connect(self.confirm_move_file)
        
    def init_ui(self):
        # 設定主佈局
        left_input_layout = QHBoxLayout()
        left_input_layout.addWidget(self.left_path_input)
        left_input_layout.addWidget(self.left_path_confirm)
        left_input_layout.addWidget(self.left_browse_button)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.left_label)
        left_layout.addLayout(left_input_layout)
        left_layout.addWidget(self.left_tree_view)

        right_input_layout = QHBoxLayout()
        right_input_layout.addWidget(self.right_path_input)
        right_input_layout.addWidget(self.right_path_confirm)
        right_input_layout.addWidget(self.right_browse_button)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.right_label)
        right_layout.addLayout(right_input_layout)
        right_layout.addWidget(self.right_tree_view)

        log_layout = QVBoxLayout()
        log_layout.addWidget(self.log_label)
        log_layout.addWidget(self.log_text_edit)

        move_main_layout = QHBoxLayout()
        move_main_layout.addLayout(left_layout, 2)
        move_main_layout.addWidget(self.start_move_btn)
        move_main_layout.addLayout(right_layout, 2)
        move_main_layout.addLayout(log_layout, 2)

        setting_layout = QVBoxLayout()
        setting_layout.addWidget(self.check_box_need_change_csd)
        setting_layout.addWidget(self.csd_path)

        self.img_container = QVBoxLayout()

        view_layout = QVBoxLayout()
        view_layout.addWidget(self.png_view_label)
        view_layout.addLayout(self.img_container)
        view_layout.addWidget(self.png_view)

        main_layout = QVBoxLayout()
        main_layout.addLayout(setting_layout)
        main_layout.addLayout(move_main_layout)

        root_layout = QHBoxLayout()
        root_layout.addLayout(main_layout)
        root_layout.addLayout(view_layout)

        # 設定視窗佈局
        self.setLayout(root_layout)

        # 設定視窗屬性
        self.setWindowTitle('檔案移動工具')
        self.setGeometry(200, 100, WINDOWS_WIDTH, WINDOWS_HEIGHT)

    def Show(self):
        self.show()

    def Hide(self):
        self.hide()

    def view_multi_png(self):
        print("view_multi_png(self, index:int):")
        # 獲取選擇模型
        selection_model = self.left_tree_view.selectionModel()

        # 獲取所選項目的索引
        selected_indexes = selection_model.selectedIndexes()

        # 列印所選項目的路徑
        selected_paths = []
        for index in selected_indexes:
            path = self.left_tree_view.model().filePath(index)
            if not path in selected_paths:
                selected_paths.append(path)
                # print(path)
 
        self.select_img = selected_paths
        self.show_png(selected_paths)

    def view_single_png(self, index:int):
        # 左側清除選擇
        self.right_tree_view.selectionModel().clearSelection()

        # 當樹狀視圖中的檔案被點擊時觸發
        file_path = self.right_tree_view.model().filePath(index)

        if file_path.lower().endswith('.png'):
            self.show_png([file_path])

    def show_png(self, pngList:list):
        # 手動刪除先前的 QLabel
        for label in self.dynamic_img:
            label.setParent(None)

        # 清除保存的 QLabel 引用
        self.dynamic_img = []

        # 動態生成 QLabel 並添加到布局中
        self.img_col = []
        imgCount = 0
        for pngName in pngList:
            col = int(imgCount / COL_MAX_SHOW_IMG)
            if len(self.img_col) <= col:
                self.img_col.append(QHBoxLayout())
                self.img_container.addLayout(self.img_col[col])

            pngLabel = QLabel(self)
            pngLabel.setFixedSize(80, 80)
            pixmap = QPixmap(pngName)
            pngLabel.setPixmap(pixmap.scaled(pngLabel.size(), Qt.KeepAspectRatio))

            self.dynamic_img.append(pngLabel)
            self.img_col[col].addWidget(pngLabel)
            imgCount = imgCount + 1
            if imgCount >= SHOW_IMG_MAX:
                break

    def browse_folder_left(self):
        startPath =  self.left_path_input.text() if url_format_check(self.left_path_input.text()) else "~"
        folder_path = QFileDialog.getExistingDirectory(self, '選擇來源資料夾', startPath)
        if folder_path:
            self.left_path_input.setText(folder_path)
            self.show_folder_contents(folder_path, self.left_tree_view)
            self.left_tree_view.selectionModel().selectionChanged.connect(self.view_multi_png)
            self.left_tree_finish = True

    def browse_folder_right(self):
        startPath =  self.right_path_input.text() if url_format_check(self.right_path_input.text()) else "~"
        folder_path = QFileDialog.getExistingDirectory(self, '選擇目標資料夾', startPath)
        if folder_path:
            self.right_path_input.setText(folder_path)
            self.show_folder_contents(folder_path, self.right_tree_view)
            self.right_tree_finish = True

    def path_confirm_left(self):
        folder_path = self.left_path_input.text()
        if folder_path and folder_path != "":
            self.show_folder_contents(folder_path, self.left_tree_view)    
            self.left_tree_view.selectionModel().selectionChanged.connect(self.view_multi_png) 
            self.left_tree_finish = True

    def path_confirm_right(self):
        folder_path = self.right_path_input.text()
        if folder_path and folder_path != "":
            self.show_folder_contents(folder_path, self.right_tree_view)        
            self.right_tree_finish = True

    # 顯示資料夾內容
    def show_folder_contents(self, folder_path:str, tree_view:QTreeView):
        model = QFileSystemModel()
        model.setRootPath(folder_path)
        tree_view.setModel(model)
        tree_view.setRootIndex(model.index(folder_path))

    # 確定移動檔案
    def confirm_move_file(self):
        if not self.right_tree_finish or not self.left_tree_finish:
            ret = QMessageBox.information(
            self, '提示',
            '請填寫來源路徑與目標路徑',
            QMessageBox.Ok)
            return

        # 取得右邊資料夾路徑
        destination_folder = self.right_path_input.text()

        reply = QMessageBox.question(self, '確認移動檔案',
                                     f'是否移動檔案?',
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes and self.check_box_need_change_csd.isChecked() and(not self.csd_path.text() or self.csd_path.text() == ""):
            QMessageBox.question(self, "沒有填入csd路徑", QMessageBox.Ok)

        elif reply == QMessageBox.Yes:
            for file_path in self.select_img:
                # 取得檔案的基本名稱（不含路徑）
                file_name = os.path.basename(file_path)

                # 確認移動檔案
                new_path = os.path.join(destination_folder, file_name)
                os.rename(file_path, new_path)
                self.show_folder_contents(destination_folder, self.right_tree_view)

                # 將日誌訊息輸出到 QTextEdit
                log_message = f'移動檔案: {file_name} to {destination_folder}\n'
                self.log_text_edit.append(log_message)

                if self.check_box_need_change_csd.isChecked():
                    self.change_csd_content(file_name, file_path, destination_folder)     
    
    # 改變csd 中相關路徑
    def change_csd_content(self, file_name, source_folder, target_folder):
        # 讀取csd資料
        if not self.csd_file_data:
            self.csd_file_data = self.find_csd_files(self.csd_path.text())

        for csdName, fileConent in self.csd_file_data.items():
            if file_name in fileConent:
                oldPath = source_folder.split('/')[-2] + "/" + file_name
                newPath = target_folder.split('\\')[-1] + "/" + file_name
                fileConent = fileConent.replace( oldPath, newPath )
                # 覆蓋寫回檔案
                with open(csdName, 'w', encoding='utf-8') as file:
                    file.write(fileConent)
                log_message = f'更改檔案: {csdName} 中跟{file_name}有關的路徑\n'
                self.log_text_edit.append(log_message)

    def find_csd_files(self, path:str)->dict:
        csd_files = {}  # 存儲找到的 .csd 文件的列表

        def search_folder(folder_path):
            try:
                # 使用 os.listdir() 获取文件夹下的所有文件和文件夹
                items = os.listdir(folder_path)
                
                for item in items:
                    item_path = os.path.join(folder_path, item)
                    
                    # 如果是文件夹，递归搜索
                    if os.path.isdir(item_path):
                        search_folder(item_path)
                    
                    # 如果是 .csd 文件，加入列表
                    elif item.endswith('.csd'):
                        # 讀取檔案內容
                        try:
                            with open(item_path, 'r', encoding='utf-8') as file:
                                content = file.read()
                                csd_files[item_path] = content
                        except:
                            print(f'{item_path} cant read')

                        
            except OSError as e:
                print("Error accessing folder e:{}".format(e))

        # 开始搜索
        search_folder(path)

        return csd_files

    def load_setting(self):
        self.m_settingMgr = Setting()
        self.m_setting = self.m_settingMgr.get_setting()

        self.check_box_need_change_csd.setChecked(self.m_setting["check_change_csd"])
        self.csd_path.setText(self.m_setting["change_csd_path"])

    def save_setting(self):
        self.m_setting["check_change_csd"] = self.check_box_need_change_csd.isChecked()
        self.m_setting["change_csd_path"] = self.csd_path.text()

        self.m_settingMgr.save_setting(self.m_setting)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileMove()
    sys.exit(app.exec_())
