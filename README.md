# rpi-bme680-wu

![my outdoor weather station](https://github.com/davift/rpi-bme680-wu/blob/main/weather-station.png)

Python code for **Raspberry Pi + BME680** to update the cloud service **WeatherUnderground**.\
This code is a fork of https://github.com/pimoroni/bme680-python. \
Version 2\
2021-11-19

## Purpose

Collect data from all the sensors, calculate and send the average of each over a period to prevent variation/noise in the acquisition.\
Optionally, a second counter, multiple of the first counter, can execute an additional task.\
The credentials are not hard-coded, but Linux environment variables.

## Installation

Clone this repo and execute the installation script of BME680 module:

```
git clone https://github.com/davift/rpi-bme680-wu.git
cd rpi-bme680-wu
sudo ./bme680-instal.sh
```

Add your WU credentials as environment variables in file `/etc/environment`:

```
WU_ID=__ID_HERE__
WU_PASS=__PASSWORD_HERE__
```

Then, create service:

```
sudo nano /etc/systemd/system/rpi-bme680-wu.service
```

Add the following content replacing the path accordingly:

```
[Unit]
Description=RaspberryPi_BME680_WeatherUnderground

[Service]
User=root
Restart=always
RestartSec=10
EnvironmentFile=/etc/environment
WorkingDirectory=/__PATH__/rpi-bme680-wu/
ExecStart=python read-all.py
StandardOutput=file:/__PATH__/rpi-bme680-wu/session-output.log
StandardError=append:/__PATH__/rpi-bme680-wu/alltimes-error.log

[Install]
WantedBy=multi-user.target
```

Enable to load the script during the boot and start the service:

```
sudo systemctl daemon-reload
sudo systemctl enable rpi-bme680-wu.service
sudo systemctl start rpi-bme680-wu.service
```

## Execution

Ideally, this code runs as a service managed by the `systemd`, which will restart if it crashes, and load on boot.\
Additional commands for managing this service are:

```
sudo systemctl status rpi-bme680-wu.service
sudo systemctl stop rpi-bme680-wu.service
```

## Unities

This code converts the acquired unities to meet the WU requirements.\
The dew point is calculated from temperature and humidity.\
The air quality index is not supported by WU.

## WU URL Vars

* winddir - 0-360 instantaneous wind direction
* windspeedmph - mph instantaneous wind speed
* windgustmph - mph current wind gust, using software specific time period
* windgustdir - 0-360 using software specific time period
* windspdmph_avg2m  - mph 2 minute average wind speed mph
* winddir_avg2m - 0-360 2 minute average wind direction
* windgustmph_10m - mph past 10 minutes wind gust mph
* windgustdir_10m - 0-360 past 10 minutes wind gust direction
* humidity - % outdoor humidity 0-100%
* dewptf - F outdoor dewpoint F
* tempf - F outdoor temperature
  * for extra outdoor sensors use temp2f, temp3f, and so on
* rainin - rain inches over the past hour) -- the accumulated rainfall in the past 60 min
* dailyrainin - rain inches so far today in local time
* baromin - barometric pressure inches
* weather - text -- metar style (+RA)
* clouds - text -- SKC, FEW, SCT, BKN, OVC
* soiltempf - F soil temperature
  * for sensors 2,3,4 use soiltemp2f, soiltemp3f, and soiltemp4f
* soilmoisture - %
  * for sensors 2,3,4 use soilmoisture2, soilmoisture3, and soilmoisture4
* leafwetness - %
  * for sensor 2 use leafwetness2
* solarradiation - W/m^2
* UV - index
* visibility - nm visibility
* indoortempf - F indoor temperature F
* indoorhumidity - % indoor humidity 0-100

## Project

https://rpiz.dftorres.ca/
