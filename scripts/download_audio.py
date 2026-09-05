"""
Download Audio Script for The Hotelier Huddle

Downloads all 20 podcast audio files directly from the public Anchor / Spotify CDN
into the local audio/ directory.
"""

import os
import json
import urllib.request
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
RSS_DUMP_PATH = os.path.join(BASE_DIR, "live_rss_feed_dump.json")

os.makedirs(AUDIO_DIR, exist_ok=True)

with open(RSS_DUMP_PATH, 'r', encoding='utf-8') as f:
    episodes = json.load(f)

print(f"Downloading {len(episodes)} episodes into {AUDIO_DIR}...")

for ep in episodes:
    ep_num = ep["episode_number"]
    url = ep.get("enclosure_url")
    if not url:
        continue
        
    out_name = f"{ep_num:02d}-{ep['title'].replace('/', '-').replace(':', ' -')}.mp3"
    out_path = os.path.join(AUDIO_DIR, out_name)
    
    if os.path.exists(out_path):
        print(f"  [✓] Ep {ep_num:02d} already downloaded: {out_name}")
        continue
        
    print(f"  [↓] Downloading Ep {ep_num:02d}: {out_name}...")
    try:
        urllib.request.urlretrieve(url, out_path)
        print(f"      Saved ({os.path.getsize(out_path)/(1024*1024):.2f} MB)")
    except Exception as e:
        print(f"      ERROR: {e}")

print("Download process complete.")
