#!/usr/bin/env python3
#---------------------------------
# Project name: QoS NB-IoT
#---------------------------------
# 
#
#
# Date: 17-06-2019 
# Programmer: AK MT


from PyQt5 import QtCore, QtGui, QtWidgets
import serial
import time, datetime   
import sys
import threading
import json
from multiprocessing import Process, Pipe, Array, Value
#import QOS_NB-IoT_rc 
import QOS_NB_IoT_rc

status_machine = Array('i', range(4))    # Status machine : [ {1 : started or running},  {2 : stopped}, {0 : not in any mode} ]

class Ui_mainWindQoSNBIoT(object):
    def setupUi(self, mainWindQoSNBIoT):
        mainWindQoSNBIoT.setObjectName("mainWindQoSNBIoT")
        mainWindQoSNBIoT.resize(800, 460)
        mainWindQoSNBIoT.setStyleSheet("background-color: rgb(46, 52, 54);")
        self.centralwidget = QtWidgets.QWidget(mainWindQoSNBIoT)
        self.centralwidget.setObjectName("centralwidget")
        self.lbl_title = QtWidgets.QLabel(self.centralwidget)
        self.lbl_title.setGeometry(QtCore.QRect(310, 70, 231, 41))
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        font.setPointSize(28)
        #font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.lbl_title.setFont(font)
        self.lbl_title.setStyleSheet("color: rgb(255, 255, 255);")
        self.lbl_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_title.setObjectName("lbl_title")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 330, 801, 71))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(50, 0, 50, 0)
        self.horizontalLayout.setSpacing(50)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_Stop = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_Stop.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("Carlito")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.btn_Stop.setFont(font)
        self.btn_Stop.setStyleSheet("color: rgb(255, 255, 255);\n"
"border: 1px solid, rgb(255,255,255);")
        self.btn_Stop.setObjectName("btn_Stop")
        self.horizontalLayout.addWidget(self.btn_Stop)
        self.btn_Start = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_Start.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("Carlito")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.btn_Start.setFont(font)
        self.btn_Start.setStyleSheet("color: rgb(255, 255, 255);\n"
"border: 1px solid, rgb(255,255,255);")
        self.btn_Start.setObjectName("btn_Start")
        self.horizontalLayout.addWidget(self.btn_Start)
        self.lbl_tilte_qos = QtWidgets.QLabel(self.centralwidget)
        self.lbl_tilte_qos.setGeometry(QtCore.QRect(180, 190, 221, 39))
        font = QtGui.QFont()
        font.setFamily("Carlito")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_tilte_qos.setFont(font)
        self.lbl_tilte_qos.setStyleSheet("color: rgb(136, 138, 133);")
        self.lbl_tilte_qos.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_tilte_qos.setObjectName("lbl_tilte_qos")
        self.lbl_titleDRINKO = QtWidgets.QLabel(self.centralwidget)
        self.lbl_titleDRINKO.setGeometry(QtCore.QRect(5, 0, 291, 71))
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        font.setPointSize(34)
        #font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.lbl_titleDRINKO.setFont(font)
        self.lbl_titleDRINKO.setStyleSheet("color: rgb(255, 255, 255);")
        self.lbl_titleDRINKO.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_titleDRINKO.setObjectName("lbl_titleDRINKO")
        self.lbl_status = QtWidgets.QLabel(self.centralwidget)
        self.lbl_status.setGeometry(QtCore.QRect(310, 240, 78, 39))
        font = QtGui.QFont()
        font.setFamily("Carlito")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_status.setFont(font)
        self.lbl_status.setStyleSheet("color: rgb(136, 138, 133);")
        self.lbl_status.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_status.setObjectName("lbl_status")
        self.lbl_csq = QtWidgets.QLabel(self.centralwidget)
        self.lbl_csq.setGeometry(QtCore.QRect(190, 240, 80, 39))
        font = QtGui.QFont()
        font.setFamily("Carlito")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_csq.setFont(font)
        self.lbl_csq.setStyleSheet("color: rgb(136, 138, 133);")
        self.lbl_csq.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_csq.setObjectName("lbl_csq")
        self.lbl_atcsq = QtWidgets.QLabel(self.centralwidget)
        self.lbl_atcsq.setGeometry(QtCore.QRect(190, 280, 71, 39))
        font = QtGui.QFont()
        font.setFamily("Carlito")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_atcsq.setFont(font)
        self.lbl_atcsq.setStyleSheet("color: rgb(255, 255, 255);")
        self.lbl_atcsq.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_atcsq.setObjectName("lbl_atcsq")
        self.lbl_statusfield = QtWidgets.QLabel(self.centralwidget)
        self.lbl_statusfield.setGeometry(QtCore.QRect(310, 280, 80, 39))
        font = QtGui.QFont()
        font.setFamily("Carlito")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_statusfield.setFont(font)
        self.lbl_statusfield.setStyleSheet("color: rgb(255, 255, 255);")
        self.lbl_statusfield.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_statusfield.setObjectName("lbl_statusfield")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(470, 180, 81, 141))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.progressBar.setFont(font)
        self.progressBar.setStyleSheet("QProgressBar {\n"
"border: 1px solid black;\n"
"text-align: top;\n"
"padding: 1px;\n"
"border-bottom-right-radius: 7px;\n"
"border-bottom-left-radius: 7px;\n"
"background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0,\n"
"stop: 0 #fff,\n"
"stop: 0.4999 #eee,\n"
"stop: 0.5 #ddd,\n"
"stop: 1 #eee );\n"
"width: 15px;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0,\n"
"stop: 0 #78d,\n"
"stop: 0.4999 #46a,\n"
"stop: 0.5 #45a,\n"
"stop: 1 #238 );\n"
"border-bottom-right-radius: 7px;\n"
"border-bottom-left-radius: 7px;\n"
"border: 1px solid black;\n"
"}")
        self.progressBar.setMaximum(30)
        self.progressBar.setProperty("value", -1)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Vertical)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.lbl_iconStatus = QtWidgets.QLabel(self.centralwidget)
        self.lbl_iconStatus.setGeometry(QtCore.QRect(9, 424, 21, 21))
        self.lbl_iconStatus.setStyleSheet("border-image: url(:/qos/iconfinder_circle_green_10280.png);\n"
"border-image: url(:/qos/iconfinder_circle_red_10282.png);")
        self.lbl_iconStatus.setText("")
        self.lbl_iconStatus.setObjectName("lbl_iconStatus")
        self.lbl_connecxionStatus = QtWidgets.QLabel(self.centralwidget)
        self.lbl_connecxionStatus.setGeometry(QtCore.QRect(39, 419, 411, 31))
        self.lbl_connecxionStatus.setStyleSheet("color: rgb(255, 255, 255);")
        self.lbl_connecxionStatus.setObjectName("lbl_connecxionStatus")
        mainWindQoSNBIoT.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainWindQoSNBIoT)
        QtCore.QMetaObject.connectSlotsByName(mainWindQoSNBIoT)

    def retranslateUi(self, mainWindQoSNBIoT):
        _translate = QtCore.QCoreApplication.translate
        mainWindQoSNBIoT.setWindowTitle(_translate("mainWindQoSNBIoT", "DRINKOTEC"))
        mainWindQoSNBIoT.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.lbl_title.setText(_translate("mainWindQoSNBIoT", "QoS NB-IoT"))
        self.btn_Stop.setText(_translate("mainWindQoSNBIoT", "Stop"))
        self.btn_Start.setText(_translate("mainWindQoSNBIoT", "Start"))
        self.lbl_tilte_qos.setText(_translate("mainWindQoSNBIoT", "Quality Of Signal"))
        self.lbl_titleDRINKO.setText(_translate("mainWindQoSNBIoT", "DRINKOTEC"))
        self.lbl_status.setText(_translate("mainWindQoSNBIoT", "Status"))
        self.lbl_csq.setText(_translate("mainWindQoSNBIoT", " CSQ  "))
        self.lbl_atcsq.setText(_translate("mainWindQoSNBIoT", "00"))
        self.lbl_statusfield.setText(_translate("mainWindQoSNBIoT", "None"))
        self.progressBar.setFormat(_translate("mainWindQoSNBIoT", "%p%"))
        self.lbl_connecxionStatus.setText(_translate("mainWindQoSNBIoT", "Not Connected"))
        
        self.btn_Start.clicked.connect(self.startQoS)
        self.btn_Stop.clicked.connect(self.stopQoS)

    # Start QoS
    def startQoS(self): 
        # 
        print("Start QoS")
        if(status_machine[0] !=1):
            self.check_SIM_gprs()
        
    # Stop QoS
    def stopQoS(self): 
        # 
        print("Stop QoS {}".format(status_machine[0]))
        if(status_machine[0] ==1):
            status_machine[0] = 0
            self.lbl_statusfield.setText("None")
            self.lbl_atcsq.setText("00")
            self.progressBar.setProperty("value", 0)
            self.lbl_connecxionStatus.setText( "Not Connected: Stopped.")
            self.lbl_iconStatus.setStyleSheet("border-image: url(:/qos/iconfinder_circle_red_10282.png);")
            


    # Get the Signal Strength
    def get_Signal_Strength(self):
       W_buff = [b'at+csq\r']
       self.ser.write(W_buff[0]) 
       self.ser.flushInput()
       #time.sleep(1)
       strMessg = self._read_data()
       return strMessg


    # Read data from the SIM Card (AT Commands)
    def _read_data(self):
	    flag_CR=False
	    flag_LF=False
	    flag_Messg=0
	    data = ""
	    buffer = bytearray()
	    while True:
		    # read byte by byte, one byte each time 
		    byte = self.ser.read(1) 
		    #print(byte)
		    if(byte==b''):
			    print("Empty byte")
			    self.ser.flushOutput()
			    self.ser.flushInput()
			    break
			    #continue
		    buffer.append(byte[0])
		    if (byte == bytes([0x0D])):
			    flag_CR=True
		    if (flag_CR==True and byte == bytes([0x0A])):
			    #print("EOF ...")
			    flag_Messg = flag_Messg + 1
		    if (flag_Messg == 4) :
			    flag_Messg = 0
			    flag_CR=False
			    flag_LF=False
			    break
	    #print(byte)
	    strRtnMessg = buffer.decode("utf-8")
	    #print(buffer.decode("utf-8"))
	
	    # Message in Hex Format
	    #print("Message : "+ ' '.join(hex(c) for c in buffer) )
	
	    return strRtnMessg

    # Check the Card SIM Connection 
    # Should be launched in a seperate thread. For now this should do the trick.
    def check_SIM_gprs(self):

       status_machine[0] = 1
       try:
          self.ser = serial.Serial("/dev/ttyAMA0")
          self.ser.baudrate = 9600
          self.ser.bytesize = serial.EIGHTBITS
          self.ser.parity = serial.PARITY_NONE
          self.ser.stopbits = serial.STOPBITS_ONE
          self.ser.timeout =  2
          self.ser.flushOutput()
          #print(self.ser)
          self.lbl_connecxionStatus.setText( "Connected.")
          self.lbl_iconStatus.setStyleSheet("border-image: url(:/qos/iconfinder_circle_green_10280.png);")
   
       except Exception as e:
          print("Error : No Serial RS232.")
          self.lbl_connecxionStatus.setText( "Not Connected: Error.")
          self.lbl_iconStatus.setStyleSheet("border-image: url(:/qos/iconfinder_circle_red_10282.png);")
          status_machine[0] = 0
          return 0
          #sys.exit(0)
  
  
       try: 
          while(status_machine[0] ==1):
              strRtnMess = self.get_Signal_Strength()
                  #QtCore.QCoreApplication.processEvents()
              lst_rtn_mssg =  ((strRtnMess.split('\r\n'))[1]).split()[1].split(',')[0]
              strDate = '{0:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())
              QtCore.QCoreApplication.processEvents()
              intStrengthSignal = int(lst_rtn_mssg)
              if(intStrengthSignal <= 9):
                 #print("{} CSQ:{} Marginal".format(strDate, intStrengthSignal))
                 self.lbl_atcsq.setText(lst_rtn_mssg)
                 self.lbl_statusfield.setText("Marginal")
                 self.progressBar.setProperty("value", intStrengthSignal)
              elif(intStrengthSignal >=10 and intStrengthSignal <=14):
                 #print("{} CSQ:{} OK".format(strDate, intStrengthSignal))
                 self.lbl_atcsq.setText(lst_rtn_mssg)
                 self.lbl_statusfield.setText("OK")
                 self.progressBar.setProperty("value", intStrengthSignal)
              elif(intStrengthSignal >=15 and intStrengthSignal <= 19):
                 #print("{} CSQ:{} Good".format(strDate, intStrengthSignal))
                 self.lbl_atcsq.setText(lst_rtn_mssg)
                 self.lbl_statusfield.setText("Good")
                 self.progressBar.setProperty("value", intStrengthSignal)
              elif(intStrengthSignal >= 20 and intStrengthSignal <= 30):
                 #print("{} CSQ:{} Excellent".format(strDate, intStrengthSignal))
                 self.lbl_atcsq.setText(lst_rtn_mssg)
                 self.lbl_statusfield.setText("Excellent")
                 self.progressBar.setProperty("value", intStrengthSignal)
             
             
              #print(lst_rtn_mssg)
              QtCore.QCoreApplication.processEvents()
              time.sleep(0.1)
              #QtCore.QCoreApplication.processEvents()

       except Exception as e:
          print("Error : Not Connected: Error Check the connection or power.")
          self.lbl_connecxionStatus.setText( "Not Connected: Error.")
          self.lbl_iconStatus.setStyleSheet("border-image: url(:/qos/iconfinder_circle_red_10282.png);")
          self.lbl_statusfield.setText("None")
          self.lbl_atcsq.setText("00")
          self.progressBar.setProperty("value", 0)
          status_machine[0] = 0
          #return 0

       QtCore.QCoreApplication.processEvents()
       self.ser.close()








if __name__ == "__main__":
    import sys
    
    status_machine[0] = 0;   
    
    app = QtWidgets.QApplication(sys.argv)
    mainWindQoSNBIoT = QtWidgets.QMainWindow()
    ui = Ui_mainWindQoSNBIoT()
    ui.setupUi(mainWindQoSNBIoT)
    mainWindQoSNBIoT.show()
    sys.exit(app.exec_())

