# 🎤 한국어 VTuber 24시간 자동 방송 시스템

Open-LLM-VTuber를 기반으로 한 한국어 AI 버튜버 자동 방송 시스템입니다.

## ✨ 주요 기능

- 🗣️ **한국어 TTS/ASR**: Edge TTS (HyunsuNeural) + SenseVoice
- 🤖 **Mistral AI 연동**: 자연스러운 한국어 대화
- 📺 **YouTube 24시간 스트리밍**: ffmpeg 자동 스트리밍
- 💬 **YouTube 채팅 연동**: 실시간 채팅 읽기 및 응답
- 🌐 **자동 브라우징**: 능동적 웹 서핑 및 정보 탐색
- 🎨 **Live2D 아바타**: 실시간 캐릭터 애니메이션

## 🚀 빠른 시작

### 1. 저장소 복제
```bash
git clone https://github.com/hwkim3330/open-ai-vtuber.git
cd open-ai-vtuber
```

### 2. 의존성 설치
```bash
# uv 패키지 매니저 설치 (없는 경우)
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# 프로젝트 의존성 설치
uv sync

# 추가 패키지 설치
pip install pytchat websockets
```

### 3. 설정 파일 생성
```bash
# 기본 설정 파일 복사
cp config_templates/conf.default.yaml conf.yaml
```

**conf.yaml에서 다음 항목을 수정하세요:**

```yaml
# 캐릭터 설정
character_config:
  character_name: '미나'  # 원하는 이름으로 변경
  human_name: '사용자'

  # 한국어 TTS (Edge TTS)
  edge_tts:
    voice: 'ko-KR-HyunsuNeural'  # 또는 'ko-KR-SunHiNeural'

  # Mistral AI 설정
  agent_config:
    agent_settings:
      basic_memory_agent:
        llm_provider: 'mistral_llm'

  # LLM 설정
  llm_config:
    mistral_llm:
      llm_api_key: 'YOUR_MISTRAL_API_KEY'  # Mistral AI API 키
      model: 'mistral-large-latest'
      temperature: 1.0
```

### 4. YouTube 스트리밍 설정

**스크립트 파일에서 스트림 키 입력:**

```bash
# stream_to_youtube.sh
STREAM_KEY="YOUR_YOUTUBE_STREAM_KEY"

# start_gui_stream.sh
STREAM_KEY="YOUR_YOUTUBE_STREAM_KEY"

# youtube_chat_bridge.py
YOUTUBE_VIDEO_ID = "YOUR_VIDEO_ID"
```

### 5. 시스템 실행

#### 전체 자동 시스템
```bash
./start_full_auto.sh
```

이 명령어는 다음을 자동으로 실행합니다:
- VTuber 서버 (http://localhost:12393)
- YouTube 채팅 모니터링
- 자동 브라우저 (3~5분마다 활동)

#### 24시간 스트리밍
```bash
./start_24h_stream.sh
```

## 📋 시스템 요구사항

### 필수 패키지
```bash
sudo apt install -y \
    ffmpeg \
    xvfb \
    chromium-browser \
    pulseaudio \
    fonts-nanum \
    fonts-nanum-coding \
    fonts-nanum-extra
```

### 선택 (GUI 사용 시)
```bash
sudo apt install -y obs-studio
```

## 🔧 주요 구성 요소

### 1. VTuber 서버
- **위치**: `run_server.py`
- **포트**: 12393
- **기능**: Live2D 렌더링, 음성 처리, WebSocket 통신

### 2. YouTube 채팅 브릿지
- **파일**: `youtube_chat_bridge.py`
- **기능**: YouTube 라이브 채팅 읽기 및 VTuber 전달
- **라이브러리**: pytchat

### 3. 자동 브라우저
- **파일**: `auto_browser.py`
- **기능**: 주기적 웹 서핑 및 능동적 발화
- **주기**: 3~5분마다

### 4. 스트리밍 스크립트
- **stream_to_youtube.sh**: ffmpeg 직접 스트리밍
- **start_24h_stream.sh**: 24시간 자동 재시작
- **start_gui_stream.sh**: OBS Studio GUI 버전

## 📁 주요 파일 구조

```
open-ai-vtuber/
├── conf.yaml                    # 메인 설정 파일 (gitignore)
├── run_server.py                # VTuber 서버
├── youtube_chat_bridge.py       # YouTube 채팅 연동
├── auto_browser.py              # 자동 브라우징
├── start_full_auto.sh           # 완전 자동 시스템
├── start_24h_stream.sh          # 24시간 스트리밍
├── stream_to_youtube.sh         # ffmpeg 스트리밍
├── start_gui_stream.sh          # OBS GUI 스트리밍
├── STREAMING_GUIDE.md           # 스트리밍 가이드
└── characters/                  # 캐릭터 설정 파일들
```

## ⚙️ 설정 커스터마이징

### 페르소나 프롬프트 수정
`conf.yaml`에서 `persona_prompt`를 원하는 성격으로 변경:

```yaml
persona_prompt: |
  당신은 능동적이고 호기심 많은 한국어 AI 버튜버 미나입니다.

  성격:
  - 자연스럽고 친근한 말투로 대화합니다
  - 시청자가 없어도 혼자서 활발하게 방송을 진행합니다
  - 웹 서핑, 뉴스 검색, 정보 탐색을 즐깁니다
```

### 브라우징 사이트 추가
`auto_browser.py`에서 `INTERESTING_SITES` 리스트 수정

### YouTube 비디오 ID 변경
`youtube_chat_bridge.py`에서 `YOUTUBE_VIDEO_ID` 수정

## 🎯 사용 팁

1. **API 키 관리**: 절대로 conf.yaml을 공개 저장소에 커밋하지 마세요
2. **메모리 관리**: 장시간 운영 시 주기적으로 재시작 권장
3. **로그 확인**: `tail -f server.log youtube_chat.log auto_browser.log`
4. **중지**: `pkill -f 'youtube_chat_bridge|auto_browser'`

## 🛠️ 문제 해결

### VTuber 서버가 시작되지 않을 때
```bash
source $HOME/.local/bin/env
uv run run_server.py --verbose
```

### YouTube 스트리밍 오류
- 스트림 키 확인: YouTube Studio → 설정 → 스트림 키
- ffmpeg 설치 확인: `ffmpeg -version`
- 네트워크 연결 확인

### 한국어 TTS 안 나올 때
`conf.yaml`에서 `edge_tts.voice` 확인:
- `ko-KR-HyunsuNeural` (남성, 추천)
- `ko-KR-SunHiNeural` (여성)

## 📝 라이선스

이 프로젝트는 Open-LLM-VTuber를 기반으로 하며, 동일한 라이선스를 따릅니다.

## 🙏 크레딧

- [Open-LLM-VTuber](https://github.com/t41372/Open-LLM-VTuber) - 기반 프로젝트
- [pytchat](https://github.com/taizan-hokuto/pytchat) - YouTube 채팅 라이브러리
- Mistral AI - LLM 제공
- Edge TTS - 한국어 음성 합성

## 📞 문의 및 기여

이슈 및 PR은 언제든 환영합니다!

---

**⚠️ 주의**: API 키와 스트림 키는 절대로 공개하지 마세요!
