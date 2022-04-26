#  Antenna control v.1.0
#  INCLUDES  #
import os
import sys
from datetime import datetime
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QIODevice, QFileInfo, QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLCDNumber, QPushButton


#  CLASSES  #
class UI(QMainWindow):  # Main class
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("interface.ui", self)  # Load interface
        print("log: UI window LOADED!")
        self.setWindowIcon(QtGui.QIcon("icon.png"))  # Upload icon
        self.setWindowTitle("Antenna control")  # ReName App

        #  Work with the REAL time
        time = datetime.now()
        formatted_time = time.strftime("%H:%M:%S")
        self.DateTime = datetime.now()
        print("log: UI window LOADED!")
        self.log_textBrowser.append(
            'Дата : %02.d-%02.d-%d' % (self.DateTime.day, self.DateTime.month, self.DateTime.year))
        self.log_textBrowser.append(
            formatted_time + ' - Программа запущена!')

        #  Work with the BUTTONS
        self.lcd = self.findChild(QLCDNumber, "lcd_TimeEdit")
        self.UploadBtn = self.findChild(QPushButton, "loadButton")
        self.StartBtn = self.findChild(QPushButton, "startButton")
        self.StopBtn = self.findChild(QPushButton, "closeButton")
        self.RbAuto = self.findChild(QPushButton, "autoRadioButton")
        self.RbHand = self.findChild(QPushButton, "handRadioButton")

        #  Work with timer in LCD
        self.timer = QTimer()
        self.timer.timeout.connect(self.lcd_number)
        self.timer.start(1000)

        # QSerialTools
        self.serial = QSerialPort()
        self.serial.setBaudRate(115200)
        portList = []
        ports = QSerialPortInfo.availablePorts()
        for port in ports:
            portList.append(port.portName())
        print(portList)

        self.tmb_comboBox.addItems(portList)  # Load COM for TMB
        self.sap_comboBox.addItems(portList)  # Load COM for SAP
        self.kk_comboBox.addItems(portList)  # Load COM for KK

        print("log: portList LOADED!")

        # Call function
        self.lcd_number()  # Time
        print("log: LCD Number(Real Time) UPLOADED!")

        self.date()  # Date
        print("log: Date UPLOADED!")
        self.clicker()
        #  self.RadioCheck()
        #  Show app
        self.show()

    def lcd_number(self):  # System time at LCD
        time = datetime.now()
        formatted_time = time.strftime("%H:%M:%S")

        self.lcd.setDigitCount(8)
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        self.lcd.display(formatted_time)

    def date(self):
        self.Date_Edit.append('%02.d-%02.d-%d' % (datetime.now().day, datetime.now().month, datetime.now().year))

    def clicker(self):
        self.UploadBtn.clicked.connect(self.UploadB)
        self.StartBtn.clicked.connect(self.StartB)
        self.StopBtn.clicked.connect(self.StopB)

    #  Tools for following object
    def RadioCheck(self):
        self.RbAuto.clicked.connect(self.AutoFollow)
        self.RbHand.clicked.connect(self.HandFollow)

    def AutoFollow(self):
        self.log_textBrowser.append('Выбрано Автоматическое сопровождение КА !')
        print("Auto follow is chosen !")

    def HandFollow(self):
        self.log_textBrowser.append('Выбрано Программное сопровождение КА !')
        print("Hand follow is chosen !")

    #  Tools for Button
    def StartB(self):  # Start button
        time = datetime.now()
        formatted_time = time.strftime("%H:%M:%S")
        self.serial.setPortName(self.tmb_comboBox.currentText())
        self.serial.setPortName(self.kk_comboBox.currentText())
        self.serial.setPortName(self.sap_comboBox.currentText())
        self.serial.open(QIODevice.ReadWrite)
        self.log_textBrowser.append(
            formatted_time + ' - Производится наведение на объект...')
        self.log_textBrowser.append(
            formatted_time + ' - Наведение успешно завершено!')
        print("log: serial OPEN!")

    def StopB(self):
        time = datetime.now()
        formatted_time = time.strftime("%H:%M:%S")
        self.serial.close()
        self.log_textBrowser.append(
            formatted_time + ' - Сеанс успешно окончен!')
        print("log: serial CLOSE!")

    def UploadB(self):
        filepath, _ = QFileDialog.getOpenFileName(None, 'Выберите исходные данные', os.getcwd(),
                                                  'Text files (*.txt)')  # Load data(*.txt)
        print(filepath)
        filename = QFileInfo(filepath).fileName()  # GET fileName without URL
        with open(filename, 'r') as f:  # READ FILE
            contentL = f.read(24)  # PARAMS for listBox
            # -PARAMS for TMB
            AzimuthalTMB = f.read(8)
            AngleTMB = f.read(8)

            # -PARAMS for KK
            AzimuthalKK = f.read(8)
            AngleKK = f.read(8)

            # -PARAMS for SAP
            AzimuthalSAP = f.read(8)
            AngleSAP = f.read(5)

            contentList = [contentL]
        # -TOOLS for TMB
        self.ugolmtmb_lineEdit.setText(AngleTMB)
        self.aztmb_lineEdit.setText(AzimuthalTMB)

        # -TOOLS for KK
        self.ugolmsap_lineEdit.setText(AngleKK)
        self.azsap_lineEdit.setText(AzimuthalKK)

        # -TOOLS for SAP
        self.ugolmkk_lineEdit.setText(AngleSAP)
        self.azkk_lineEdit.setText(AzimuthalSAP)

        # -TOOLS for listBox
        self.list_comboBox.addItems(contentList)

        print("DEBUG: close folder...")


app = QApplication(sys.argv)
UIWindow = UI()
app.exec()
