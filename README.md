# METARMap
Raspberry Pi project to visualize flight conditions on a map using WS8211 LEDs addressed via NeoPixel

## Detailed instructions
I've created detailed instructions about the setup and parts used here: https://slingtsi.rueker.com/making-a-led-powered-metar-map-for-your-wall/

## Software Setup
* Install [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/) on SD card
* [Enable Wi-Fi and SSH](https://medium.com/@danidudas/install-raspbian-jessie-lite-and-setup-wi-fi-without-access-to-command-line-or-using-the-network-97f065af722e)
* Install SD card and power up Raspberry Pi
* SSH (using [Putty](https://www.putty.org) or some other SSH tool) into the Raspberry and configure password and timezones
	* passwd
	* sudo raspi-config
* Update packages 
	* sudo apt-get update
	* sudo apt-get upgrade
* Copy the **metar.py**, **airports**, **startup.sh**, **refresh.sh** scripts into the pi home directory
* Install python3 and pip3 if not already installed
	* sudo apt-get install python3
	* sudo apt-get install python3-pip
* Install required python libraries for the project
	* pip install -r requirements.txt
* Attach WS8211 LEDs to Raspberry Pi, if you are using just a few, you can connect the directly, otherwise you may need to also attach external power to the LEDs. For my purpose with 22 powered LEDs it was fine to just connect it directly. You can find [more details about wiring here](https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring).
* Test the script by running it directly (it needs to run with root permissions to access the GPIO pins):
	* sudo python3 main.py
* Make appropriate changes to the **airports** file for the airports you want to use and change the **metar.py** script to the correct **LED_COUNT** (including empty lines if you have LEDs in between airports that will stay off) and **LED_INITIAL_BRIGHTNESS** if you want to change it

## TODO

- Add photoresistor circuit for detecting ambient light. [Instructions here](https://pimylifeup.com/raspberry-pi-light-sensor/).
