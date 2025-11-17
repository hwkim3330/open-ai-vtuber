#!/usr/bin/env python3
"""
AI SVG 생성기 - Mistral AI로 즉시 그림 그리기
이미지 API 대기 없이 SVG 코드로 빠르게 생성
"""

import asyncio
import random
import requests
import json
import os
from datetime import datetime

MISTRAL_API_KEY = "bN77wfiqQRd7EYrUdDA4PN9T5p4fTKht"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# SVG 주제
SVG_TOPICS = [
    "귀여운 고양이",
    "아름다운 산",
    "미래 도시",
    "별이 빛나는 밤",
    "꽃다발",
    "우주선",
    "나비",
    "로봇"
]

def generate_svg(topic):
    """Mistral AI로 SVG 코드 생성"""
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""Create a simple, beautiful SVG illustration of {topic}.
Output ONLY the SVG code, no explanation.
Make it colorful and visually appealing.
Size should be 400x400.
Use vibrant colors and simple shapes."""

    payload = {
        "model": "mistral-large-latest",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    try:
        response = requests.post(MISTRAL_API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            svg_code = data['choices'][0]['message']['content']

            # SVG 코드만 추출
            if '<svg' in svg_code and '</svg>' in svg_code:
                start = svg_code.find('<svg')
                end = svg_code.find('</svg>') + 6
                svg_code = svg_code[start:end]

            # 저장
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_images/svg_art_{timestamp}.svg"
            os.makedirs("generated_images", exist_ok=True)

            with open(filename, "w", encoding="utf-8") as f:
                f.write(svg_code)

            print(f"✅ SVG 생성 완료: {filename}")
            print(f"   주제: {topic}")
            return filename
        else:
            print(f"❌ API 오류: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ SVG 생성 실패: {e}")
        return None

async def auto_generate_svgs():
    """주기적으로 SVG 생성"""
    print("🎨 AI SVG 생성기 시작!")
    print(f"🔗 모델: Mistral Large (초고속 생성)")
    print()

    while True:
        # 랜덤 주제
        topic = random.choice(SVG_TOPICS)

        print(f"🎨 [{datetime.now().strftime('%H:%M:%S')}] 그림 그리는 중...")
        print(f"   주제: {topic}")

        # SVG 생성
        svg_path = generate_svg(topic)

        if svg_path:
            print(f"   📁 저장됨: {svg_path}")

        # 1~2분마다 생성
        wait_time = random.randint(60, 120)
        print(f"⏳ {wait_time}초 후 다음 작품...")
        print()
        await asyncio.sleep(wait_time)

async def main():
    """메인 함수"""
    print("=" * 60)
    print("   VTuber AI SVG 생성기 (초고속)")
    print("=" * 60)
    print()

    await auto_generate_svgs()

if __name__ == "__main__":
    asyncio.run(main())
