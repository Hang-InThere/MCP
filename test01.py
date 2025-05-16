import json
import urllib, urllib3, sys, uuid
import ssl
import flask
from flask import request, jsonify

app = flask.Flask(__name__)
def get_tianqi_info(city):
    host = 'https://ali-weather.showapi.com'
    path = '/area-to-weather'
    method = 'GET'
    appcode = 'fd9787dbbf924b8cbcceef86e1cb0167'
    querys = 'area='+city+'&needMoreDay=0&needIndex=0&need3HourForcast=0&needAlarm=0&needHourData=needHourData'
    bodys = {}
    url = host + path + '?' + querys

    http = urllib3.PoolManager()
    headers = {
        'Authorization': 'APPCODE ' + appcode
    }
    response = http.request('GET', url, headers=headers)
    content = response.data.decode('utf-8')
    data = json.loads(content)
    return data

@app.route('/get_tianqi_info', methods=['POST'])
def tianqi_info():
    data = request.get_json()
    if not data:
        return jsonify({'error':'无效的请求数据'}), 400
    city = data.get('city')

    if not city:
        return jsonify({'error':'需要输入城市名称'}), 400
    result = get_tianqi_info(city)
    return result

if __name__ == '__main__':
    app.run(debug=True)