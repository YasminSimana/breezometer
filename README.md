# Breezometer backend home assignment - Sensors Data

We have millions of sensors spread around the world. Each sensor sends his data to the server
every minute. The server needs to save the data and send the sensor an “OK” response to let it
know that the data has been saved.

The data received from the device has the following fields:
device_id, timestamp, latitude, longitude, value

## System diagram

![diagram](https://github.com/YasminSimana/breezometer/blob/main/public/system_diagram.png?raw=true)

## Requirements

python 3.9
mysql DB

## How to run the program?

- Get repo
  git clone https://github.com/YasminSimana/breezometer.git
- Run the program
  py -3.9 app.py
