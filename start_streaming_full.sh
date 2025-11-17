#!/bin/bash

# 완전 통합 VTuber 스트리밍 시스템
# VTuber 서버 + YouTube 채팅 + 자동 브라우저 + YouTube 스트리밍

echo "🎬 완전 통합 VTuber 스트리밍 시스템 시작"
echo "==========================================="
echo ""

VTUBER_DIR="/home/kim/Open-LLM-VTuber"
cd "$VTUBER_DIR"

# 설정
STREAM_KEY="qawy-zmxr-1w9t-zw8w-9j6r"
YOUTUBE_URL="rtmp://a.rtmp.youtube.com/live2/$STREAM_KEY"
VTUBER_URL="http://localhost:12393"
DISPLAY_NUM=":99"

# 1. VTuber 서버 확인
echo "1️⃣  VTuber 서버 확인..."
if curl -s http://localhost:12393 > /dev/null; then
    echo "   ✅ 서버 실행 중"
else
    echo "   ⚠️  서버 시작 중..."
    source $HOME/.local/bin/env
    uv run run_server.py --verbose > server.log 2>&1 &
    sleep 10
fi

# 2. 자동 브라우저 시작
echo ""
echo "2️⃣  자동 브라우저 시작..."
if pgrep -f "auto_browser.py" > /dev/null; then
    echo "   ✅ 이미 실행 중"
else
    python3 auto_browser.py > auto_browser.log 2>&1 &
    echo "   ✅ 자동 웹 탐색 시작 (PID: $!)"
fi

# 3. 가상 디스플레이 설정
echo ""
echo "3️⃣  가상 디스플레이 설정..."
export DISPLAY=$DISPLAY_NUM

if ! pgrep -x "Xvfb" > /dev/null; then
    echo "   🖥️  가상 디스플레이 시작..."
    Xvfb $DISPLAY_NUM -screen 0 1920x1080x24 &
    sleep 3
else
    echo "   ✅ 가상 디스플레이 실행 중"
fi

# 4. 브라우저로 VTuber 페이지 열기
echo ""
echo "4️⃣  VTuber 페이지 열기..."
if pgrep -f "chromium.*$VTUBER_URL" > /dev/null || pgrep -f "chrome.*$VTUBER_URL" > /dev/null; then
    echo "   ✅ 브라우저 이미 실행 중"
else
    echo "   🌐 브라우저 시작..."
    chromium-browser --kiosk --no-sandbox --disable-dev-shm-usage \
        --window-size=1920,1080 --disable-gpu \
        "$VTUBER_URL" > /dev/null 2>&1 &
    sleep 7
    echo "   ✅ VTuber 페이지 로드 완료"
fi

# 5. YouTube 스트리밍 시작
echo ""
echo "5️⃣  YouTube 스트리밍 시작..."
echo "   📡 RTMP 서버: rtmp://a.rtmp.youtube.com/live2"
echo "   🎥 해상도: 1920x1080 @ 30fps"
echo "   🔊 오디오: AAC 192kbps"
echo ""
echo "   ⏸️  중지: Ctrl+C"
echo ""
echo "==========================================="
echo ""

# ffmpeg로 화면 캡처 및 스트리밍
ffmpeg -f x11grab -video_size 1920x1080 -framerate 30 -i $DISPLAY_NUM \
    -f pulse -i default \
    -c:v libx264 -preset veryfast -maxrate 6000k -bufsize 12000k \
    -pix_fmt yuv420p -g 60 \
    -c:a aac -b:a 192k -ar 44100 \
    -f flv "$YOUTUBE_URL" 2>&1 | tee streaming.log

echo ""
echo "✅ 스트리밍 종료"
