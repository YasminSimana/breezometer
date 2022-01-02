from controllers.dataHandler import *
from flask import Flask, request

app = Flask(__name__)

@app.route('/data', methods = ['POST'])
def data():
    params = request.data
    return insertData(params)

@app.route('/get-avg', methods = ['GET'])
def avgData():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    return getAvgData(lat, lon)

if __name__ == "__main__":
    app.run()