#!/bin/bash

# 완전 자동 24시간 VTuber 방송 시스템
# YouTube 채팅 연동 + 자동 브라우징 + 능동적 발화

echo "🎬 완전 자동 VTuber 방송 시스템 시작"
echo "=========================================="
echo ""

VTUBER_DIR="/home/kim/Open-LLM-VTuber"
cd "$VTUBER_DIR"

# 1. VTuber 서버 확인
echo "1️⃣  VTuber 서버 확인..."
if curl -s http://localhost:12393 > /dev/null; then
    echo "   ✅ 서버 실행 중"
else
    echo "   ⚠️  서버 재시작 중..."
    source $HOME/.local/bin/env
    uv run run_server.py --verbose > server.log 2>&1 &
    sleep 10
fi

# 2. YouTube 채팅 브릿지 시작
echo ""
echo "2️⃣  YouTube 채팅 연동 시작..."
source $HOME/.local/bin/env
python3 youtube_chat_bridge.py > youtube_chat.log 2>&1 &
CHAT_PID=$!
echo "   ✅ YouTube 채팅 모니터링 (PID: $CHAT_PID)"

# 3. 자동 브라우저 시작
echo ""
echo "3️⃣  자동 브라우저 시작..."
python3 auto_browser.py > auto_browser.log 2>&1 &
BROWSER_PID=$!
echo "   ✅ 자동 웹 탐색 (PID: $BROWSER_PID)"

# 4. 상태 출력
echo ""
echo "=========================================="
echo "🎉 모든 시스템 가동!"
echo ""
echo "📺 VTuber 서버: http://localhost:12393"
echo "💬 YouTube 채팅: 실시간 연동 중"
echo "🌐 자동 브라우저: 3~5분마다 활동"
echo ""
echo "📊 로그 확인:"
echo "   - VTuber 서버: tail -f server.log"
echo "   - YouTube 채팅: tail -f youtube_chat.log"
echo "   - 자동 브라우저: tail -f auto_browser.log"
echo ""
echo "🛑 중지: pkill -f 'youtube_chat_bridge\\|auto_browser'"
echo "=========================================="

# 상태 모니터링
echo ""
echo "📡 실시간 모니터링 (Ctrl+C로 종료)..."
tail -f youtube_chat.log auto_browser.log
