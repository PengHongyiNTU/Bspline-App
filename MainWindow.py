from re import S
from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QContextMenuEvent
from PyQt6.QtCore import QSize


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("B-Spline")

        self.label = QLabel()
        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)

        layout = QVBoxLayout()
        
        layout.addWidget(self.label)
        layout.addWidget(self.input)

        Container = QWidget()
        Container.setLayout(layout)
        self.setCentralWidget(Container)
        self.setFixedSize(QSize(400, 300))

    def button_clicked(self):
        self.button.setText('Already Clicked')
        self.button.setEnabled(False)
        print("Button was clicked")

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        context = QMenu(self)
        context.addAction(QAction("Copy", self))
        context.addAction(QAction("Paste", self))
        context.exec(event.globalPos())
    

    