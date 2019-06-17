
import time


#
# AT+CPOWD = 0  ---> Power Off Urgently
# AT+CPOWD = 1   ---> Normal Power Of

# reset / restart
# AT+CFUN=1,1

def reset_sim(ser):
	# Read the HTTP Status
	# mode (GET, POST, HEAD), status (idle, receiving, sending), finish (amount of data transmitted), remain (amount of data to be sent)
	W_buff = [b'at+cfun=1,1\n'] 
	ser.write(W_buff[0])
	ser.flushInput()
	time.sleep(1)
	read_data(ser)





# Read data from the SIM Card (AT Commands)
def read_data(ser):
	flag_CR=False
	flag_LF=False
	flag_Messg=0
	data = ""
	buffer = bytearray()
	while True:
		# read byte by byte, one byte each time 
		byte = ser.read(1) 
		buffer.append(byte[0])
		if (byte == bytes([0x0D])):
			flag_CR=True
		if (flag_CR==True and byte == bytes([0x0A])):
			#print("EOF ...")
			flag_Messg = flag_Messg + 1
		if (flag_Messg == 2) :
			flag_Messg = 0
			flag_CR=False
			flag_LF=False
			break
	#print(byte)
	print(buffer.decode("utf-8"))
   # Message in Hex Format
	#print("Message : "+ ' '.join(hex(c) for c in buffer) )
	print("----------------------------------")


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
	print(buffer.decode("utf-8"))
    # Message in Hex Format
	#print("Message : "+ ' '.join(hex(c) for c in buffer) )
	
	
# Read data from the SIM Card (AT Commands)
def _read_data_serverStatus(ser):
	flag_CR=False
	flag_LF=False
	flag_Messg=0
	data = ""
	buffer = bytearray()
	while True:
		# read byte by byte, one byte each time 
		byte = ser.read(1) 
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
	print(buffer.decode("utf-8"))	
	#print(buffer[:41].decode("utf-8"))
    
    # Message in Hex Format
	#print("Message : "+ ' '.join(hex(c) for c in buffer) )
	#print("Message : "+ ''.join(hex(c) for c in buffer[:41]) )
	mssg_hex = ''.join(hex(c) for c in buffer[:41])
	#print(mssg_hex)
	
	# at+httpaction=1 OK +HTTPACTION: 1,201,194
	# Message : 0x61 0x74 0x2b 0x68 0x74 0x74 0x70 0x61 0x63 0x74 0x69 0x6f 0x6e 0x3d 0x31 0xd 0xa 0x4f 0x4b 0xd 0xa 0xd 0xa 0x2b 0x48 0x54 0x54 0x50 0x41 0x43 0x54 0x49 0x4f 0x4e 0x3a 0x20 0x31 0x2c 0x32 0x30 0x31 0x2c 0x31 0x39 0x34 0xd 0xa
	# '0x610x740x2b0x680x740x740x700x610x630x740x690x6f0x6e0x3d0x310xd0xa0x4f0x4b0xd0xa0xd0xa0x2b0x480x540x540x500x410x430x540x490x4f0x4e0x3a0x200x310x2c0x320x300x31'
	# '  0x2c0x310x390x340xd0xa'
	
	if (mssg_hex == '0x610x740x2b0x680x740x740x700x610x630x740x690x6f0x6e0x3d0x310xd0xa0x4f0x4b0xd0xa0xd0xa0x2b0x480x540x540x500x410x430x540x490x4f0x4e0x3a0x200x310x2c0x320x300x31'):
		print("Status 201 json created and registered")
		return True
	else:
		print("Server Issue: with the json creation in the DB.")
		return False

	print("----------------------------------")



# Read data from the SIM Card (AT Commands)
def read_return_data(ser):
	flag_CR=False
	flag_LF=False
	flag_Messg=0
	data = ""
	buffer = bytearray()
	while True:
		# read byte by byte, one byte each time 
		byte = ser.read(1) 
		buffer.append(byte[0])
		if (byte == bytes([0x0D])):
			flag_CR=True
		if (flag_CR==True and byte == bytes([0x0A])):
			#print("EOF ...")
			flag_Messg = flag_Messg + 1
		if (flag_Messg == 2) :
			flag_Messg = 0
			flag_CR=False
			flag_LF=False
			break

	return buffer


