#!/bin/bash

# 24시간 자동 재시작 스트리밍 스크립트
# 스트리밍이 끊기면 자동으로 재시작합니다.

STREAM_SCRIPT="/home/kim/Open-LLM-VTuber/stream_to_youtube.sh"
LOG_FILE="/home/kim/Open-LLM-VTuber/streaming.log"

echo "🔄 24시간 자동 스트리밍 시작..."
echo "📝 로그: $LOG_FILE"
echo ""

# 무한 루프로 스트리밍 유지
while true; do
    echo "$(date): 스트리밍 시작" >> "$LOG_FILE"

    # 스트리밍 실행
    bash "$STREAM_SCRIPT" 2>&1 | tee -a "$LOG_FILE"

    # 스트리밍이 종료되면 5초 후 재시작
    echo "$(date): 스트리밍 중단됨. 5초 후 재시작..." >> "$LOG_FILE"
    sleep 5
done
