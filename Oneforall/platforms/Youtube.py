import asyncio
import os
import random
import re
from typing import Union
import requests
import httpx
import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch

from Oneforall.utils.database import is_on_off
from Oneforall.utils.formatters import time_to_seconds

def cookies():
    url = "https://v0-mongo-db-api-setup.vercel.app/api/cookies.txt"
    filename = "cookies.txt"

    if os.path.exists(filename):
        os.remove(filename)

    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)
        return filename
    else:
        raise Exception("Failed to fetch cookies from URL")

def ensure_download_dir():
    os.makedirs("downloads", exist_ok=True)

async def shell_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, errorz = await proc.communicate()
    return (out if not errorz else errorz).decode("utf-8")

async def api_download(vidid, video=False):
    ensure_download_dir()
    API = "https://api.cobalt.tools/api/json"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    path = os.path.join("downloads", f"{vidid}.{'mp4' if video else 'm4a'}")
    data = {
        "url": f"https://www.youtube.com/watch?v={vidid}",
        **({"vQuality": "480"} if video else {"isAudioOnly": "True", "aFormat