# Read data from the SIM Card (AT Commands)
def _read_return_data(ser):
	flag_CR=False
	flag_LF=False
	flag_Messg=0
	data = ""
	buffer = bytearray()
	while True:
		# read byte by byte, one byte each time 
		byte = ser.read(1) 
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

	return buffer



# Connect the Card SIM: Enter the Code PIN to authenticate 
def connect_Card_SIM(ser):
	print("%s: %s" % ( "Connecting the Sim Card ...", time.ctime(time.time()))  ) 
	W_buff = [b"AT+CPIN?\n"]
	ser.write(W_buff[0])
	ser.flushInput()
	time.sleep(1)
    #ser.flushOutput()
	buffer = read_return_data(ser)
	print(buffer.decode("utf-8"))
	print("Message : "+ ' '.join(hex(c) for c in buffer) )
	print(''.join(hex(c) for c in buffer))
	str_mssg = ''.join(hex(c) for c in buffer)
	if ( str_mssg == '0x410x540x2b0x430x500x490x4e0x3f0xd0xa0x2b0x430x500x490x4e0x3a0x200x520x450x410x440x590xd0xa'):
		#print("Already connected ...")
		print("%s: %s" % ( "Already connected ...", time.ctime(time.time()))  )
	else:
		connect_SIM_PIN(ser)
	print("----------------------------------")

# Connect the Card SIM: Enter the Code PIN to authenticate 
def connect_SIM_PIN(ser):   
	W_buff = [b"AT+CPIN=6703\n"]
	ser.write(W_buff[0])
	ser.flushInput()
	time.sleep(1)
	read_data(ser)



# Check the Card SIM Connection 
def check_Card_SIM_gprs(ser):
	print("%s: %s" % ( "Checking the Connection to the Sim Card ...", time.ctime(time.time()))  ) 
	W_buff = [b"AT+CPIN?\n"]
	ser.write(W_buff[0])
	ser.flushInput()
	time.sleep(1)
	
	try:
		buffer = read_return_data(ser)
	except Exception as e:
		return False
	print(buffer.decode("utf-8"))
	print("Message : "+ ' '.join(hex(c) for c in buffer) )
	print(''.join(hex(c) for c in buffer))
	str_mssg = ''.join(hex(c) for c in buffer)
	if ( str_mssg == '0x410x540x2b0x430x500x490x4e0x3f0xd0xa0x2b0x430x500x490x4e0x3a0x200x520x450x410x440x590xd0xa'):
		#print("Already connected ...")
		print("%s: %s" % ( "SIM Card already connected ...", time.ctime(time.time()))  )
		print("----------------------------------")
		return True
	else:
		W_buff = [b"AT+CPIN=6703\n"]
		ser.write(W_buff[0])
		ser.flushInput()
		time.sleep(1)
		buffer = read_return_data(ser)
		print(buffer.decode("utf-8"))
		print("Message : "+ ' '.join(hex(c) for c in buffer) )
		print(''.join(hex(c) for c in buffer))
		str_mssg = ''.join(hex(c) for c in buffer)
		
		#'0x41 0x54 0x2b 0x43 0x50 0x49 0x4e 0x3d 0x36 0x37 0x30 0x33 0xd 0xa 0x4f 0x4b 0xd 0xa'
		#'0x410x540x2b0x430x500x490x4e0x3d0x360x370x300x330xd0xa0x4f0x4b0xd0xa'
		if ( str_mssg == '0x410x540x2b0x430x500x490x4e0x3d0x360x370x300x330xd0xa0x4f0x4b0xd0xa'):
			#print("Already connected ...")
			print("%s: %s" % ( "SIM Card now connected ...", time.ctime(time.time()))  )
			print("----------------------------------")
			return True
		else:
			return False


