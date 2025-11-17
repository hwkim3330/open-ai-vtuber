# 🎤 Open-LLM-VTuber - 미나의 24시간 라이브 스트림

자율적인 한국어 AI VTuber 시스템 - 혼자서 방송하고, 그림 그리고, 날씨도 알려줍니다!

## ✨ 주요 기능

### 🗣️ 완전 자율 방송
- **10초마다 자동 발화**: 시청자가 없어도 혼자 활발하게 방송 진행
- **자연스러운 한국어**: ko-KR-SunHiNeural (여성 음성) 사용
- **능동적인 성격**: 스스로 주제를 찾고 이야기 시작

### 🌐 자동 웹 서핑
- **30~60초 주기**: 자동으로 웹사이트 탐색
- **다양한 주제**: 뉴스, 기술, GitHub 트렌드, 날씨 등
- **실시간 정보 공유**: 찾은 정보를 시청자에게 자연스럽게 전달

### 🎨 AI 그림 생성
- **1~2분마다**: Mistral AI로 SVG 그림 생성
- **빛나는 효과**: 모델 위에 글로우 쉐이더 오버레이
- **[SVG:주제] 패턴**: VTuber가 말하면 자동으로 그림 표시
- **즉시 생성**: API 방식으로 빠른 렌더링

### 🌤️ 날씨 기상캐스터
- **30분마다**: 판교 지역 실시간 날씨 방송
- **Open-Meteo API**: 무료, API 키 불필요
- **한국어 설명**: 온도, 습도, 풍속, 날씨 상태

### 📺 YouTube 라이브 스트리밍
- **24시간 무중단**: 자동 재시작 메커니즘
- **실제 브라우저 캡처**: 권한 문제 해결
- **고품질**: 1080p, 6Mbps 스트리밍

## 🚀 빠른 시작

### 1. 완전 통합 시스템 실행

모든 기능을 한 번에 시작:

```bash
cd /home/kim/Open-LLM-VTuber
./start_complete_system.sh
```

이 스크립트는 자동으로 실행합니다:
- ✅ VTuber 서버 (localhost:12393)
- ✅ 자동 브라우저 (30-60초 주기)
- ✅ AI SVG 생성기 (1-2분 주기)
- ✅ 날씨 서비스 (30분 주기)
- ✅ Ultra UI (빛나는 오버레이)
- ⚠️ YouTube 스트리밍 (선택 사항)

### 2. 개별 서비스 실행

필요한 서비스만 실행하려면:

```bash
# VTuber 서버만
source $HOME/.local/bin/env && uv run run_server.py --verbose

# 자동 브라우저만
python3 auto_browser.py

# AI SVG 생성기만
python3 ai_svg_creator.py

# 날씨 서비스만
python3 weather_service.py

# Ultra UI 열기
google-chrome --new-window --app="file:///home/kim/Open-LLM-VTuber/vtuber_ultra.html"
```

### 3. YouTube 스트리밍 설정

스트림 키를 업데이트하세요:

```bash
# start_complete_system.sh 또는 streaming 스크립트에서
STREAM_KEY="your-stream-key-here"
```

## 🎮 주요 파일 설명

### 핵심 설정
- **conf.yaml**: VTuber 메인 설정 파일
  - Mistral AI API 키: `bN77wfiqQRd7EYrUdDA4PN9T5p4fTKht`
  - 음성: `ko-KR-SunHiNeural` (여성)
  - 주기적 발화 활성화
  - 기상캐스터 역할 포함

### 서비스 스크립트
- **start_complete_system.sh**: 완전 통합 시스템 시작 스크립트
- **auto_browser.py**: 자율 웹 서핑 시스템
- **ai_svg_creator.py**: Mistral AI SVG 생성기
- **weather_service.py**: 판교 날씨 서비스

### UI 파일
- **vtuber_ultra.html**: 완전한 UI (빛나는 SVG 오버레이)
- **vtuber_complete.html**: 이전 버전 UI (활동 피드 포함)

## 🎨 SVG 그림 그리기

VTuber가 응답에 `[SVG:주제]` 형식을 포함하면 자동으로 그림이 생성됩니다:

```
"귀여운 고양이를 그려볼게요! [SVG:cute cat]"
"별이 빛나는 밤하늘이에요 [SVG:starry night sky]"
```

생성된 SVG는:
- 모델 위에 오버레이로 표시
- 빛나는 글로우 효과 적용
- 떠다니는 애니메이션
- 15초 후 자동 페이드아웃

## 🌐 웹서핑 주제

자동 브라우저가 탐색하는 사이트:
- 📰 Google 뉴스 (한국어)
- 💻 GitHub 트렌딩
- 🌦️ 날씨 정보
- 🤖 AI/ML 최신 소식
- 🎮 게임 뉴스
- 📱 기술 뉴스

## 🛠️ 의존성

### Python 패키지
```bash
pip3 install --break-system-packages \
    requests \
    websockets \
    pytchat \
    midiutil
```

### 시스템 패키지
```bash
sudo apt install -y \
    fonts-nanum \
    fonts-nanum-coding \
    fonts-nanum-extra \
    obs-studio \
    ffmpeg \
    pulseaudio \
    chromium-browser
```

### uv 패키지 관리자
프로젝트는 `uv`를 사용합니다:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
```

## 📊 시스템 모니터링

### 로그 확인
```bash
# 모든 서비스 로그 실시간 모니터링
tail -f server_complete.log auto_browser_complete.log svg_creator_complete.log weather_complete.log

