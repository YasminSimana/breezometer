# Breezometer backend home assignment - Sensors Data

We have millions of sensors spread around the world. Each sensor sends his data to the server
every minute. The server needs to save the data and send the sensor an “OK” response to let it
know that the data has been saved.

This program will allow us to insert the data comming from the sensors and to get the air pollution in your area (50 m radius) by a given coordinates

## System diagram

![diagram](https://github.com/YasminSimana/breezometer/blob/main/public/system_diagram.png?raw=true)

## Requirements

python 3.9
mysql DB

## How to run the program?

- Get repo

  ```
  git clone https://github.com/YasminSimana/breezometer.git
  ```

- Change the DB connection details in the constant.py file

- Run the program
  ```
  py -3.9 app.py
  ```

## How to use the program?

- In order to insert sensors data to the DB:
  Send POST request to

  ```
  http://[YOUR_HOST]/data
  ```

  With a list of dictionaries with the following fields: "device_id", "timestamp", "latitude", "longitude", "value"
  For example:

  ```
  [{"device_id": 1, "timestamp": "2022-01-01 20:53:00", "latitude": 150.2589, "longitude": 55.2456, "value": 55},
  {"device_id": 1, "timestamp": "2022-01-01 20:52:00", "latitude": 150.2589, "longitude": 55.2456, "value": 35}]
  ```

- In order to get the value of the air pollution in your area (50 m radius):
  Send GET request to
  ```
  http://[YOUR_HOST]/get-avg?lat=[YOUR_LATITUDE]&lon=[YOUR_LONGITUDE]
  ```
