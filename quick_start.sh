#!/bin/bash

# 빠른 시작 스크립트 - 모든 설치가 완료되면 자동으로 스트리밍 시작

echo "⏳ 패키지 설치 완료 대기 중..."

# apt 프로세스가 완료될 때까지 대기
while pgrep -x "apt" > /dev/null || pgrep -x "apt-get" > /dev/null; do
    echo "   설치 진행 중... ($(date +%H:%M:%S))"
    sleep 5
done

echo "✅ 모든 패키지 설치 완료!"
sleep 2

# Xvfb 확인 및 설치
if ! command -v Xvfb &> /dev/null; then
    echo "📦 Xvfb 설치 중..."
    echo "1" | sudo -S apt install -y xvfb
fi

echo "🎥 YouTube 24시간 스트리밍 시작!"
echo ""
echo "📺 YouTube Studio: https://studio.youtube.com"
echo "🌐 VTuber: http://localhost:12393"
echo "🔑 스트림 키: YOUR_YOUTUBE_STREAM_KEY (YouTube Studio에서 확인)"
echo ""

# 24시간 스트리밍 시작
/home/kim/Open-LLM-VTuber/start_24h_stream.sh
