import json

import requests

city = ''

def get_city(city):
    url = 'http://127.0.0.1:5000/get_tianqi_info'

    payload = {'city':city}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            try:
                return {'result':response.json()}
            except Exception as e:
                return {'result':str(e)}
        else:
            return {'result':response.status_code}
    except Exception as e:
        return {'result': str(e)}

def extract_weather_info(weather_data):
    # 提取now节点下的数据
    try :
        now_info = weather_data['showapi_res_body']['now']
        api_datail = now_info['aqiDetail']

        # 组合成新的JSON对象
        result = {
            "area": api_datail['area'],
            "weather": now_info['weather'],
            "temperature": now_info['temperature']
        }
        res = result
    except KeyError as e:
        res = {'error':'数据字段不完整'}
    except Exception as e:
        res = {'error':'数据处理失败'}
    return {'result':res}

weather_data = get_city('南京')
print(extract_weather_info(weather_data))

