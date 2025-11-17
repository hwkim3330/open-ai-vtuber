#!/usr/bin/env python3
"""
판교 날씨 서비스
실시간 날씨 정보를 가져와서 VTuber에게 전달
"""

import asyncio
import requests
import json
from datetime import datetime

VTUBER_WS_URL = "ws://localhost:12393/ws"

# 판교 좌표
PANGYO_LAT = 37.3945
PANGYO_LON = 127.1110

def get_weather():
    """Open-Meteo API로 판교 날씨 가져오기 (무료, API 키 불필요)"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={PANGYO_LAT}&longitude={PANGYO_LON}&current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m&timezone=Asia/Seoul"

        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            current = data['current']

            temp = current['temperature_2m']
            humidity = current['relative_humidity_2m']
            wind_speed = current['wind_speed_10m']
            weather_code = current['weather_code']

            # 날씨 코드 해석
            weather_desc = get_weather_description(weather_code)

            weather_info = {
                'location': '판교',
                'temperature': f"{temp}°C",
                'humidity': f"{humidity}%",
                'wind_speed': f"{wind_speed}km/h",
                'condition': weather_desc,
                'time': datetime.now().strftime('%H:%M')
            }

            return weather_info
        else:
            print(f"❌ 날씨 API 오류: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 날씨 정보 가져오기 실패: {e}")
        return None

def get_weather_description(code):
    """WMO weather code to English description"""
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Fog",
        51: "Light drizzle",
        53: "Drizzle",
        55: "Heavy drizzle",
        61: "Rain",
        63: "Rain",
        65: "Heavy rain",
        71: "Snow",
        73: "Snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Rain showers",
        81: "Rain showers",
        82: "Heavy showers",
        85: "Snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with hail"
    }
    return weather_codes.get(code, "Unknown")

async def broadcast_weather():
    """주기적으로 날씨 방송"""
    import websockets

    print("🌤️ 판교 날씨 서비스 시작!")
    print(f"📍 위치: 판교 ({PANGYO_LAT}, {PANGYO_LON})")
    print()

    while True:
        weather = get_weather()

        if weather:
            print(f"☀️ [{weather['time']}] 판교 날씨")
            print(f"   🌡️  온도: {weather['temperature']}")
            print(f"   💧 습도: {weather['humidity']}")
            print(f"   💨 풍속: {weather['wind_speed']}")
            print(f"   ☁️  날씨: {weather['condition']}")

            # Send to VTuber
            try:
                async with websockets.connect(VTUBER_WS_URL) as websocket:
                    message = f"📍 Weather update for {weather['location']}: {weather['condition']}, {weather['temperature']}, humidity {weather['humidity']}"
                    data = {
                        "type": "proactive_speak",
                        "text": message
                    }
                    await websocket.send(json.dumps(data))
                    print(f"   ✅ Sent to VTuber: {message}")
            except Exception as e:
                print(f"   ❌ VTuber connection failed: {e}")

        # Broadcast every 30 minutes
        print(f"⏳ Next weather broadcast in 30 minutes...")
        print()
        await asyncio.sleep(1800)

async def main():
    """Main function"""
    print("=" * 60)
    print("   Pangyo Weather Forecaster")
    print("=" * 60)
    print()

    await broadcast_weather()

if __name__ == "__main__":
    asyncio.run(main())
