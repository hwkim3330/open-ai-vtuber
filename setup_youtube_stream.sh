#!/bin/bash

# YouTube 스트리밍 자동화 스크립트
# Stream Key: YOUR_YOUTUBE_STREAM_KEY (YouTube에서 발급받은 키로 교체)

STREAM_KEY="YOUR_YOUTUBE_STREAM_KEY"
VTUBER_URL="http://localhost:12393"
OBS_CONFIG_DIR="$HOME/.config/obs-studio"

echo "🎥 YouTube 스트리밍 설정 시작..."

# OBS 설정 디렉토리 생성
mkdir -p "$OBS_CONFIG_DIR/basic/scenes"
mkdir -p "$OBS_CONFIG_DIR/basic/profiles/Untitled"

# OBS 프로파일 설정
cat > "$OBS_CONFIG_DIR/basic/profiles/Untitled/basic.ini" << 'EOF'
[General]
Name=Untitled

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
RecType=Standard
RecTracks=1
FLVTrack=1
FFOutputToFile=false
Encoder=obs_x264
RecEncoder=obs_x264
AudioEncoder=ffmpeg_aac
EOF

# OBS 스트리밍 설정
cat > "$OBS_CONFIG_DIR/basic/profiles/Untitled/service.json" << EOF
{
    "type": "rtmp_common",
    "settings": {
        "key": "$STREAM_KEY",
        "server": "rtmp://a.rtmp.youtube.com/live2",
        "service": "YouTube - RTMPS",
        "use_auth": false
    }
}
EOF

# OBS Scene 설정 (Browser Source로 VTuber 추가)
cat > "$OBS_CONFIG_DIR/basic/scenes/Untitled.json" << EOF
{
    "current_scene": "VTuber Scene",
    "scene_order": [
        {"name": "VTuber Scene"}
    ],
    "sources": [
        {
            "name": "VTuber Browser",
            "type": "browser_source",
            "settings": {
                "url": "$VTUBER_URL",
                "width": 1920,
                "height": 1080,
                "fps": 30,
                "shutdown": false,
                "restart_when_active": false
            }
        }
    ],
    "scenes": [
        {
            "name": "VTuber Scene",
            "sources": [
                {
                    "name": "VTuber Browser",
                    "visible": true
                }
            ]
        }
    ]
}
EOF

echo "✅ OBS 설정 완료!"
echo "📺 YouTube 스트림 서버: rtmp://a.rtmp.youtube.com/live2"
echo "🔑 스트림 키: $STREAM_KEY"
echo "🌐 VTuber URL: $VTUBER_URL"
echo ""
echo "이제 OBS Studio를 실행하고 '스트리밍 시작' 버튼을 누르세요!"
