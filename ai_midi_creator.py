#!/usr/bin/env python3
"""
AI MIDI 음악 생성기 - Mistral AI로 즉시 음악 만들기
"""

import asyncio
import random
import requests
import json
import os
from datetime import datetime

MISTRAL_API_KEY = "bN77wfiqQRd7EYrUdDA4PN9T5p4fTKht"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# 음악 스타일
MUSIC_STYLES = [
    "happy upbeat melody",
    "calm relaxing ambient",
    "energetic electronic",
    "cheerful piano tune",
    "peaceful nature sounds",
    "exciting game music"
]

def generate_midi_code(style):
    """Mistral AI로 MIDI Python 코드 생성"""
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""Generate Python code using the 'midiutil' library to create a {style}.
Output ONLY Python code that creates a MIDI file.
The code should:
1. Import from midiutil import MIDIFile
2. Create a simple melody (10-20 notes)
3. Save to a file
4. Be executable without modification

Example structure:
from midiutil import MIDIFile
track = 0
channel = 0
time = 0
tempo = 120
MyMIDI = MIDIFile(1)
MyMIDI.addTempo(track, time, tempo)
# Add notes
with open('output.mid', 'wb') as f:
    MyMIDI.writeFile(f)"""

    payload = {
        "model": "mistral-large-latest",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        response = requests.post(MISTRAL_API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            code = data['choices'][0]['message']['content']

            # Python 코드만 추출
            if '```python' in code:
                code = code.split('```python')[1].split('```')[0]
            elif '```' in code:
                code = code.split('```')[1].split('```')[0]

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_music/music_{timestamp}.mid"
            code_file = f"generated_music/gen_{timestamp}.py"

            os.makedirs("generated_music", exist_ok=True)

            # 코드 실행하여 MIDI 생성
            code = code.replace('output.mid', filename)

            with open(code_file, "w") as f:
                f.write(code)

            exec(code)

            print(f"✅ MIDI 생성 완료: {filename}")
            print(f"   스타일: {style}")
            return filename
        else:
            print(f"❌ API 오류: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ MIDI 생성 실패: {e}")
        return None

async def auto_generate_music():
    """주기적으로 음악 생성"""
    print("🎵 AI MIDI 생성기 시작!")
    print(f"🔗 모델: Mistral Large")
    print()

    # midiutil 설치 확인
    try:
        from midiutil import MIDIFile
    except ImportError:
        print("⚠️  midiutil 설치 필요: pip install midiutil")
        return

    while True:
        style = random.choice(MUSIC_STYLES)

        print(f"🎵 [{datetime.now().strftime('%H:%M:%S')}] 음악 작곡 중...")
        print(f"   스타일: {style}")

        midi_path = generate_midi_code(style)

        if midi_path:
            print(f"   📁 저장됨: {midi_path}")

        # 2~3분마다 생성
        wait_time = random.randint(120, 180)
        print(f"⏳ {wait_time}초 후 다음 곡...")
        print()
        await asyncio.sleep(wait_time)

async def main():
    """메인 함수"""
    print("=" * 60)
    print("   VTuber AI MIDI 생성기")
    print("=" * 60)
    print()

    await auto_generate_music()

if __name__ == "__main__":
    asyncio.run(main())
