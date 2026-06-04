#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python "$SCRIPT_DIR/generate_volcengine_image.py" \
  --prompt "A cinematic scene of a young boy standing at a window, looking out at the rainy landscape outside. The camera is behind the boy, showing his back and shoulders as he gazes through the window. Outside, rain is falling steadily, creating droplets on the windowpane. The scene is melancholic and contemplative, with soft natural lighting from the overcast sky. The boy is about 8 years old, wearing a simple shirt. The window frames a view of a wet street or garden with trees and distant buildings. The overall mood is peaceful yet slightly somber, capturing a quiet moment of reflection. Cinematic composition, depth of field, beautiful atmospheric lighting with blue-gray tones." \
  --output-file "<workspace-dir>/outputs/reference_boy_window_rain.jpg" \
  --size 2K