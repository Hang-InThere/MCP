import json

import httpx
import requests
from mcp.server import FastMCP

mcp = FastMCP("WeatherServer")
OPENWEATHER_API_KEY = "9c19473610fc656ab7c14c43e35b319b"
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
USER_AGENT = "weather-app/1.0"
# 配置高德地图 API 密钥
AMAP_API_KEY = "b5dfc461cbf4f3ee5fa3590a191028b1"
def get_location(address):
    url = "https://restapi.amap.com/v3/geocode/geo"
    params = {
        "key": AMAP_API_KEY,
        "address": address
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("status") == "1" and data.get("geocodes"):
        return data["geocodes"][0]["location"]
    return None
def find_restaurants(address):
    url = "https://restapi.amap.com/v3/place/around"
    company_location = get_location(address)
    params = {
        "key": AMAP_API_KEY,
        "location": company_location,
        "keywords": "饭店",
        "types": "050000",
        "radius": 3000,
        "page": 1,
        "offset": 10
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("status") == "1":
        return data.get("pois", [])
    return "获取饭店信息失败"

async def get_weather(city):
    """
    从OpenWeather API 获取天气信息
    :param city: 城市名称（需要试用英文，如 beijing）
    :return: 天气数据字典；若发生错误，返回包含error信息的字典
    """
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "zh_cn",
    }
    headers = {"User-Agent": USER_AGENT}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(OPENWEATHER_BASE_URL, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP请求错误：{e}"}
        except Exception as e:
            return {"error": f"发生错误：{e}"}


def format_weather_data(data):
    """
    格式化天气数据
    :param data: 天气数据字典
    :return: 格式化后的字符串；若发生错误，返回包含error信息的字符串
    """

    #  如果传入的是字符串，则先转换成字典
    if isinstance(data, str):
        data = json.loads(data)

    if "error" in data:
        return data["error"]
    weather = data["weather"][0]["description"]
    temperature = data["main"]["temp"]
    city = data["name"]
    country = data["sys"]["country"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]

    return f"城市：{city}, {country}\n天气：{weather}\n温度：{temperature}°C\n湿度：{humidity}%\n风速：{wind}m/s"

@mcp.tool()
async def get_weather_tool(city: str):
    """
    获取城市的天气信息
    :param city: 城市名称（需要试用英文，如 beijing）
    :return: 天气数据字典；若发生错误，返回包含error信息的字典
    """
    weather_data = await get_weather(city)
    return format_weather_data(weather_data)

@mcp.tool()
async def get_restaurant_tool(address: str):
    restaurants = await find_restaurants(address)
    return restaurants

if __name__ == "__main__":
    mcp.run(transport="stdio")