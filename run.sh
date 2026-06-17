#!/usr/bin/env bash

CONFIG_PATH=/data/options.json

FREQ=$(jq -r '.frequency' "$CONFIG_PATH")
EVENT_TYPE=$(jq -r '.event_type' "$CONFIG_PATH")

echo "Starting SAME/EAS RTL-SDR"
echo "Frequency: $FREQ"
echo "HA event type: $EVENT_TYPE"

rtl_fm -f "$FREQ" -M fm -s 22050 | multimon-ng -a EAS -t raw - | python3 /same_eas.py "$EVENT_TYPE"
