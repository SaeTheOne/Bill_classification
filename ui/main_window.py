import os
import glob
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QLabel, QTextEdit, QProgressBar, QTabWidget,
    QFileDialog, QMessageBox, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from core.category_manager import CategoryManager, CONFIG_FILE
from core.worker import ProcessingWorker
from ui.widgets import FileDropListWidget
from ui.category_dialog import CategoryDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.manager = CategoryManager()
        self.worker = None
        self.setWindowTitle("智能账单分类助手")
        
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        width = int(screen_geometry.width() * 0.35)
        height = int(screen_geometry.height() * 0.45)
        self.resize(width, height)
        self.setMinimumSize(500, 400)
        
        self._init_menu()
        self._init_ui()
        self._update_preview()

    def _init_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("文件")
        open_action = QAction("打开文件夹", self)
        open_action.triggered.connect(self._open_folder)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        cat_menu = menubar.addMenu("分类管理")
        manage_action = QAction("管理分类规则", self)
        manage_action.triggered.connect(self._open_category_manager)
        cat_menu.addAction(manage_action)
        reload_action = QAction("重新加载配置", self)
        reload_action.triggered.connect(self._reload_config)
        cat_menu.addAction(reload_action)

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(5)

        self.tab_widget = QTabWidget()
        file_tab = QWidget()
        file_layout = QVBoxLayout(file_tab)
        file_layout.setSpacing(5)

        file_group = QGroupBox("待处理文件")
        file_group_layout = QVBoxLayout(file_group)
        file_group_layout.setSpacing(3)
        file_group_layout.addWidget(QLabel("💡 拖拽文件/文件夹到下方，或点击按钮添加"))

        self.file_list = FileDropListWidget()
        self.file_list.setMinimumHeight(80)
        file_group_layout.addWidget(self.file_list)

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("添加文件")
        self.btn_add.clicked.connect(self._add_files)
        self.btn_add_folder = QPushButton("添加文件夹")
        self.btn_add_folder.clicked.connect(self._add_folder)
        self.btn_clear = QPushButton("清空")
        self.btn_clear.clicked.connect(self.file_list.clear)
        self.btn_start = QPushButton("开始处理")
        self.btn_start.setStyleSheet("background-color: #0078d7; color: white; font-weight: bold;")
        self.btn_start.clicked.connect(self._start_processing)

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_add_folder)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_start)
        file_group_layout.addLayout(btn_layout)
        file_layout.addWidget(file_group)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setMaximumHeight(15)
        file_layout.addWidget(self.progress)

        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("color: #666;")
        file_layout.addWidget(self.status_label)

        self.tab_widget.addTab(file_tab, "文件处理")

        rule_tab = QWidget()
        rule_layout = QVBoxLayout(rule_tab)
        self.rule_preview = QTextEdit()
        self.rule_preview.setReadOnly(True)
        self.rule_preview.setMaximumHeight(200)
        rule_layout.addWidget(self.rule_preview)
        self.tab_widget.addTab(rule_tab, "规则概览")

        layout.addWidget(self.tab_widget)
        self.statusBar().showMessage("就绪")

    def _update_preview(self):
        if not self.manager.categories:
            self.rule_preview.setText("未加载配置")
            return
        text = f"已加载: {CONFIG_FILE}\n\n"
        for main_cat, sub_cats in self.manager.categories.items():
            text += f"【{main_cat}】\n"
            if isinstance(sub_cats, dict):
                for sub_cat, rules in sub_cats.items():
                    if rules is None:
                        rules_str = ""
                    else:
                        rules_str = str(rules)
                    if len(rules_str) > 40:
                        display = rules_str[:40] + "..."
                    else:
                        display = rules_str if rules_str else "(空规则)"
                    text += f"  └─ {sub_cat}: {display}\n"
            text += "\n"
        self.rule_preview.setText(text)

    def _reload_config(self):
        if self.manager.load():
            self._update_preview()
            QMessageBox.information(self, "成功", "配置已重新加载")
        else:
            QMessageBox.warning(self, "错误", "加载失败")

    def _open_category_manager(self):
        dialog = CategoryDialog(self.manager, self)
        if dialog.exec():
            self._update_preview()

    def _add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "选择账单文件", "",
            "支持的格式 (*.xlsx *.xls *.csv);;Excel (*.xlsx *.xls);;CSV (*.csv)"
        )
        if files:
            self.file_list.add_files(files)

    def _add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder:
            self.file_list.add_files([folder])

    def _open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择包含账单的文件夹")
        if folder:
            files = []
            for ext in ['*.csv', '*.xlsx', '*.xls']:
                files.extend(glob.glob(os.path.join(folder, ext)))
            if files:
                self.file_list.add_files(files)
                QMessageBox.information(self, "成功", f"找到 {len(files)} 个文件")
            else:
                QMessageBox.warning(self, "提示", "未找到支持的文件")

    def _get_file_paths(self):
        paths = []
        for i in range(self.file_list.count()):
            text = self.file_list.item(i).text()
            if text.startswith("[文件夹] "):
                paths.append(text.replace("[文件夹] ", ""))
            else:
                paths.append(text)
        return paths

    def _start_processing(self):
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "提示", "请先添加文件")
            return
        if not self.manager.categories:
            QMessageBox.warning(self, "提示", "未加载分类配置")
            return
        file_paths = self._get_file_paths()
        self.btn_start.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.status_label.setText("处理中...")
        self.statusBar().showMessage("正在处理...")
        self.worker = ProcessingWorker(file_paths)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.status.connect(self.status_label.setText)
        self.worker.finished.connect(self._on_finished)
        self.worker.error.connect(self._on_error)
        self.worker.start()

    def _on_finished(self, stats):
        self.btn_start.setEnabled(True)
        self.progress.setVisible(False)
        self.status_label.setText("完成")
        self.statusBar().showMessage(f"完成！共 {stats['total']} 笔")
        msg = f"✅ 处理完成！\n\n"
        msg += f"成功分类: {stats['total'] - stats['unclassified']} 笔\n"
        msg += f"未分类: {stats['unclassified']} 笔\n"
        msg += f"输出: {stats['output_file']}"
        if stats.get('unclassified_file'):
            msg += f"\n未分类: {stats['unclassified_file']}"
        QMessageBox.information(self, "完成", msg)

    def _on_error(self, error):
        self.btn_start.setEnabled(True)
        self.progress.setVisible(False)
        self.status_label.setText("错误")
        self.statusBar().showMessage(f"错误: {error}")
        QMessageBox.critical(self, "错误", error)
