from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QWidget, QPushButton
from PyQt6.QtCore import QSize, QDateTime
from PyQt6 import QtGui
from PyQt6 import QtWidgets
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import numpy as np
import re
import os
import Bspline
import sympy

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self._x = []
        self._y = []

        sympy.init_printing(use_unicode=True)


        self.setWindowTitle("B-Spline")
        self.setFixedSize(QSize(800, 600))
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setStyleSheet(
            """
            QMenuBar {
                 background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 lightgray, stop:1 darkgray);  
            }
            QTextEdit {
                background-color: black;
            }
            """
        )

        # Status bar
        self.status = self.statusBar()
        self.status.showMessage("Ready")

        # Menu Bar
        menu = self.menuBar()
        menu.setNativeMenuBar(False)
       
        import_menu = menu.addMenu("Import")
        import_icon = getattr(QtWidgets.QStyle.StandardPixmap, 'SP_DialogOpenButton')
        import_menu.setIcon(self.style().standardIcon(import_icon))
        
        help_menu = menu.addMenu("Help")
        help_icon = getattr(QtWidgets.QStyle.StandardPixmap, 'SP_MessageBoxInformation')
        help_menu.setIcon(self.style().standardIcon(help_icon))
        display_help_act = QtGui.QAction("Display Help", self)
        display_help_act.triggered.connect(self.display_help)
        help_menu.addAction(display_help_act)
        select_file_act = QtGui.QAction("Select from local files", self)
        select_file_act.setStatusTip('Import Local Text File')
        select_file_act.triggered.connect(self.getfile)
        import_menu.addAction(select_file_act)


        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)

        
        self.example_label = QLabel()
        self.example_label.setText("Example: (0, 1), (1, 2), (2, 3), (3, 4)")
        self.enter_button = QPushButton("Enter")
        self.enter_button.clicked.connect(self._points_entered)


        self.console = QtWidgets.QTextEdit()
        self.console.setReadOnly(True)
        self.console.setTextColor(QtGui.QColor(0, 255, 0))
        self.console.setTextBackgroundColor(QtGui.QColor(0, 0, 0))
        self.console.append("$ Program Started")
        self.console.append("$ You may click the menu bar to import text files")
        self.console.append("$ You can also enter the points manually")
        self.console.append("$ Example: (x0, y0) (x1, y1) (x2, y2)")


        
        self.input = QLineEdit()
        self.input_label = QLabel()
        self.file_label = QLabel()
        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self._plot)
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self._reset)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self._save)
        
        
        self.plot_button.setToolTip('Click to plot')
        self.reset_button.setToolTip('Click to reset')
        self.save_button.setToolTip('Click to save')
        self.save_button.setEnabled(False)
        

        self.input.textChanged.connect(self.input_label.setText)

        # Canvas
        static_canvas = FigureCanvas(Figure(figsize=(5, 4)))
        toolbar = NavigationToolbar(static_canvas, self)
        self._ax = static_canvas.figure.subplots()
        self.canvas = static_canvas


        grid.addWidget(toolbar, 0, 0, 1, 6)
        grid.addWidget(static_canvas, 1, 0, 7, 6)

        grid.addWidget(self.console, 0, 6, 6, 3)
        grid.addWidget(self.input, 6, 6, 1, 2)
        grid.addWidget(self.enter_button, 6, 8, 1, 1)
        grid.addWidget(self.plot_button, 7, 6, 1, 1)
        grid.addWidget(self.save_button, 7, 7, 1, 1)
        grid.addWidget(self.reset_button, 7, 8, 1, 1)
   

        Container = QWidget()
        Container.setLayout(grid)
        self.setCentralWidget(Container)





    def getfile(self):
        home_dir = os.getcwd()
        dlg = QtWidgets.QFileDialog()
        dlg.setNameFilter("Text Files (*.txt)")
        fnames = dlg.getOpenFileName(self, 'Open file', home_dir)
        if fnames[0]:
            self.console.append("$ File Selected: " + fnames[0])
        with open(fnames[0], 'r') as f:
            self.console.append("$ File Opened: " + fnames[0])
            for line in f:
                x = float(line.split(' ')[0])
                y = float(line.split(' ')[1])
                self._x.append(x)
                self._y.append(y)
                self.console.append(f'>> Point Added  x: {x}, y: {y}')

    def display_help(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.setWindowTitle('Help')
        msg.setText('This software is used to plot B-Spline curves')
        msg.setInformativeText('To use this software: \n\n1. Enter the points in the text box  or Click the menu bar to import text files \n2. Click the Plot button \n3. Click the Reset button to clear the plot')
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg.exec()


    def _points_entered(self):
        input_string = self.input.text()
        matched = re.findall(r'\(([^)]+)\)', input_string)
        if matched:
            for match in matched:
                x, y = match.split(',')
                self.console.append(f'>> Point Added  x: {x}, y: {y}')
                x = float(x.strip())
                y = float(y.strip())
                self._x.append(x)
                self._y.append(y)
            
        else:
            self.console.append(">> Invalid input")
        self.enter_button.setEnabled(False)
        


    def _reset(self):
        self._x = []
        self._y = []
        self._ax.clear()
        self.console.clear()
        self.canvas.draw()
        self.enter_button.setEnabled(True)
        self.plot_button.setEnabled(True)
        self.save_button.setEnabled(False)
        self.console.append("$ Program Started")

    def _plot(self):
        if self._x and self._y:
            x = np.array(self._x)
            y = np.array(self._y)
            k = 3
            t = Bspline.chord_length_parameterization(x, y)
            T = Bspline.insert_dummy(t, k)
            self.T = T
            N = Bspline.get_N(k, t, T)
            self.N = N
            self.console.append(">> N: \n" + sympy.Matrix(N).__repr__())
            D = Bspline.get_D(x, y)
            self.D = D
            self.console.append(">> D: \n" + sympy.Matrix(D).__repr__())
            P = Bspline.get_P(N, D)
            self.P = P
            self.console.append(">> P: \n" + sympy.Matrix(P).__repr__())
            self.console.append(">> Plotting...")
            curve = Bspline.get_curve(P, k, T)
            self.curve = curve
            self._ax.clear()
            self._ax.plot(P[:, 0], P[:, 1], '--k', label='Control Polygon', marker='s', markersize=5)
            self._ax.scatter(x=x, y=y, c='r', s=80, label='Data Points')
            self._ax.plot(curve[:, 0], curve[:, 1], 'b', linewidth=2, label='B-spline curve')
            self._ax.legend()
            self._ax.set_title('Cubic B-Spline Curve')
            self.canvas.draw()
            self.plot_button.setEnabled(False)
            self.save_button.setEnabled(True)


        else:
            self.console.append(">> No points entered")


    def _save(self):
        time =  QDateTime.currentDateTime().toString("yyyy-MM-dd_hh-mm-ss")
        save_path = os.path.join(os.getcwd(), 'cubic_' + time + '.txt')
        self.console.append(">> Saving to: " + save_path)
        with open(save_path, 'w') as f:
            f.write('3\n')
            f.write(f'{len(self.P)}\n')
            T_list = [str(T) for T in list(self.T)]
            line = ' '.join(T_list)
            f.write(f'{line}\n')
            for i in range(len(self.P)):
                f.write(f'{self.P[i, 0]} {self.P[i, 1]}\n')
        self.console.append(">> Saved")

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        reply = QtWidgets.QMessageBox.question(self, 'Message', "Are you sure to quit?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No)
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()


    

    