# 개별 로그
tail -f server_complete.log      # VTuber 서버
tail -f auto_browser_complete.log # 자동 브라우저
tail -f svg_creator_complete.log  # SVG 생성기
tail -f weather_complete.log      # 날씨 서비스
tail -f streaming_complete.log    # YouTube 스트리밍
```

### 프로세스 확인
```bash
# 실행 중인 서비스 확인
ps aux | grep -E "(run_server|auto_browser|svg_creator|weather_service)" | grep -v grep

# 포트 사용 확인
lsof -i :12393  # VTuber 서버
```

## 🛑 시스템 중지

모든 서비스 중지:
```bash
pkill -f 'run_server|auto_browser|svg_creator|weather_service|ffmpeg'
```

개별 서비스 중지:
```bash
pkill -f run_server        # VTuber 서버만
pkill -f auto_browser      # 자동 브라우저만
pkill -f svg_creator       # SVG 생성기만
pkill -f weather_service   # 날씨 서비스만
pkill -f 'ffmpeg.*youtube' # 스트리밍만
```

## 🔧 문제 해결

### 스트리밍이 작동하지 않음
1. 새 스트림 키 확인
2. YouTube Studio에서 스트림 상태 확인
3. ffmpeg 로그 확인: `tail -f streaming_complete.log`

### 브라우저 권한 문제
- 실제 브라우저 사용 (가상 디스플레이 아님)
- 마이크/카메라 권한은 UI에서 수동으로 부여

### 날씨 서비스 작동 안 함
```bash
# 수동으로 테스트
python3 -c "from weather_service import get_weather; print(get_weather())"

# WebSocket 연결 확인
curl http://localhost:12393
```

### VTuber가 말을 안 함
1. `conf.yaml`에서 `proactive_speak_prompt` 활성화 확인
2. UI에서 10초 간격 설정 확인
3. 서버 로그에서 오류 확인

## 📝 설정 커스터마이징

### 발화 간격 변경
`conf.yaml`의 persona_prompt에서:
```yaml
행동 지침:
  - 주기적으로 스스로 말을 시작하세요 (10초마다 능동적으로)  # <- 여기 수정
```

### 음성 변경
```yaml
edge_tts:
  voice: 'ko-KR-SunHiNeural'  # 다른 음성으로 변경
```

사용 가능한 음성 목록:
```bash
edge-tts --list-voices | grep ko-KR
```

### 날씨 위치 변경
`weather_service.py`에서:
```python
PANGYO_LAT = 37.3945  # 위도
PANGYO_LON = 127.1110  # 경도
```

### 브라우징 주기 변경
`auto_browser.py`에서:
```python
wait_time = random.randint(30, 60)  # 30~60초
```

## 🌟 특별 기능

### Think Tag (생각 표시)
VTuber가 생각을 괄호로 표시:
```
(오늘은 날씨가 좋네요) 안녕하세요 여러분!
```

### Live2D 표정 제어
시스템이 자동으로 감정에 맞는 표정 변경

### MCP 도구 통합
Model Context Protocol로 다양한 도구 사용 가능

## 📂 프로젝트 구조

```
Open-LLM-VTuber/
├── conf.yaml                    # 메인 설정 파일
├── start_complete_system.sh     # 완전 통합 시작 스크립트
├── auto_browser.py              # 자율 웹 서핑
├── ai_svg_creator.py            # SVG 생성기
├── weather_service.py           # 날씨 서비스
├── vtuber_ultra.html           # Ultra UI
├── vtuber_complete.html        # Complete UI
├── run_server.py               # VTuber 서버
├── src/                        # 소스 코드
├── live2d-models/              # Live2D 모델
├── characters/                 # 캐릭터 설정
└── cache/                      # 캐시 파일
```

## 🔗 유용한 링크

- **VTuber 서버**: http://localhost:12393
- **Ultra UI**: file:///home/kim/Open-LLM-VTuber/vtuber_ultra.html
- **GitHub 저장소**: https://github.com/hwkim3330/open-ai-vtuber
- **원본 프로젝트**: https://github.com/t41372/Open-LLM-VTuber

## 🎯 사용 팁

1. **첫 실행**: `start_complete_system.sh`로 모든 기능 테스트
2. **안정적인 운영**: 개별 서비스를 systemd로 관리
3. **커스터마이징**: `conf.yaml`에서 페르소나와 행동 수정
4. **모니터링**: tmux/screen으로 로그 실시간 확인
5. **스트리밍**: 테스트 후 24시간 자동 재시작 설정

## ⚙️ 고급 설정

### systemd 서비스 설정
24시간 무중단 운영을 위해 systemd 서비스로 등록:

```bash
sudo nano /etc/systemd/system/vtuber.service
```

### Docker 컨테이너
격리된 환경에서 실행:
```bash
# TODO: Dockerfile 추가 예정
```

### 성능 최적화
- GPU 가속 활성화
- 낮은 지연시간을 위한 네트워크 설정
- 메모리 사용량 모니터링

## 📜 라이선스

Open-LLM-VTuber 프로젝트의 라이선스를 따릅니다.

## 🙏 감사의 말

- Open-LLM-VTuber 프로젝트
- Mistral AI
- Edge TTS
- Open-Meteo API

---

**즐거운 방송 되세요! 🎉**
