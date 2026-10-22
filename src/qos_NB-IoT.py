

import serial
import time, datetime   
import sys
import threading
import json



# Get the Signal Strength
def get_Signal_Strength(ser):
   W_buff = [b'at+csq\r']
   ser.write(W_buff[0]) 
   ser.flushInput()
   #time.sleep(1)
   strMessg = _read_data(ser)
   return strMessg


# Read data from the SIM Card (AT Commands)
def _read_data(ser):
	flag_CR=False
	flag_LF=False
	flag_Messg=0
	data = ""
	buffer = bytearray()
	while True:
		# read byte by byte, one byte each time 
		byte = ser.read(1) 
		#print(byte)
		if(byte==b''):
			print("Empty byte")
			ser.flushOutput()
			ser.flushInput()
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
def check_SIM_gprs():

   try:
      ser = serial.Serial("/dev/ttyUSB3")
      ser.baudrate = 9600
      ser.bytesize = serial.EIGHTBITS
      ser.parity = serial.PARITY_NONE
      ser.stopbits = serial.STOPBITS_ONE
      ser.timeout =  2
      ser.flushOutput()
      #print(ser)
   
   except Exception as e:
      print("Error : No Serial RS232.")
      sys.exit(0)
  
  
   while(True):
      strRtnMess = get_Signal_Strength(ser)
      lst_rtn_mssg =  ((strRtnMess.split('\r\n'))[1]).split()[1].split(',')[0]
      strDate = '{0:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())
      intStrengthSignal = int(lst_rtn_mssg)
      if(intStrengthSignal <= 9):
         print("{} CSQ:{} Marginal".format(strDate, intStrengthSignal))
      elif(intStrengthSignal >=10 and intStrengthSignal <=14):
         print("{} CSQ:{} OK".format(strDate, intStrengthSignal))
      elif(intStrengthSignal >=15 and intStrengthSignal <= 19):
         print("{} CSQ:{} Good".format(strDate, intStrengthSignal))
      elif(intStrengthSignal >= 20 and intStrengthSignal <= 30):
         print("{} CSQ:{} Excellent".format(strDate, intStrengthSignal))
      #print(lst_rtn_mssg)
      time.sleep(1)
  

   ser.close()



check_SIM_gprs()




