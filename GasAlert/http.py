__author__ = 'Classic'
import urllib2
import urllib
import RPi.GPIO as GPIO

#setup GPIO using Board numbering
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(12, GPIO.OUT) #PIN DE PODER PARA BT

#BT read
#!/usr/bin/env python
import time
import serial
import os.path

while 1:
    ping -c4 104.131.71.204 > /dev/null
    if [ $? == 0 ]
    then
        if os.path.exists(file_path):
            f = open(file_path,"a")
            idbal=f.read()
            f.close()
    else:
        echo "No network connection, restarting wlan0"
        #turning on BT
        GPIO.output(12,True)
        time.sleep(1)

        ser = serial.Serial(
                       port='/dev/ttyAMA0',
                       baudrate = 9600,
                       parity=serial.PARITY_NONE,
                       stopbits=serial.STOPBITS_ONE,
                       bytesize=serial.EIGHTBITS,
                       timeout=1
                   )

        while 1:
                x=ser.readline()
                if(x!=''):
                        print x
                        break
        ser.close()
        btval=x.split(':')
        print btval[0]
        print btval[1]
        print btval[2]

        #turning off BT
        GPIO.output(12,False)
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
            ping -c4 104.131.71.204 > /dev/null
            if [ $? != 0 ] then
                cont+=1
                echo "No network connection, restarting wlan0"
                /sbin/ifdown 'wlan0'
                sleep 5
                /sbin/ifup --force 'wlan0'
            else:
                break
            fi
            if cont==9:
                sudo /sbin/shutdown -r now

        #sending post
        idbal=btval[2]
        f = open("/home/pi/idbal.txt","a")
        f.write(idbal)
        f.close()
    fi

i=1
while 1:
        if(GPIO.input(11) ==0 and GPIO.input(13)==0):
                print('<25%')
                val=15
        elif(GPIO.input(11) ==1 and GPIO.input(13)==0):
                print('<50%')
                val=50
        elif(GPIO.input(11) ==0 and GPIO.input(13)==1):
                print('<75%')
                val=75
        elif(GPIO.input(11) ==1 and GPIO.input(13)==1):
                print('<100%')
                val=100
        i+=1
        query_args = { 'registro_id':idbal, 'porcentaje':val }
        url = 'http://104.131.71.204/medicion-gas/ws_api/public/api/v1/medicion'
        print val
        data = urllib.urlencode(query_args)
        request = urllib2.Request(url, data)
        response = urllib2.urlopen(request).read()
        print response
        time.sleep(30)


