#!/usr/bin/env python3
"""
자동 브라우저 - VTuber가 웹 서핑하는 것처럼 보이게
주기적으로 흥미로운 웹사이트를 방문하고 정보를 수집
"""

import asyncio
import random
import websockets
import json
from datetime import datetime

VTUBER_WS_URL = "ws://localhost:12393/ws"

# Interesting websites list
INTERESTING_SITES = [
    {"url": "https://news.google.com/topstories?hl=en-US", "topic": "latest news"},
    {"url": "https://www.reddit.com/r/science/", "topic": "science news"},
    {"url": "https://github.com/trending", "topic": "trending open source"},
    {"url": "https://www.youtube.com/feed/trending", "topic": "trending videos"},
    {"url": "https://www.wikipedia.org/", "topic": "Wikipedia articles"},
    {"url": "https://techcrunch.com/", "topic": "tech news"},
    {"url": "https://www.producthunt.com/", "topic": "new products"},
]

# Conversation starters
CONVERSATION_STARTERS = [
    "What should we explore today?",
    "Let me find something interesting!",
    "Checking out {topic} right now.",
    "Found something cool in {topic}!",
    "Hey everyone, look at {topic}! This is interesting.",
    "I heard {topic} is trending today, let's check it out!",
]

async def send_to_vtuber(message):
    """Send message to VTuber"""
    try:
        async with websockets.connect(VTUBER_WS_URL) as websocket:
            data = {
                "type": "proactive_speak",
                "text": message
            }
            await websocket.send(json.dumps(data))
            print(f"✅ Sent to VTuber: {message}")
    except Exception as e:
        print(f"❌ VTuber connection failed: {e}")

async def browse_sites():
    """주기적으로 웹사이트 방문"""
    print("🌐 자동 브라우저 시작!")
    print(f"🔗 VTuber 서버: {VTUBER_WS_URL}")
    print()

    while True:
        # 랜덤 웹사이트 선택
        site = random.choice(INTERESTING_SITES)
        topic = site["topic"]

        # 랜덤 대화 시작
        starter = random.choice(CONVERSATION_STARTERS).format(topic=topic)

        print(f"📍 [{datetime.now().strftime('%H:%M:%S')}] {starter}")
        print(f"   🔗 {site['url']}")

        # VTuber에게 알림
        await send_to_vtuber(starter)

        # 30초~1분마다 반복 (더 자주)
        wait_time = random.randint(30, 60)
        print(f"⏳ {wait_time}초 후 다음 활동...")
        print()
        await asyncio.sleep(wait_time)

async def main():
    """메인 함수"""
    print("=" * 60)
    print("   VTuber 자동 브라우저")
    print("=" * 60)
    print()

    await browse_sites()

if __name__ == "__main__":
    asyncio.run(main())
