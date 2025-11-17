# 🎥 한국어 VTuber YouTube 24시간 스트리밍 가이드

## 📋 설정 완료 항목

✅ **Open-LLM-VTuber 설치 완료**
- 버전: v1.2.1
- 서버 주소: http://localhost:12393

✅ **한국어 설정**
- 캐릭터 이름: 미나 (親근하고 활발한 AI 버튜버)
- TTS: Edge TTS 한국어 (ko-KR-SunHiNeural)
- ASR: SenseVoice (중국어/영어/일본어/한국어/광동어 지원)
- LLM: Mistral AI (mistral-small-latest)

✅ **YouTube 스트리밍 설정**
- 스트림 키: YouTube Studio에서 확인하세요 (설정 → 스트림 키)
- 스트림 서버: rtmp://a.rtmp.youtube.com/live2

## 🚀 사용 방법

### 1. VTuber 서버 실행 (이미 실행 중)
```bash
cd /home/kim/Open-LLM-VTuber
source $HOME/.local/bin/env
uv run run_server.py --verbose
```

### 2. 24시간 자동 스트리밍 시작
```bash
cd /home/kim/Open-LLM-VTuber
./start_24h_stream.sh
```

이 명령어는:
- 가상 디스플레이(Xvfb)를 시작
- Chromium 브라우저로 VTuber 페이지를 전체화면으로 열기
- ffmpeg로 화면을 캡처하여 YouTube로 스트리밍
- 연결이 끊기면 자동으로 재시작 (24시간 무중단)

### 3. 수동 스트리밍 (한 번만 실행)
```bash
cd /home/kim/Open-LLM-VTuber
./stream_to_youtube.sh
```

### 4. OBS Studio 사용 (GUI 선호 시)
```bash
# OBS 설정 자동화
./setup_youtube_stream.sh

# OBS Studio 실행
obs
```

OBS에서:
1. "설정" → "스트림"에서 YouTube가 선택되어 있는지 확인
2. "스트리밍 시작" 버튼 클릭

## 📊 스트리밍 모니터링

### 로그 확인
```bash
tail -f /home/kim/Open-LLM-VTuber/streaming.log
```

### 서버 상태 확인
```bash
# VTuber 서버 확인
curl http://localhost:12393

# 프로세스 확인
ps aux | grep -E "ffmpeg|chromium|Xvfb"
```

### YouTube Studio에서 확인
https://studio.youtube.com/channel/UC.../livestreaming

## ⚙️ 설정 변경

### 캐릭터 성격 변경
`/home/kim/Open-LLM-VTuber/conf.yaml` 파일의 `persona_prompt` 수정

### TTS 목소리 변경
한국어 목소리 옵션:
- `ko-KR-SunHiNeural` (여성, 현재 설정)
- `ko-KR-InJoonNeural` (남성)
- `ko-KR-BongJinNeural` (남성)
- `ko-KR-GookMinNeural` (남성)
- `ko-KR-YuJinNeural` (여성)

`conf.yaml`에서 `edge_tts.voice` 값 변경 후 서버 재시작

### 스트리밍 품질 변경
`stream_to_youtube.sh`에서 ffmpeg 설정 수정:
- `-maxrate`: 비트레이트 (기본 6000k)
- `-framerate`: 프레임레이트 (기본 30)
- `-video_size`: 해상도 (기본 1920x1080)

## 🛠️ 문제 해결

### 서버가 응답하지 않음
```bash
# 프로세스 확인 및 재시작
pkill -f run_server.py
cd /home/kim/Open-LLM-VTuber
source $HOME/.local/bin/env
uv run run_server.py --verbose &
```

### 스트리밍이 연결되지 않음
```bash
# ffmpeg 프로세스 종료
pkill -f ffmpeg

# 다시 시작
./stream_to_youtube.sh
```

### 화면이 검은색
```bash
# Xvfb 재시작
pkill Xvfb
Xvfb :99 -screen 0 1920x1080x24 &
sleep 2

# Chromium 재시작
pkill chromium
DISPLAY=:99 chromium-browser --kiosk --no-sandbox --window-size=1920,1080 http://localhost:12393 &
```

## 📝 주제 아이디어

사용자가 "주제 알아서 맘대로"라고 했으므로, AI가 자동으로 다양한 주제로 대화할 수 있습니다:

- 오늘의 날씨와 뉴스
- 재미있는 사실과 트리비아
- 기술과 프로그래밍 이야기
- 일상 대화와 시청자 질문 답변
- 음악 추천과 감상
- 게임 이야기
- 요리 레시피와 음식 이야기

## 🔧 고급 설정

### Mistral AI API 키 변경
`conf.yaml`에서 `mistral_llm.llm_api_key` 값 변경

### 웹캠 사용
VTuber 웹 인터페이스에서 카메라 권한 허용 시 웹캠으로 표정 추적 가능

### MCP 도구 사용
`conf.yaml`에서 `mcp_enabled_servers`에 도구 추가:
- `"time"`: 시간 조회
- `"ddg-search"`: DuckDuckGo 검색

## 📞 지원

문제가 발생하면:
1. `streaming.log` 로그 파일 확인
2. GitHub Issues: https://github.com/Open-LLM-VTuber/Open-LLM-VTuber/issues
3. Discord: https://discord.gg/3UDA8YFDXx

---

**생성일**: 2025-11-17
**설정자**: Claude Code
