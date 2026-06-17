import sys
import json
import time
import os
import urllib.request

event_type = sys.argv[1]

ha_url = "http://supervisor/core/api/events/" + event_type
token = os.environ.get("SUPERVISOR_TOKEN")

if not token:
    print("Missing SUPERVISOR_TOKEN", flush=True)
    sys.exit(1)

print("Waiting for SAME/EAS alerts...", flush=True)

def fire_event(data):
    body = json.dumps(data).encode("utf-8")

    req = urllib.request.Request(
        ha_url,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=10) as response:
        print(f"HA event fired: {response.status}", flush=True)

for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    print(f"RAW: {line}", flush=True)

    if "ZCZC" not in line:
        continue

    event_data = {
        "raw": line,
        "received": int(time.time()),
        "source": "rtl_sdr_same_eas"
    }

    try:
        fire_event(event_data)
    except Exception as e:
        print(f"Failed to fire HA event: {e}", flush=True)
