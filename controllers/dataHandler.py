import mysql.connector
from datetime import datetime, timedelta
from timeit import default_timer as timer


# TODO - get vars from config file
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="yasminsheffer21",
  database="mydatabase"
)
mycursor = mydb.cursor(buffered=True)

mycursor.execute("CREATE TABLE IF NOT EXISTS sensors (id INT PRIMARY KEY, lat DOUBLE, lon DOUBLE)")
# TODO - create a new sensorsData table every hour + name include date+hour
mycursor.execute("CREATE TABLE IF NOT EXISTS sensorsData (id INT, time TIMESTAMP,lat DOUBLE, lon DOUBLE, data DOUBLE, PRIMARY KEY(id, time))")

"""insertData gets an array of dicts with the relevant data
returns 'OK' if the insertion succeeded or 'FAIL' if not"""
def insertData(dataArr):
    start = timer()
    # for multilines data
    for data in dataArr:
        print("data: ", data)
        # check if sensor is in sensors table
        mycursor.execute(
            "SELECT id, COUNT(*) FROM sensors WHERE id = %s",
            (data['device_id'],)
        )
        # gets the number of rows affected by the command executed
        row_count = mycursor.rowcount
        if row_count == 0:
            sql = "INSERT INTO sensors (id, lat, lon) VALUES (%s, %s, %s)"
            val = (data['device_id'], data['latitude'], data['longitude'])
            try:
                mycursor.execute(sql, val)
                mydb.commit()
                end = timer()
                print(end - start) # Time in seconds
                return "OK"
            except:
                end = timer()
                print(end - start) # Time in seconds
                return "FAIL"

        #insert data row into sensorsData table
        sql = "INSERT INTO sensorsData (id, time, lat, lon, data) VALUES (%s, %s, %s, %s, %s)"
        val = (data['device_id'], data['timestamp'], data['latitude'], data['longitude'], data['value'])
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            end = timer()
            print(end - start) # Time in seconds
            return "OK"
        except:
            end = timer()
            print(end - start) # Time in seconds
            return "FAIL"

"""getAvgData gets 2 numbers - lat and lon
returns the avg data calculated from all sensors in the 50m radius for the last 5 min or False in case of an error"""
def getAvgData(lat, lon):
    timeDuration = datetime.now() - timedelta(minutes=5)
    # TODO - change the hard coded number repesent the 50 m to constant var
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
        HAVING distance < 0.0310686"""

    val = (lat, lon, lat)
    try:
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
    except:
        return False
    # get only ids
    ids = tuple([item[0] for item in myresult])
    # get all relevant data rows
    sql = "SELECT id, data, time FROM sensorsData WHERE id IN {} and time >= '{}'".format(ids, timeDuration)
    try:
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        sumData = 0
        for x in myresult:
            sumData += x[1]

        avgData = sumData / len(myresult)
        print(avgData)
        return avgData
    except:
        return False