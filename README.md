# Breezometer backend home assignment - Sensors Data

We have millions of sensors spread around the world. Each sensor sends his data to the server
every minute. The server needs to save the data and send the sensor an “OK” response to let it
know that the data has been saved.

The data received from the device has the following fields:
device_id, timestamp, latitude, longitude, value

## System diagram

![alt text](https://github.com/YasminSimana/breezometer/blob/master/public/system_diagram.png?raw=true)

## Requirements

python 3.9
access to cloud mongodb (or ask me for the user and password + give me your IP so I will add it to the whitelist)

## How to run the program?

- pull the git repo
- In the terminal enter:
  py -3.10 app.py
