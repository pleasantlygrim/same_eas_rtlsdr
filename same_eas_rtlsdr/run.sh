#!/usr/bin/env bash

CONFIG_PATH=/data/options.json

FREQ=$(jq -r '.frequency' "$CONFIG_PATH")
EVENT_TYPE=$(jq -r '.event_type' "$CONFIG_PATH")
AUDIO_STREAM=$(jq -r '.audio_stream' "$CONFIG_PATH")
AUDIO_PORT=$(jq -r '.audio_port' "$CONFIG_PATH")

echo "Starting SAME/EAS RTL-SDR"
echo "Frequency: $FREQ"
echo "HA event type: $EVENT_TYPE"
echo "Audio stream: $AUDIO_STREAM"
echo "Audio port: $AUDIO_PORT"

if [ "$AUDIO_STREAM" = "true" ]; then
  echo "Starting web UI on port 8080"
  python3 /web.py &

  echo "Starting with audio stream enabled"

  rtl_fm -f "$FREQ" -M fm -s 22050 | tee \
    >(multimon-ng -a EAS -t raw - | python3 /same_eas.py "$EVENT_TYPE") \
    >(sox -t raw -r 22050 -e signed-integer -b 16 -c 1 - -t mp3 - > /tmp/noaa_stream.mp3)
else
  echo "Starting without audio stream"

  rtl_fm -f "$FREQ" -M fm -s 22050 | multimon-ng -a EAS -t raw - | python3 /same_eas.py "$EVENT_TYPE"
fi
