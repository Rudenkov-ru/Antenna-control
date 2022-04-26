# Antenna control v.1.0
# INCLUDES #
import os
from PyQt5.QtWidgets import QFileDialog, QLCDNumber
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import QIODevice, QFileInfo, QTime, QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
import datetime
import pytz

# HOOK LOGIC #
app = QtWidgets.QApplication([])
DateTime = datetime.datetime.now()
RST = pytz.timezone('Europe/Moscow')
ui = uic.loadUi("interface.ui")
ui.setWindowIcon(QtGui.QIcon('icon.png'))
ui.setWindowTitle("Antenna control")

print("log: UI window LOADED!")
ui.log_textBrowser.append('Дата : %02.d-%02.d-%d' % (DateTime.day, DateTime.month, DateTime.year))
ui.log_textBrowser.append(
    '%02.d:%02.d:%02.d - Программа запущена!' % (DateTime.hour, DateTime.minute, DateTime.second))

timer = QTimer()
timer.start(1000)
Error = QtWidgets.QErrorMessage()
# -- FIND/OUTPUT PORTS
serial = QSerialPort()
serial.setBaudRate(115200)

portList = []
ports = QSerialPortInfo.availablePorts()
for port in ports:
    portList.append(port.portName())
print(portList)

ui.tmb_comboBox.addItems(portList)  # Load COM for TMB
ui.sap_comboBox.addItems(portList)  # Load COM for SAP
ui.kk_comboBox.addItems(portList)  # Load COM for KK

print("log: portList LOADED!")


# -- BUTTONS
def loadB():  # Open directory for load data
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
    ui.ugolmtmb_lineEdit.setText(AngleTMB)
    ui.aztmb_lineEdit.setText(AzimuthalTMB)

    # -TOOLS for KK
    ui.ugolmsap_lineEdit.setText(AngleKK)
    ui.azsap_lineEdit.setText(AzimuthalKK)

    # -TOOLS for SAP
    ui.ugolmkk_lineEdit.setText(AngleSAP)
    ui.azkk_lineEdit.setText(AzimuthalSAP)

    # -TOOLS for listBox
    ui.list_comboBox.addItems(contentList)
    print("DEBUG: close folder...")
    with open(filename, 'r') as f:  # READ FILE
        allContent = f.read()  # PARAMS for log_textBrowser
        ui.log_textBrowser.append(
            '%02.d:%02.d:%02.d - Целеуказания загружены! [%s]' % (
                DateTime.hour, DateTime.minute, DateTime.second, allContent))


def startB():  # Start button

    serial.setPortName(ui.tmb_comboBox.currentText())
    serial.setPortName(ui.kk_comboBox.currentText())
    serial.setPortName(ui.sap_comboBox.currentText())
    serial.open(QIODevice.ReadWrite)
    ui.log_textBrowser.append(
        '%02.d:%02.d:%02.d - Производится наведение на объект...' % (
            DateTime.hour, DateTime.minute, DateTime.second))
    ui.log_textBrowser.append(
        '%02.d:%02.d:%02.d - Наведение успешно завершено!' % (DateTime.hour, DateTime.minute, DateTime.second))
    print("log: serial OPEN!")


def closeB():
    serial.close()
    ui.log_textBrowser.append(
        '%02.d:%02.d:%02.d - Сеанс успешно окончен!' % (DateTime.hour, DateTime.minute, DateTime.second))
    print("log: serial CLOSE!")







def TimeUpdater():
    ui.Time_Edit.append('%02.d:%02.d:%02.d' % (DateTime.hour, DateTime.minute, DateTime.second))
    ui.Date_Edit.append('%02.d-%02.d-%d' % (DateTime.day, DateTime.month, DateTime.year))


TimeUpdater()

ui.closeButton.clicked.connect(closeB)  # Close button
ui.startButton.clicked.connect(startB)  # Start button
ui.loadButton.clicked.connect(loadB)  # Load button

# SHOW PROGRAM #
ui.show()
app.exec()
