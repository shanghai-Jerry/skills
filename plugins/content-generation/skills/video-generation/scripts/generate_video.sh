#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python "$SCRIPT_DIR/generate_volcengine_video.py" \
  --prompt "A young boy stands at a window, looking out at the rainy landscape. The camera is positioned behind the boy, showing his back and shoulders as he gazes through the window. Outside, rain falls steadily, creating droplets on the windowpane that slowly trickle down. The scene is melancholic and contemplative. The boy remains still, lost in thought as he watches the rain. The lighting is soft and natural from the overcast sky. Slow, subtle camera movement - a gentle push-in towards the boy and window. Atmospheric, cinematic shot with depth of field focusing on the raindrops on the window. The mood is peaceful yet slightly somber, capturing a quiet moment of childhood reflection." \
  --reference-images "<workspace-dir>/outputs/reference_boy_window_rain.jpg" \
  --output-file "<workspace-dir>/outputs/boy_window_rain_video.mp4" \
  --duration 5 \
  --ratio 16:9