from flask import config
import mysql.connector
from datetime import datetime, timedelta
from timeit import default_timer as timer
import json
import constant

# TODO - get vars from config file
mydb = mysql.connector.connect(
  host=constant.HOST,
  user=constant.USER,
  password=constant.PASSWORD,
  database=constant.DATABASE
)
mydb.autocommit = True

mycursor = mydb.cursor(buffered=True)

mycursor.execute("CREATE TABLE IF NOT EXISTS sensors (id INT PRIMARY KEY, lat DOUBLE, lon DOUBLE)")
# TODO - create a new sensorsData table every hour + name include date+hour
mycursor.execute("CREATE TABLE IF NOT EXISTS sensorsData (id INT, time TIMESTAMP,lat DOUBLE, lon DOUBLE, data DOUBLE, PRIMARY KEY(id, time))")


"""insertData gets an array of dicts with the relevant data
returns 'OK' if the insertion succeeded or 'FAIL' if not"""
def insertData(dataArr):
    start = timer()
    # for multilines data
    for data in json.loads(dataArr):
        # check if sensor is in sensors table
        mycursor.execute(
            "SELECT COUNT(*) FROM sensors WHERE id = %s",
            (data['device_id'],)
        )
        # gets the number of rows affected by the command executed
        myresult = mycursor.fetchall()
        if myresult[0][0] == 0:
            sql = "INSERT INTO sensors (id, lat, lon) VALUES (%s, %s, %s)"
            val = (data['device_id'], data['latitude'], data['longitude'])
            try:
                mycursor.execute(sql, val)
            except Exception as e:
                # TODO - insert errors to logger
                print(e)
                end = timer()
                print(end - start) # Time in seconds
                return "FAIL"
        # check if data row is in sensorsData table
        mycursor.execute(
            "SELECT COUNT(*) FROM sensorsData WHERE id = %s and time = %s",
            (data['device_id'], data['timestamp'])
        )
        # gets the number of rows affected by the command executed
        myresult = mycursor.fetchall()
        if myresult[0][0] > 0:
            continue
        #insert data row into sensorsData table
        sql = "INSERT INTO sensorsData (id, time, lat, lon, data) VALUES (%s, %s, %s, %s, %s)"
        val = (data['device_id'], data['timestamp'], data['latitude'], data['longitude'], data['value'])
        try:
            mycursor.execute(sql, val)
        except Exception as e:
            print(e)
            end = timer()
            print(end - start) # Time in seconds
            return "FAIL"
    end = timer()
    print(end - start) # Time in seconds
    return "OK"

"""getAvgData gets 2 numbers - lat and lon
returns the avg data calculated from all sensors in the 50m radius for the last 5 min 
or 'False' in case of an error or if there are no results"""
def getAvgData(lat, lon):
    timeDuration = datetime.now() - timedelta(minutes=5)
    # gets the sensors ids who is in the required radius
    sql = """
        SELECT id, ( 
            3959 * acos (
            cos ( radians(%s) )
            * cos( radians( lat ) )
            * cos( radians( lon ) - radians(%s) )
            + sin ( radians(%s) )
            * sin( radians( lat ) )
            )
        ) AS distance
        FROM sensors
        HAVING distance < %s"""

    val = (lat, lon, lat, constant.RADIUS)
    try:
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        # in case there are no sensors in the requested radius
        if len(myresult) == 0:
            return "False"
    except Exception as e:
        print(e)
        return "False"
    # get only ids
    ids = tuple([item[0] for item in myresult])
    # get all relevant data rows
    sql = "SELECT id, data, time FROM sensorsData WHERE id IN {} and time >= '{}'".format(ids, timeDuration)
    try:
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        # in case there is no data for the requested sensors and time
        if len(myresult) == 0:
            return "False"
        sumData = 0
        for x in myresult:
            sumData += x[1]
        avgData = sumData / len(myresult)
        return {"avg data": avgData}
    except Exception as e:
        print(e)
        return "False"