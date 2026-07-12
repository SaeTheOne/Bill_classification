import os
from PySide6.QtWidgets import QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QKeyEvent


class FileDropListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DropOnly)
        self.setDefaultDropAction(Qt.CopyAction)
        self.setStyleSheet("""
            QListWidget {
                border: 2px dashed #a0a0a0;
                border-radius: 5px;
                background-color: #f9f9f9;
                font-size: 13px;
                padding: 5px;
                min-height: 80px;
            }
            QListWidget:hover {
                border-color: #0078d7;
                background-color: #eef6fc;
            }
            QListWidget::item {
                padding: 3px;
                border-bottom: 1px solid #eee;
                background-color: transparent;
                color: #333;
            }
            QListWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
            QListWidget::item:selected:hover {
                background-color: #0078d7;
                color: white;
            }
            QListWidget::item:selected:!active {
                background-color: #d0d0d0;
                color: #333;
            }
            QListWidget::item:hover:!selected {
                background-color: #e8f0fe;
            }
        """)

    def keyPressEvent(self, event):
        """监听键盘事件，支持 Delete 键删除"""
        if event.key() == Qt.Key_Delete:
            current_row = self.currentRow()
            if current_row >= 0:
                self.takeItem(current_row)
                return
        super().keyPressEvent(event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            paths = []
            for url in event.mimeData().urls():
                path = url.toLocalFile()
                if os.path.exists(path):
                    paths.append(path)
            if paths:
                self.add_files(paths)
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()

    def add_files(self, paths):
        existing = [self.item(i).text() for i in range(self.count())]
        for path in paths:
            if path not in existing:
                text = f"[文件夹] {path}" if os.path.isdir(path) else path
                self.addItem(QListWidgetItem(text))