def bearer_check_open(ser):
	
	W_buff = [b'at+sapbr=2,1\n'] 
	ser.write(W_buff[0])
	ser.flushInput()
	#time.sleep(1)
	buffer = _read_return_data(ser)
	#
	#buffer = read_return_data(ser)
	print(buffer.decode("utf-8"))
	print(buffer[:25].decode("utf-8"))
	print("Message : "+ ' '.join(hex(c) for c in buffer[:25]) )
	str_mssg = ''.join(hex(c) for c in buffer[:25])
	#str_mssg = ''.join(hex(c) for c in buffer)
	# at+sapbr=2,1
	# +SAPBR: 1,1,"XX.XX.XX.XX"
	# +SAPBR: 1,1   -->python3 0x61 0x74 0x2b 0x73 0x61 0x70 0x62 0x72 0x3d 0x32 0x2c 0x31 0xd 0xa 0x2b 0x53 0x41 0x50 0x42 0x52 0x3a 0x20 0x31 0x2c 0x31
	if ( str_mssg == "0x610x740x2b0x730x610x700x620x720x3d0x320x2c0x310xd0xa0x2b0x530x410x500x420x520x3a0x200x310x2c0x31"):
		#print("Already connected ...")
		print("%s: %s" % ( "Bearer already open and connected ...", time.ctime(time.time()))  )
	else:
		print("%s: %s" % ( "Openning and connecting the Bearer ...", time.ctime(time.time()))  )
		bearer_config_open(ser)
	print("----------------------------------")		



def bearer_config_open(ser):
	
	bearer_test(ser)
	
	# Setting the APN (Access Point Name): gprs.swisscom.ch
	# Configure the bearer profile 1 (APN)
	# Bearer Settings for Applications Based on IP
	# 3 Set bearer parameters
	# 1 Bearer is connected
	W_buff = [b'at+sapbr=3,1,"APN","gprs.swisscom.ch"\n'] 
	ser.write(W_buff[0])
	ser.flushInput()
	time.sleep(1)
	read_data(ser)
	#_read_return_data(ser)

	ser.flushOutput()

	# To open bearer
	# Bearer Settings for Applications Based on IP
	# 1 Set bearer parameters
	# 1 Bearer is connected
	W_buff = [b'at+sapbr=1,1\n'] 
	ser.write(W_buff[0])
	ser.flushInput()
	time.sleep(4)
	read_data(ser)

	# Bearer Settings for Applications Based on IP
	# 2 Query bearer
	# 1 Bearer is connected
	W_buff = [b'at+sapbr=2,1\n'] 
	ser.write(W_buff[0])
	ser.flushInput()
	time.sleep(1)
	read_data(ser)
	#ser.flushOutput()


def bearer_close(ser):
   # To close Bearer
   W_buff = [b'at+sapbr=0,1\n'] 
   ser.write(W_buff[0])
   ser.flushInput()
   time.sleep(1)
   read_data(ser)


def bearer_test(ser):
   # To close Bearer
   W_buff = [b'at+sapbr=?\n'] 
   ser.write(W_buff[0])
   ser.flushInput()
   time.sleep(1)
   _read_data(ser)


# Get the Signal Strength
def get_Signal_Strength(ser):
   W_buff = [b'at+csq\n'] 
   ser.write(W_buff[0])
   ser.flushInput()
   #time.sleep(1)
   _read_data(ser)



# Get the Data Service's status
def get_Data_Service_Status(ser):
   W_buff = [b'at+cgatt?\n'] 
   ser.write(W_buff[0])
   ser.flushInput()
   time.sleep(1)
   _read_data(ser)


# Set the CMNET (APN)
def set_CMNET_APN(ser, apn):
   W_buff = [b'at+cstt='+ apn.encode() + b'\n'] 
   ser.write(W_buff[0])
   ser.flushInput()
   time.sleep(2)
   read_data(ser)


# Bring Up the Wireless connection
def bring_UP_Wireless(ser):
   W_buff = [b'at+ciicr\n'] 
   ser.write(W_buff[0])
   ser.flushInput()
   time.sleep(2)
   read_data(ser)


# Bring Up the Wireless connection
def get_Local_IP(ser):
   W_buff = [b'at+cifsr\n'] 
   ser.write(W_buff[0])
   ser.flushInput()
   time.sleep(1)
   read_data(ser)


# Set the CMNET (APN)
def tcp_Connect(ser, ip, port):
   W_buff = [b'at+cipstart="TCP",'+ ip.encode() + b','+ port.encode() + b'\n'] 
   ser.write(W_buff[0])
   ser.flushInput()
   time.sleep(1)
   read_data(ser)


# Send Data Through TCP connection
def tcp_Data_Length(ser, data_length):
   W_buff = [b'at+cipsend='+ data_length.encode() + b'\n'] 
   ser.write(W_buff[0])
   ser.flushInput()
   time.sleep(1)
   read_data(ser)

