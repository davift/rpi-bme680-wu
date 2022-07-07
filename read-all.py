#!/usr/bin/env python

#
# version 2
# date 2021-11-19
# https://github.com/davift/rpi-bme680-wu
#

import bme680
import time
import os
import math

# Initializing the BM680 module.
try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# These calibration data can safely be commented out, if desired.
for name in dir(sensor.calibration_data):

    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)

#        if isinstance(value, int):
#            print('{}: {}'.format(name, value))

# These oversampling settings can be tweaked to change the balance between accuracy and noise in the data.
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

#print('\n\nInitial reading:')
for name in dir(sensor.data):
    value = getattr(sensor.data, name)

#    if not name.startswith('_'):
#        print('{}: {}'.format(name, value))

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Up to 10 heater profiles can be configured, each with their own temperature and duration.
#sensor.set_gas_heater_profile(200, 150, nb_profile=1)
#sensor.select_gas_heater_profile(1)

# Initializing all the variables that will compose the average.
tem = tem2 = pre = pre2 = hum = hum2 = air = air2 = dew = 0

# Initializing the variables of the two counters.
count = count2 = 1

# Gathering the redentials from the system's environment variables.

wu_id = os.environ.get('WU_ID')
wu_pass = os.environ.get('WU_PASS')

# Testing if the credentials were successfully acquired.
#print(wu_id, wu_pass)

try:
    while True:
        time.sleep(1)

# Print counters.
#        print("CounterOne {0}\tCounterTwo {1}".format(count,count2))

#        if sensor.get_sensor_data():
#            output = '{3:.0f}, {0:.2f} C, {1:.2f} hPa, {2:.2f} %'.format(sensor.data.temperature,sensor.data.pressure,sensor.data.humidity,count)

        if sensor.data.heat_stable:
            air = air + sensor.data.gas_resistance
            print('{0}, {1} Ohms'.format(output,sensor.data.gas_resistance))

        tem = tem + sensor.data.temperature
        pre = pre + sensor.data.pressure
        hum = hum + sensor.data.humidity
        count = count + 1

        if count > 60:

# Calculating the dew point based on the averages of the first counter.
            dew = (((math.log(hum/60/100))+((17.62*tem/60)/(243.12+tem/60)))*243.12)/(17.62-((math.log(hum/60/100))+((17.62*tem/60)/(243.12+tem/60))))

# Pushing the data to Weather Underground. The values will be the average of the last 60 seconds.
            _ = os.system('curl --silent "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?ID={0}&PASSWORD={1}&dateutc=now&action=updateraw&tempf={2:.1f}&baromin={3:.1f}&humidity={4:.1f}&aqi={5:.0f}&dewptf={6:.1f}" > /dev/null 2>&1'.format(wu_id,wu_pass,tem/60*9/5+32,pre/60/33.86,hum/60,air/60/1000,dew*9/5+32))

            count2 = count2 + 1
            tem2 = tem2 + tem/60
            pre2 = pre2 + pre/60
            hum2 = hum2 + hum/60
            air2 = air2 + air/60

            tem = 0
            pre = 0
            hum = 0
            air = 0
            dew = 0
            count = 1

        if count2 > 10:

# Additional code that runs in a multiple of the first counter.
#            ADD HERE ANY CODE

            tem2 = 0
            pre2 = 0
            hum2 = 0
            air2 = 0
            count2 = 1

except KeyboardInterrupt:
    pass
