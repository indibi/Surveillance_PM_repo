#!/bin/bash
#autostart.sh
#Created for the Solid Mind Project Group
#Used to add autostart script after OS fully boots which is necessery
#for GUI dependent processes
#This script creates autostart directory under .config and initialize autostart script in it.

mkdir /home/pi/.config/autostart
cd /home/pi/.config/autostart/
{ echo "[Desktop Entry]" ; echo "Type=Application" ; echo "Name=Survaillance-Protective_Measures" ; echo "Exec=/usr/bin/python3 /home/pi/project/Survaillance_PM_repo/controller.py" ; } >> survaillance.desktop
