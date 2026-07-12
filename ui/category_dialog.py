from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QSplitter, QGroupBox,
    QListWidget, QTextEdit, QPushButton, QMessageBox, QInputDialog, QLabel,
    QWidget, QListWidgetItem, QMenu, QApplication
)
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QAction

from core.category_manager import CategoryManager
from core.user_keywords_manager import UserKeywordsManager


class CategoryDialog(QDialog):
    def __init__(self, manager, parent=None):
        super().__init__(parent)
        self.manager = manager
        self.keywords_manager = UserKeywordsManager()
        self.current_main = None
        self.current_sub = None
        self.current_third = None
        self.setWindowTitle("分类规则管理")

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        width = int(screen_geometry.width() * 0.5)
        height = int(screen_geometry.height() * 0.55)
        self.resize(width, height)
        self.setMinimumSize(700, 450)

        self._init_ui()
        self._load_data()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)

        btn_layout = QHBoxLayout()
        self.btn_add_main = QPushButton("添加一级分类")
        self.btn_add_main.clicked.connect(self._add_main)
        self.btn_add_sub = QPushButton("添加二级分类")
        self.btn_add_sub.clicked.connect(self._add_sub)
        self.btn_add_third = QPushButton("添加三级分类")
        self.btn_add_third.clicked.connect(self._add_third)
        self.btn_delete = QPushButton("删除选中")
        self.btn_delete.clicked.connect(self._delete)

        btn_layout.addWidget(self.btn_add_main)
        btn_layout.addWidget(self.btn_add_sub)
        btn_layout.addWidget(self.btn_add_third)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        splitter = QSplitter(Qt.Horizontal)

        col1 = QWidget()
        col1_layout = QVBoxLayout(col1)
        col1_layout.setContentsMargins(0, 0, 0, 0)
        col1_layout.addWidget(QLabel("📊 一级分类（右键菜单）"))
        self.main_list = QListWidget()
        self.main_list.itemClicked.connect(self._on_main_selected)
        self.main_list.itemDoubleClicked.connect(self._rename_main)
        self.main_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.main_list.customContextMenuRequested.connect(self._show_main_menu)
        self.main_list.installEventFilter(self)
        col1_layout.addWidget(self.main_list)

        col2 = QWidget()
        col2_layout = QVBoxLayout(col2)
        col2_layout.setContentsMargins(0, 0, 0, 0)
        col2_layout.addWidget(QLabel("📂 二级分类（右键菜单）"))
        self.sub_list = QListWidget()
        self.sub_list.itemClicked.connect(self._on_sub_selected)
        self.sub_list.itemDoubleClicked.connect(self._rename_sub)
        self.sub_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.sub_list.customContextMenuRequested.connect(self._show_sub_menu)
        self.sub_list.installEventFilter(self)
        col2_layout.addWidget(self.sub_list)

        col3 = QWidget()
        col3_layout = QVBoxLayout(col3)
        col3_layout.setContentsMargins(0, 0, 0, 0)
        col3_layout.addWidget(QLabel("📁 三级分类（右键菜单）"))
        self.third_list = QListWidget()
        self.third_list.itemClicked.connect(self._on_third_selected)
        self.third_list.itemDoubleClicked.connect(self._rename_third)
        self.third_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.third_list.customContextMenuRequested.connect(self._show_third_menu)
        self.third_list.installEventFilter(self)
        col3_layout.addWidget(self.third_list)

        rule_group = QGroupBox("系统规则（只读）")
        rule_layout = QVBoxLayout(rule_group)
        self.rule_edit = QTextEdit()
        self.rule_edit.setMaximumHeight(120)
        self.rule_edit.setReadOnly(True)
        self.rule_edit.setStyleSheet("background-color: #f5f5f5;")
        rule_layout.addWidget(self.rule_edit)
        col3_layout.addWidget(rule_group)

        keyword_group = QGroupBox("用户追加的关键词（双击删除）")
        keyword_layout = QVBoxLayout(keyword_group)
        self.keyword_list = QListWidget()
        self.keyword_list.setMaximumHeight(80)
        self.keyword_list.itemDoubleClicked.connect(self._remove_keyword)
        keyword_layout.addWidget(self.keyword_list)

        keyword_btn_layout = QHBoxLayout()
        btn_append = QPushButton("➕ 追加关键词")
        btn_append.clicked.connect(self._append_keyword)
        btn_append.setStyleSheet("background-color: #17a2b8; color: white;")
        keyword_btn_layout.addWidget(btn_append)

        btn_remove = QPushButton("➖ 删除选中")
        btn_remove.clicked.connect(self._remove_keyword_btn)
        keyword_btn_layout.addWidget(btn_remove)

        keyword_btn_layout.addStretch()
        keyword_layout.addLayout(keyword_btn_layout)

        hint = QLabel("💡 追加关键词：多个用空格或逗号分隔 | 双击关键词可删除")
        hint.setStyleSheet("color: #666; font-size: 11px;")
        keyword_layout.addWidget(hint)

        col3_layout.addWidget(keyword_group)

        splitter.addWidget(col1)
        splitter.addWidget(col2)
        splitter.addWidget(col3)
        splitter.setSizes([120, 180, 400])
        layout.addWidget(splitter)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        self.btn_save = QPushButton("💾 保存配置")
        self.btn_save.clicked.connect(self._save)
        self.btn_save.setStyleSheet("background-color: #28a745; color: white; font-weight: bold; padding: 6px 16px;")
        bottom_layout.addWidget(self.btn_save)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)

        self.btn_add_sub.setEnabled(False)
        self.btn_add_third.setEnabled(False)
        self.btn_delete.setEnabled(False)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            key_event = event
            if key_event.key() == Qt.Key_Delete:
                if obj is self.main_list and self.main_list.currentItem():
                    self._delete()
                    return True
                elif obj is self.sub_list and self.sub_list.currentItem():
                    self._delete()
                    return True
                elif obj is self.third_list and self.third_list.currentItem():
                    self._delete()
                    return True
        return super().eventFilter(obj, event)

    def _show_main_menu(self, position):
        item = self.main_list.itemAt(position)
        if not item:
            return
        self.main_list.setCurrentItem(item)
        menu = QMenu()
        rename_action = QAction("重命名", self)
        rename_action.triggered.connect(lambda: self._rename_main(item))
        menu.addAction(rename_action)
        delete_action = QAction("删除", self)
        delete_action.triggered.connect(self._delete)
        menu.addAction(delete_action)
        menu.addSeparator()
        add_sub_action = QAction("添加二级分类", self)
        add_sub_action.triggered.connect(self._add_sub)
        menu.addAction(add_sub_action)
        menu.exec(self.main_list.mapToGlobal(position))

    def _show_sub_menu(self, position):
        item = self.sub_list.itemAt(position)
        if not item:
            return
        self.sub_list.setCurrentItem(item)
        menu = QMenu()
        rename_action = QAction("重命名", self)
        rename_action.triggered.connect(lambda: self._rename_sub(item))
        menu.addAction(rename_action)
        delete_action = QAction("删除", self)
        delete_action.triggered.connect(self._delete)
        menu.addAction(delete_action)
        menu.addSeparator()
        add_third_action = QAction("添加三级分类", self)
        add_third_action.triggered.connect(self._add_third)
        menu.addAction(add_third_action)
        menu.exec(self.sub_list.mapToGlobal(position))

    def _show_third_menu(self, position):
        item = self.third_list.itemAt(position)
        if not item:
            return
        self.third_list.setCurrentItem(item)
        menu = QMenu()
        rename_action = QAction("重命名", self)
        rename_action.triggered.connect(lambda: self._rename_third(item))
        menu.addAction(rename_action)
        delete_action = QAction("删除", self)
        delete_action.triggered.connect(self._delete)
        menu.addAction(delete_action)
        menu.exec(self.third_list.mapToGlobal(position))

    def _load_data(self):
        self.main_list.clear()
        for cat in self.manager.get_main_categories():
            self.main_list.addItem(cat)
        if self.main_list.count() > 0:
            self.main_list.setCurrentRow(0)
            self._on_main_selected(self.main_list.item(0))

    def _on_main_selected(self, item):
        self.current_main = item.text()
        self.current_sub = None
        self.current_third = None
        self.btn_add_sub.setEnabled(True)
        self.btn_add_third.setEnabled(False)
        self.btn_delete.setEnabled(True)
        self.sub_list.clear()
        self.third_list.clear()
        self.rule_edit.clear()
        self.keyword_list.clear()
        for sub in self.manager.get_sub_categories(self.current_main):
            self.sub_list.addItem(sub)
        if self.sub_list.count() > 0:
            self.sub_list.setCurrentRow(0)
            self._on_sub_selected(self.sub_list.item(0))

    def _on_sub_selected(self, item):
        self.current_sub = item.text()
        self.current_third = None
        self.btn_add_third.setEnabled(True)
        self.btn_delete.setEnabled(True)
        self.third_list.clear()
        self.rule_edit.clear()
        self.keyword_list.clear()
        for third in self.manager.get_third_categories(self.current_main, self.current_sub):
            self.third_list.addItem(third)
        if self.third_list.count() > 0:
            self.third_list.setCurrentRow(0)
            self._on_third_selected(self.third_list.item(0))

    def _on_third_selected(self, item):
        self.current_third = item.text()
        self.btn_delete.setEnabled(True)
        rules = self.manager.get_rules(self.current_main, self.current_sub, self.current_third)
        self.rule_edit.setText(rules)
        self._load_keywords()

    def _load_keywords(self):
        self.keyword_list.clear()
        keywords = self.keywords_manager.get_keywords(
            self.current_main, self.current_sub, self.current_third, None
        )
        for kw in keywords:
            item = QListWidgetItem(kw)
            item.setForeground(Qt.blue)
            self.keyword_list.addItem(item)
        if not keywords:
            self.keyword_list.addItem("（暂无追加的关键词）")

    def _append_keyword(self):
        if not self.current_main or not self.current_sub or not self.current_third:
            QMessageBox.warning(self, "提示", "请先选择三级分类")
            return
        text, ok = QInputDialog.getText(
            self,
            "追加关键词",
            "输入要追加的关键词（多个用空格或逗号分隔）："
        )
        if not ok or not text:
            return
        keywords = []
        for sep in ['，', ',', ' ']:
            if sep in text:
                keywords = [k.strip() for k in text.split(sep) if k.strip()]
                break
        if not keywords:
            keywords = [text.strip()]
        added = self.keywords_manager.add_keywords(
            self.current_main, self.current_sub, self.current_third, None, keywords
        )
        if added:
            self.keywords_manager.save()
            self._load_keywords()
            QMessageBox.information(self, "成功", f"已追加: {', '.join(added)}")
        else:
            QMessageBox.warning(self, "提示", "所有关键词已存在")

    def _remove_keyword(self, item):
        keyword = item.text()
        if keyword.startswith("（暂无"):
            return
        reply = QMessageBox.question(
            self, "确认删除", f"删除关键词「{keyword}」？",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.keywords_manager.remove_keyword(
                self.current_main, self.current_sub, self.current_third, None, keyword
            )
            self.keywords_manager.save()
            self._load_keywords()

    def _remove_keyword_btn(self):
        item = self.keyword_list.currentItem()
        if not item:
            QMessageBox.warning(self, "提示", "请先选中一个关键词")
            return
        self._remove_keyword(item)

    def _add_main(self):
        text, ok = QInputDialog.getText(self, "添加一级分类", "输入分类名（多个用空格分隔）：")
        if ok and text:
            added = [name for name in text.strip().split() if self.manager.add_main_category(name)]
            if added:
                self._load_data()
                QMessageBox.information(self, "成功", f"已添加 {len(added)} 个一级分类")

    def _add_sub(self):
        if not self.current_main:
            QMessageBox.warning(self, "提示", "请先选择一级分类")
            return
        text, ok = QInputDialog.getText(self, "添加二级分类", f"在「{self.current_main}」下添加：")
        if ok and text:
            added = [name for name in text.strip().split() if self.manager.add_sub_category(self.current_main, name)]
            if added:
                self._load_data()
                self._select_main(self.current_main)
                QMessageBox.information(self, "成功", f"已添加 {len(added)} 个二级分类")

    def _add_third(self):
        if not self.current_main or not self.current_sub:
            QMessageBox.warning(self, "提示", "请先选择一级和二级分类")
            return
        text, ok = QInputDialog.getText(self, "添加三级分类", f"在「{self.current_main} → {self.current_sub}」下添加：")
        if ok and text:
            added = []
            for name in text.strip().split():
                if self.manager.add_third_category(self.current_main, self.current_sub, name):
                    added.append(name)
            if added:
                self._load_data()
                self._select_main(self.current_main)
                QMessageBox.information(self, "成功", f"已添加 {len(added)} 个三级分类")

    def _delete(self):
        third_item = self.third_list.currentItem()
        sub_item = self.sub_list.currentItem()
        main_item = self.main_list.currentItem()

        if third_item:
            reply = QMessageBox.question(
                self, "确认删除",
                f"删除三级分类「{third_item.text()}」？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.manager.delete_third_category(self.current_main, self.current_sub, third_item.text())
                self._load_data()
                self._select_main(self.current_main)
        elif sub_item:
            reply = QMessageBox.question(
                self, "确认删除",
                f"删除二级分类「{sub_item.text()}」及其所有三级分类？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.manager.delete_sub_category(self.current_main, sub_item.text())
                self._load_data()
                self._select_main(self.current_main)
        elif main_item:
            reply = QMessageBox.question(
                self, "确认删除",
                f"删除一级分类「{main_item.text()}」及其所有子分类？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.manager.delete_main_category(main_item.text())
                self._load_data()

    def _rename_main(self, item):
        old = item.text()
        new, ok = QInputDialog.getText(self, "重命名一级分类", "新名称：", text=old)
        if ok and new and new != old:
            if self.manager.rename_main_category(old, new):
                self._load_data()
                self._select_main(new)

    def _rename_sub(self, item):
        if not self.current_main:
            return
        old = item.text()
        new, ok = QInputDialog.getText(self, "重命名二级分类", "新名称：", text=old)
        if ok and new and new != old:
            if self.manager.rename_sub_category(self.current_main, old, new):
                self._load_data()
                self._select_main(self.current_main)

    def _rename_third(self, item):
        if not self.current_main or not self.current_sub:
            return
        old = item.text()
        new, ok = QInputDialog.getText(self, "重命名三级分类", "新名称：", text=old)
        if ok and new and new != old:
            if self.manager.rename_third_category(self.current_main, self.current_sub, old, new):
                self._load_data()
                self._select_main(self.current_main)

    def _save(self):
        if self.manager.save():
            QMessageBox.information(self, "成功", "配置已保存")
        else:
            QMessageBox.critical(self, "错误", "保存失败")

    def _select_main(self, name):
        for i in range(self.main_list.count()):
            if self.main_list.item(i).text() == name:
                self.main_list.setCurrentRow(i)
                self._on_main_selected(self.main_list.item(i))
                break
