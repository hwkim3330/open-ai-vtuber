#!/bin/bash

# GUI 버전 - 바로 시작하기
# 가상 디스플레이 없이 실제 화면에서 실행

echo "🎥 한국어 VTuber YouTube 스트리밍 - GUI 버전"
echo ""
echo "1️⃣  브라우저로 VTuber 열기"
echo "2️⃣  OBS Studio로 화면 캡처"
echo "3️⃣  YouTube 스트리밍 시작"
echo ""

VTUBER_URL="http://localhost:12393"
STREAM_KEY="YOUR_YOUTUBE_STREAM_KEY"  # YouTube 스트림 키를 여기에 입력하세요

# 1. 브라우저로 VTuber 페이지 열기
echo "🌐 브라우저 열기..."
if command -v google-chrome &> /dev/null; then
    google-chrome --new-window --app="$VTUBER_URL" &
elif command -v chromium-browser &> /dev/null; then
    chromium-browser --new-window --app="$VTUBER_URL" &
elif command -v firefox &> /dev/null; then
    firefox --new-window "$VTUBER_URL" &
else
    xdg-open "$VTUBER_URL" &
fi

sleep 3

# 2. OBS Studio 설정
echo ""
echo "⚙️  OBS Studio 설정 중..."

# OBS 설정 디렉토리
OBS_CONFIG_DIR="$HOME/.config/obs-studio"
mkdir -p "$OBS_CONFIG_DIR/basic/profiles/Streaming"

# 간단한 OBS 프로파일 생성
cat > "$OBS_CONFIG_DIR/basic/profiles/Streaming/basic.ini" << 'EOF'
[General]
Name=Streaming

[Video]
BaseCX=1920
BaseCY=1080
OutputCX=1920
OutputCY=1080
FPSType=0
FPSCommon=30

[Output]
Mode=Advanced

[AdvOut]
Encoder=obs_x264
RecEncoder=obs_x264
EOF

# YouTube 스트림 설정
cat > "$OBS_CONFIG_DIR/basic/profiles/Streaming/service.json" << EOF
{
    "type": "rtmp_common",
    "settings": {
        "key": "$STREAM_KEY",
        "server": "rtmp://a.rtmp.youtube.com/live2",
        "service": "YouTube - RTMPS"
    }
}
EOF

echo "✅ OBS 설정 완료!"
echo ""
echo "📋 다음 단계:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. OBS Studio 실행:"
echo "   obs"
echo ""
echo "2. OBS에서 설정:"
echo "   - '소스' 추가 → '창 캡처' 또는 '화면 캡처'"
echo "   - 브라우저 창 선택"
echo ""
echo "3. '스트리밍 시작' 클릭!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 VTuber: $VTUBER_URL"
echo "🔑 스트림 키: $STREAM_KEY"
echo "📺 YouTube Studio: https://studio.youtube.com"
echo ""

# OBS 실행
if command -v obs &> /dev/null; then
    echo "🎬 OBS Studio 실행 중..."
    obs &
else
    echo "⚠️  OBS Studio가 아직 설치되지 않았습니다."
    echo "   설치 명령어: sudo apt install obs-studio"
fi
