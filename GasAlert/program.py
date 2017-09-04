import urllib2
import urllib
import RPi.GPIO as GPIO
import subprocess
import socket

#setup GPIO using Board numbering

#GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT) #PIN DE PODER PARA BT
GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#BT read
#!/usr/bin/env python
import time
import serial
import os.path

def check_connectivity(reference):
  print 'Revisando conexion'
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(reference)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False

def restart():
    print 'reiniciando raspberry'
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output

print check_connectivity('104.131.71.204')
file_path="/home/pi/idbal.txt"
while 1:
    if (check_connectivity('104.131.71.204') and os.path.exists(file_path)):
        	f = open(file_path,"r")
        	idbal=f.readline()
            	f.close()
		print idbal
		break
    else:
        print "No hay conexion a internet, tomando datos del BT"
        #turning on BT
        GPIO.output(11,GPIO.HIGH)
        time.sleep(1)

        ser = serial.Serial(
                       port='/dev/ttyAMA0',
                       baudrate = 9600,
                       parity=serial.PARITY_NONE,
                       stopbits=serial.STOPBITS_ONE,
                       bytesize=serial.EIGHTBITS,
                       timeout=1
                   )
	ser.flush()
	time.sleep(1)

        while 1:
                x=ser.readline()
                if(x!=''):
			try:
				btval=x.split(':')
				print btval[0]
        			print btval[1]
        			print btval[2]
                        	break
			except:
				print "BT vacio"
        ser.close()
#        btval=x.split(':')
       	print btval[0]
        print btval[1]
        print btval[2]

        #turning off BT
        GPIO.output(11,GPIO.LOW)
        time.sleep(1)

        import os
        os.remove("/etc/wpa_supplicant/wpa_supplicant.conf")


        myString="ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev"
        mystr2="\nupdate_config=1"

        mystr3="\nnetwork={"
        mystr4='\n        ssid="'
        mystr41=btval[0]
        mystr5='"\n        psk="'
        mystr51=btval[1]
        mystr6='"\n        key_mgmt=WPA-PSK'
        mystr7='\n}'
        b = open("/etc/wpa_supplicant/wpa_supplicant.conf","a")
        b.write(myString+mystr2+mystr3+mystr4+mystr41+mystr5+mystr51+mystr6+mystr7)
        b.close()


        # time.sleep(30)
        # sudo ifdown wlan0
        # sudo ifup wlan0
        # time.sleep(30)
        cont=1
        while cont<10:
            time.sleep(5)
            if (~check_connectivity('104.131.71.204')):
                cont+=1
                print "No network connection, restarting wlan0"
		from subprocess import Popen, PIPE 
		my_cmd = "sudo service networking restart"   # might be wlan0
		proc = subprocess.Popen(my_cmd, shell=True, stdout=subprocess.PIPE)
                #/sbin/ifdown 'wlan0'
                #sleep 5
                #/sbin/ifup --force 'wlan0'
            else:
                break
            if cont==9:
                print("imposible - reiniciando equipo")
		restart()
        #sending post
        idbal=btval[2]
	os.remove("/home/pi/idbal.txt")
        f = open("/home/pi/idbal.txt","a")
        f.write(idbal)
        f.close()
	break

i=1
while 1:
	b1=GPIO.input(31)
	b2=GPIO.input(33)
	b3=GPIO.input(35)
	b4=GPIO.input(37)
	val=10*(b1*1+b2*2+b3*4+b4*8)
	print val
	print "%"
        i+=1
	try:
		query_args = { 'registro_id':idbal, 'porcentaje':val }
        	url = 'http://104.131.71.204/medicion-gas/ws_api/public/api/v1/medicion'
        	print val
        	data = urllib.urlencode(query_args)
        	request = urllib2.Request(url, data)
        	response = urllib2.urlopen(request).read()
        	print response
        	time.sleep(30)
	except:
		if(~check_connectivity('104.131.71.204')):
			restart()
