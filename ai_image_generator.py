#!/usr/bin/env python3
"""
AI 이미지 생성기 - Stable Diffusion
VTuber가 주기적으로 그림을 그려서 화면에 표시
"""

import asyncio
import random
import requests
import json
import os
from datetime import datetime

# Hugging Face Inference API
HF_API_KEY = "hf_xxxxx"  # Hugging Face API 키 (필요시 추가)
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"

# 그림 주제 리스트
IMAGE_TOPICS = [
    "a cute anime cat sitting on a desk",
    "beautiful sunset over mountains",
    "futuristic city with neon lights",
    "magical forest with glowing mushrooms",
    "cozy coffee shop interior",
    "space station orbiting earth",
    "cherry blossoms in spring",
    "underwater coral reef with fish",
    "steampunk robot playing music",
    "fantasy castle in the clouds"
]

def generate_image(prompt):
    """Stable Diffusion으로 이미지 생성"""
    headers = {}
    if HF_API_KEY and HF_API_KEY != "hf_xxxxx":
        headers["Authorization"] = f"Bearer {HF_API_KEY}"

    payload = {"inputs": prompt}

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            # 이미지 저장
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_images/ai_art_{timestamp}.png"
            os.makedirs("generated_images", exist_ok=True)

            with open(filename, "wb") as f:
                f.write(response.content)

            print(f"✅ 이미지 생성 완료: {filename}")
            print(f"   주제: {prompt}")
            return filename
        else:
            print(f"❌ API 오류: {response.status_code}")
            print(f"   {response.text}")
            return None
    except Exception as e:
        print(f"❌ 이미지 생성 실패: {e}")
        return None

async def auto_generate_images():
    """주기적으로 이미지 생성"""
    print("🎨 AI 이미지 생성기 시작!")
    print(f"🔗 모델: Stable Diffusion 2.1")
    print()

    while True:
        # 랜덤 주제 선택
        prompt = random.choice(IMAGE_TOPICS)

        print(f"🎨 [{datetime.now().strftime('%H:%M:%S')}] 그림 그리는 중...")
        print(f"   주제: {prompt}")

        # 이미지 생성
        image_path = generate_image(prompt)

        if image_path:
            print(f"   📁 저장됨: {image_path}")

        # 5~10분마다 생성
        wait_time = random.randint(300, 600)
        print(f"⏳ {wait_time//60}분 후 다음 작품...")
        print()
        await asyncio.sleep(wait_time)

async def main():
    """메인 함수"""
    print("=" * 60)
    print("   VTuber AI 이미지 생성기")
    print("=" * 60)
    print()

    await auto_generate_images()

if __name__ == "__main__":
    asyncio.run(main())
