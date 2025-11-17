#!/bin/bash

# 완전 통합 VTuber 시스템
# 모든 기능을 하나의 스크립트로 실행

echo "🚀 VTuber 완전 통합 시스템 시작"
echo "========================================="
echo ""

VTUBER_DIR="/home/kim/Open-LLM-VTuber"
cd "$VTUBER_DIR"

# 기존 프로세스 정리
echo "🧹 기존 프로세스 정리..."
pkill -f "run_server|auto_browser|svg_creator|weather_service|ffmpeg.*youtube" 2>/dev/null
sleep 2

# 1. VTuber 서버 시작
echo ""
echo "1️⃣  VTuber 서버 시작..."
source $HOME/.local/bin/env
uv run run_server.py --verbose > server_complete.log 2>&1 &
SERVER_PID=$!
echo "   ✅ VTuber 서버 (PID: $SERVER_PID)"
sleep 8

# 2. 자동 브라우저 시작
echo ""
echo "2️⃣  자동 브라우저 시작..."
python3 auto_browser.py > auto_browser_complete.log 2>&1 &
BROWSER_PID=$!
echo "   ✅ 자동 브라우저 (PID: $BROWSER_PID)"

# 3. AI SVG 생성기 시작
echo ""
echo "3️⃣  AI SVG 생성기 시작..."
python3 ai_svg_creator.py > svg_creator_complete.log 2>&1 &
SVG_PID=$!
echo "   ✅ AI SVG 생성기 (PID: $SVG_PID)"

# 4. 판교 날씨 서비스 시작
echo ""
echo "4️⃣  판교 날씨 서비스 시작..."
python3 weather_service.py > weather_complete.log 2>&1 &
WEATHER_PID=$!
echo "   ✅ 날씨 서비스 (PID: $WEATHER_PID)"

# 5. Ultra UI 열기 (실제 브라우저)
echo ""
echo "5️⃣  Ultra VTuber UI 열기..."
google-chrome --new-window --app="file://$VTUBER_DIR/vtuber_ultra.html" > /dev/null 2>&1 &
echo "   ✅ Ultra UI 실행 (빛나는 SVG 오버레이)"

# 6. YouTube 스트리밍 시작 (선택사항)
echo ""
read -p "YouTube 스트리밍 시작할까요? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "6️⃣  YouTube 스트리밍 시작..."
    echo "   ⚠️  스트림 키를 업데이트하세요!"
    echo ""

    STREAM_KEY="qawy-zmxr-1w9t-zw8w-9j6r"
    YOUTUBE_URL="rtmp://a.rtmp.youtube.com/live2/$STREAM_KEY"

    # 현재 실제 디스플레이 사용
    CURRENT_DISPLAY=$(echo $DISPLAY)

    # 화면 캡처 (실제 브라우저 창)
    ffmpeg -f x11grab -video_size 1920x1080 -framerate 30 -i $CURRENT_DISPLAY \
        -f pulse -i default \
        -c:v libx264 -preset veryfast -maxrate 6000k -bufsize 12000k \
        -pix_fmt yuv420p -g 60 \
        -c:a aac -b:a 192k -ar 44100 \
        -f flv "$YOUTUBE_URL" > streaming_complete.log 2>&1 &
    STREAM_PID=$!
    echo "   ✅ YouTube 스트리밍 (PID: $STREAM_PID)"
    echo "   📺 실제 브라우저 창을 캡처합니다"
fi

# 완료
echo ""
echo "========================================="
echo "🎉 완전 통합 시스템 가동 완료!"
echo ""
echo "📊 실행 중인 서비스:"
echo "   • VTuber 서버: PID $SERVER_PID"
echo "   • 자동 브라우저: PID $BROWSER_PID"
echo "   • AI SVG 생성: PID $SVG_PID"
echo "   • 날씨 서비스: PID $WEATHER_PID"
if [ ! -z "$STREAM_PID" ]; then
echo "   • YouTube 스트리밍: PID $STREAM_PID"
fi
echo ""
echo "🌐 Ultra UI: file://$VTUBER_DIR/vtuber_ultra.html"
echo "📺 VTuber 서버: http://localhost:12393"
echo ""
echo "📋 기능:"
echo "   ✅ 10초마다 자동 발화"
echo "   ✅ 30~60초 주기 자동 브라우징"
echo "   ✅ 1~2분마다 AI SVG 생성"
echo "   ✅ 30분마다 판교 날씨 방송"
echo "   ✅ 모델 위에 빛나는 SVG 오버레이"
echo "   ✅ 실시간 브라우저 UI (권한 문제 해결)"
echo ""
echo "🛑 중지: pkill -f 'run_server|auto_browser|svg_creator|weather_service|ffmpeg'"
echo "========================================="
echo ""

# 로그 모니터링
echo "📡 로그 모니터링 (Ctrl+C로 종료)..."
tail -f server_complete.log auto_browser_complete.log svg_creator_complete.log weather_complete.log
