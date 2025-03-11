import m3u8
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/parse")
async def parse_master_playlist(url: str, referer: str = ""):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": referer
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return JSONResponse(content={"error": "Failed to fetch M3U8 file"}, status_code=500)

        master_playlist = m3u8.loads(response.text)

        if not master_playlist.is_variant:
            return JSONResponse(content={"error": "Not a master playlist"}, status_code=400)

        streams = [
            {
                "resolution": playlist.stream_info.resolution,
                "bandwidth": playlist.stream_info.bandwidth,
                "url": playlist.uri
            }
            for playlist in master_playlist.playlists
        ]

        return {"streams": streams}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Vercel needs a handler
import os
if os.environ.get("VERCEL"):
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
