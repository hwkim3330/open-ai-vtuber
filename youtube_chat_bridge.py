#!/usr/bin/env python3
"""
YouTube 라이브 채팅 → Open-LLM-VTuber 브릿지
채팅 메시지를 읽어서 VTuber에게 전달합니다.
"""

import asyncio
import websockets
import json
import time
from urllib.parse import urlparse, parse_qs

# pip install pytchat 필요
try:
    import pytchat
    PYTCHAT_AVAILABLE = True
except ImportError:
    PYTCHAT_AVAILABLE = False
    print("⚠️  pytchat가 설치되지 않았습니다. 설치: pip install pytchat")

VTUBER_WS_URL = "ws://localhost:12393/ws"
YOUTUBE_VIDEO_ID = "YOUR_YOUTUBE_VIDEO_ID"  # YouTube 라이브 비디오 ID (예: NoALowWIJro)

async def send_to_vtuber(message, author):
    """VTuber에게 메시지 전달"""
    try:
        async with websockets.connect(VTUBER_WS_URL) as websocket:
            # 텍스트 메시지 전송
            data = {
                "type": "text_input",
                "text": f"[{author}님] {message}"
            }
            await websocket.send(json.dumps(data))
            print(f"✅ VTuber에게 전달: [{author}] {message}")
    except Exception as e:
        print(f"❌ VTuber 연결 실패: {e}")

async def monitor_youtube_chat():
    """YouTube 채팅 모니터링"""
    if not PYTCHAT_AVAILABLE:
        print("❌ pytchat 라이브러리가 필요합니다!")
        print("   설치: pip install pytchat")
        return

    print(f"🎥 YouTube 라이브 채팅 모니터링 시작")
    print(f"📺 비디오 ID: {YOUTUBE_VIDEO_ID}")
    print(f"🔗 VTuber 서버: {VTUBER_WS_URL}")
    print()

    try:
        chat = pytchat.create(video_id=YOUTUBE_VIDEO_ID)

        while chat.is_alive():
            for c in chat.get().sync_items():
                author = c.author.name
                message = c.message

                # 채팅 출력
                print(f"💬 [{author}]: {message}")

                # VTuber에게 전달
                await send_to_vtuber(message, author)

            await asyncio.sleep(1)  # 1초마다 체크

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        print("   YouTube 라이브 스트림이 활성화되어 있는지 확인하세요.")

def extract_video_id(url):
    """YouTube URL에서 비디오 ID 추출"""
    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]
    elif "youtube.com" in url:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        return params.get("v", [None])[0]
    return url

async def main():
    """메인 함수"""
    print("=" * 60)
    print("   YouTube 라이브 채팅 → VTuber 브릿지")
    print("=" * 60)
    print()

    # 채팅 모니터링 시작
    await monitor_youtube_chat()

if __name__ == "__main__":
    asyncio.run(main())
