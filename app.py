from controllers.dataHandler import *

insertData([{"device_id": 1, "timestamp": "2022-01-01 10:10:10", "latitude": 150.2589, "longitude": 55.2456, "value": 55}])
print(getAvgData(150.2599, 55.2455))