# Write Data to send Through TCP connection
def tcp_Data_Send(ser, data_get_post):
   W_buff = [ data_get_post.encode() + b'\n<0x1A'] 
   ser.write(W_buff[0])
   ser.flushInput()
   time.sleep(1)
   read_data(ser)




# HTTP Post method to send data to the remote server. 
def http_post_send(ser, post_server_url, mssg_obj_json):
#def post_send_method(post_server_url , mssg_obj_json):

   # Initialize HTTP Service
   W_buff = [b'at+httpinit\n'] 
   ser.write(W_buff[0])
   ser.flushInput()
   time.sleep(1)
   read_data(ser)


   # Set Parameter for HTTP session
   # CID Bearer profile identifier (Madatory Parameter)
   W_buff = [b'at+httppara="CID",1\n'] 
   ser.write(W_buff[0])
   ser.flushInput()
   time.sleep(1)
   read_data(ser)


   # HTTP client URL (Mandatory Parameter)
   W_buff = [b'at+httppara="URL",' + post_server_url + b'\n'] 
   ser.write(W_buff[0])
   ser.flushInput()
   time.sleep(1)
   read_data(ser)


   # Set the Content type in the Header. Headers={"Content-Type":"Application/json"}
   W_buff = [b'at+httppara="CONTENT","Application/json"\n'] 
   ser.write(W_buff[0])
   ser.flushInput()
   #ser.flushOutput()
   time.sleep(1)
   read_data(ser)

   #ser.flushOutput()

   # POST the data whose size is 500 Bytes and the maximum latency time for inputting is 10000 ms. 
   # It is ready to receive data from UART, and DCD has been set to low.
   # All data has been received over, and DCD is set to high.
   W_buff = [b'at+httpdata=200,1000\n'] 
   ser.write(W_buff[0])
   ser.flushInput()
   #ser.flushOutput()
   time.sleep(4)
   read_data(ser)


   #ser.flushOutput()

   # Send the data to post via UART  
   #W_buff = [b'{\"mod_addr\":\"01\",\"org_id\":\"6A8DDA2569EB\",\"evt_datetime\":\"2018-08-21T10:29:33.333Z\", \"evt_name\":\"Event_Waiter_ON\",\"emp_key\":\"00\",\"prod_plu\":\"000\",\"emp_name\":\"Aukje\"}\n'] 
   #ser.write(W_buff[0])

   # Send the data to post via UART 
   ser.write(mssg_obj_json[0])
   ser.flushInput()
   time.sleep(4)
   read_data(ser)

   #ser.flushOutput()
   # HTTP Method Post  --->  Parameter = 1 
   # POST session start
   W_buff = [b'at+httpaction=1\n'] 
   ser.write(W_buff[0])
   ser.flushInput()
   time.sleep(4)
   bln_stat = _read_data_serverStatus(ser)
   if(bln_stat == True):
      print("True 201 created status")
      return True
   elif(bln_stat == False):
      print("False Not 201 created status ")
      return False
   #ser.flushOutput()


   # HTTP Method Post  --->  Parameter = 1 
   # POST session start
   #W_buff = [b'at+httpaction=?\n'] 
   #ser.write(W_buff[0])
   #ser.flushInput()
   #time.sleep(2)
   #read_data(ser)
   #ser.flushOutput()


def http_get_status(ser):
	# Read the HTTP Status
	# mode (GET, POST, HEAD), status (idle, receiving, sending), finish (amount of data transmitted), remain (amount of data to be sent)
	W_buff = [b'at+httpstatus?\n'] 
	ser.write(W_buff[0])
	ser.flushInput()
	time.sleep(4)
	read_data(ser)


# Read the returned data from the server
def http_read(ser):
   #ser.flushOutput()
   W_buff = [b'at+httpread\n'] 
   ser.write(W_buff[0])
   ser.flushInput()
   time.sleep(4)
   read_data(ser)
   read_data(ser)


# Read the returned data from the server
def http_read_conf(ser):
   #ser.flushOutput()
   W_buff = [b'at+httpread\n'] 
   ser.write(W_buff[0])
   ser.flushInput()
   time.sleep(4)
   read_data(ser)
   obj_ret = read_return_data(ser)
   return obj_ret

# Terminate HTTP service
def http_term(ser):
   ser.flushOutput()
   W_buff = [b'at+httpterm\n'] 
   ser.write(W_buff[0])
   ser.flushInput()
   #time.sleep(1)
   read_data(ser)



