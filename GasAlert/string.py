#sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
        ssid="AndroidHP"
        psk="simbarin1234"
        key_mgmt=WPA-PSK
}