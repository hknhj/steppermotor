import sys
import serial
from PyQt5.QtWidgets import *
from PyQt5 import uic

main_ui = uic.loadUiType("scanner main.ui")[0]
scan = uic.loadUiType("scan.ui")[0]
manual = uic.loadUiType("manual.ui")[0]

class ScanWindow(QMainWindow, scan):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class ManualWindow(QMainWindow, manual):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class WindowClass(QMainWindow, main_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ser = serial.Serial('COM3', 9600)
        
        self.scanEnterButton.clicked.connect(self.scanEnter)
        self.manualEnterButton.clicked.connect(self.manualEnter)
        self.initLocButton.clicked.connect(self.initLoc)
        
    def scanEnter(self):
        self.scan_window = ScanWindow()
        self.scan_window.show()
        
    def manualEnter(self):
        self.manual_window = ManualWindow()
        self.manual_window.show()
        
    def initLoc(self):
        value = 10
        self.ser.write(value.encode('utf-8'))
        print(f"Sent : {value}")
        
        
if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
