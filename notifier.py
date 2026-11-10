import json
import os
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

RESOURCE_ID = "139171"
VERSION_API = f"https://api.spigotmc.org/legacy/update.php?resource={RESOURCE_ID}"
RESOURCE_URL = f"https://www.spigotmc.org/resources/{RESOURCE_ID}/"
STATE_FILE = Path("last_version.txt")

def fetch_latest_version() -> str:
    request = Request(VERSION_API, headers={"User-Agent": "HyperVN-Spigot-Notifier/1.0"})
    with urlopen(request, timeout=20) as response:
        version = response.read().decode("utf-8").strip()
    if not version or len(version) > 100:
        raise RuntimeError(f"SpigotMC returned an invalid version: {version!r}")
    return version

def send_discord_notification(version: str, previous: str) -> None:
    webhook = os.environ.get("DISCORD_WEBHOOK", "").strip()
    if not webhook:
        raise RuntimeError("Missing DISCORD_WEBHOOK. Add it in GitHub Actions secrets.")
    payload = {
        "username": "HYPERVN Update Bot",
        "embeds": [{
            "title": "🚀 TuTienCore vừa có phiên bản mới!",
            "description": (
                f"**Phiên bản mới:** `{version}`\\n"
                f"**Phiên bản trước:** `{previous}`\\n\\n"
                f"[Xem tài nguyên và changelog trên SpigotMC]({RESOURCE_URL})"
            ),
            "url": RESOURCE_URL,
            "color": 7411656,
            "footer": {"text": "HYPERVN • SpigotMC Update Notifier"}
        }]
    }
    request = Request(webhook, data=json.dumps(payload).encode("utf-8"),
                      headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=20) as response:
        if response.status not in (200, 204):
            raise RuntimeError(f"Discord webhook returned HTTP {response.status}")

def main() -> int:
    try:
        latest = fetch_latest_version()
        previous = STATE_FILE.read_text(encoding="utf-8").strip() if STATE_FILE.exists() else ""
        if not previous:
            STATE_FILE.write_text(latest + "\\n", encoding="utf-8")
            print(f"Baseline saved: TuTienCore {latest}. No notification sent.")
            return 0
        if latest == previous:
            print(f"No update: TuTienCore {latest}")
            return 0
        send_discord_notification(latest, previous)
        STATE_FILE.write_text(latest + "\\n", encoding="utf-8")
        print(f"Notification sent: {previous} -> {latest}")
        return 0
    except (HTTPError, URLError, TimeoutError, RuntimeError, OSError) as error:
        print(f"Notifier failed: {error}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
