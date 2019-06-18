#!/bin/bash


sleep 1
echo `sudo modprobe usbserial vendor=0x12d1 product=0x1506`
sleep 1 

echo "`date`:  Script to ensure that the QoS NB-IoT Python program is running."


strprocess='/home/pi/QOS/QoS_NB-IoT_gui.py'
outp="$(ps aux | grep python | awk '{print $13}' | head -n1)"

echo "${outp}"
echo "-----------------------------------"
echo "${strprocess}"

if [ "$outp" = "$strprocess" ]; then 
	echo "==> ${outp} already running..." 
else
	echo "==> Restarting the process ..."
	echo `sudo su pi -c "DISPLAY=:0.0 sudo /usr/bin/python3 /home/pi/QOS/QoS_NB-IoT_gui.py"`
	#echo `sudo /usr/bin/python3 /home/pi/QOS/QoS_NB-IoT_gui.py`
  

fi 



