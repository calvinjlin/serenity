import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget, QPushButton

class App(QWidget):
    def __init__(self):
        
        super().__init__()
        self.title = 'Ser'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        # mainMenu = self.menuBar()
        # fileMenu = mainMenu.addMenu('File')
        # editMenu = mainMenu.addMenu('Edit')
        # viewMenu = mainMenu.addMenu('View')

        layout = QGridLayout()
        
        # button = QPushButton('Confirm', self)
        # button.clicked.connect(self.on_click)
        # button2 = QPushButton('Confifrm', self)
        # button2.clicked.connect(self.on_click1)
        # button2.move(100,70)
        layout.addWidget(QPushButton('button1'),0,0)
        layout.addWidget(QPushButton('button2'),0,1)
        self.setLayout(layout)
        self.show()
        

    @pyqtSlot()
    def on_click(self):
        print('Click')

    @pyqtSlot()
    def on_click1(self):
        print('Clicwk')

def main():

    app = QApplication(sys.argv)
    ex = App()

    sys.exit(app.exec())

if __name__=='__main__':
    main()