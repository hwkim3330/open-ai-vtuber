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

# 흥미로운 웹사이트 목록
INTERESTING_SITES = [
    {"url": "https://news.google.com/topstories?hl=ko", "topic": "최신 뉴스"},
    {"url": "https://www.reddit.com/r/science/", "topic": "과학 뉴스"},
    {"url": "https://github.com/trending", "topic": "인기 오픈소스 프로젝트"},
    {"url": "https://www.youtube.com/feed/trending", "topic": "인기 YouTube 동영상"},
    {"url": "https://www.wikipedia.org/", "topic": "위키피디아 랜덤 문서"},
    {"url": "https://techcrunch.com/", "topic": "기술 뉴스"},
    {"url": "https://www.producthunt.com/", "topic": "새로운 제품들"},
]

# 대화 주제 예시
CONVERSATION_STARTERS = [
    "오늘은 뭘 해볼까요?",
    "재미있는 것 좀 찾아볼게요!",
    "지금 {topic} 확인해보는 중이에요.",
    "{topic}에서 흥미로운 걸 발견했어요!",
    "여러분, {topic} 보세요! 이거 재미있네요.",
    "오늘 {topic}가 화제라고 하는데, 한번 볼까요?",
]

async def send_to_vtuber(message):
    """VTuber에게 메시지 전달"""
    try:
        async with websockets.connect(VTUBER_WS_URL) as websocket:
            data = {
                "type": "proactive_speak",
                "text": message
            }
            await websocket.send(json.dumps(data))
            print(f"✅ VTuber에게 전달: {message}")
    except Exception as e:
        print(f"❌ VTuber 연결 실패: {e}")

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

        # 3~5분마다 반복
        wait_time = random.randint(180, 300)
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
