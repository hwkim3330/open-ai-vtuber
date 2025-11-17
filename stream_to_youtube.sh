#!/bin/bash

# YouTube 스트리밍 - ffmpeg 직접 스트리밍 (24시간 자동)
# GUI 없이 백그라운드에서 실행 가능

STREAM_KEY="qawy-zmxr-1w9t-zw8w-9j6r"  # YouTube 스트림 키
YOUTUBE_URL="rtmp://a.rtmp.youtube.com/live2/$STREAM_KEY"
VTUBER_URL="http://localhost:12393"

echo "🎥 YouTube 라이브 스트리밍 시작..."
echo "📺 스트리밍 URL: rtmp://a.rtmp.youtube.com/live2"
echo "🌐 VTuber: $VTUBER_URL"
echo ""
echo "⏸️  중지하려면 Ctrl+C를 누르세요"
echo ""

# 가상 디스플레이 설정 (헤드리스 환경에서 필요)
export DISPLAY=:99

# Xvfb가 실행 중인지 확인
if ! pgrep -x "Xvfb" > /dev/null; then
    echo "🖥️  가상 디스플레이 시작..."
    Xvfb :99 -screen 0 1920x1080x24 &
    sleep 2
fi

# 브라우저로 VTuber 페이지 열기 (백그라운드)
if ! pgrep -x "chromium" > /dev/null && ! pgrep -x "chrome" > /dev/null; then
    echo "🌐 브라우저 시작..."
    chromium-browser --kiosk --no-sandbox --disable-dev-shm-usage --window-size=1920,1080 "$VTUBER_URL" &
    sleep 5
fi

# ffmpeg로 화면 캡처 및 YouTube 스트리밍
echo "📡 스트리밍 시작..."
ffmpeg -f x11grab -video_size 1920x1080 -framerate 30 -i :99.0 \
    -f pulse -i default \
    -c:v libx264 -preset veryfast -maxrate 6000k -bufsize 12000k \
    -pix_fmt yuv420p -g 60 -c:a aac -b:a 192k -ar 44100 \
    -f flv "$YOUTUBE_URL"

echo "✅ 스트리밍 종료"
