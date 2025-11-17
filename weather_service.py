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
    """WMO 날씨 코드를 한국어로 변환"""
    weather_codes = {
        0: "맑음",
        1: "대체로 맑음",
        2: "구름 조금",
        3: "흐림",
        45: "안개",
        48: "안개",
        51: "이슬비",
        53: "이슬비",
        55: "이슬비",
        61: "비",
        63: "비",
        65: "강한 비",
        71: "눈",
        73: "눈",
        75: "강한 눈",
        77: "진눈깨비",
        80: "소나기",
        81: "소나기",
        82: "강한 소나기",
        85: "눈",
        86: "강한 눈",
        95: "천둥번개",
        96: "천둥번개와 우박",
        99: "천둥번개와 우박"
    }
    return weather_codes.get(code, "알 수 없음")

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

            # VTuber에게 전달
            try:
                async with websockets.connect(VTUBER_WS_URL) as websocket:
                    message = f"📍 {weather['location']} 날씨: {weather['condition']}, {weather['temperature']}, 습도 {weather['humidity']}"
                    data = {
                        "type": "proactive_speak",
                        "text": message
                    }
                    await websocket.send(json.dumps(data))
                    print(f"   ✅ VTuber에게 전달: {message}")
            except Exception as e:
                print(f"   ❌ VTuber 연결 실패: {e}")

        # 30분마다 날씨 방송
        print(f"⏳ 30분 후 다음 날씨 방송...")
        print()
        await asyncio.sleep(1800)

async def main():
    """메인 함수"""
    print("=" * 60)
    print("   판교 날씨 기상캐스터")
    print("=" * 60)
    print()

    await broadcast_weather()

if __name__ == "__main__":
    asyncio.run(main())
