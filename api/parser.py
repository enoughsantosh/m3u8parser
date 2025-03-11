import m3u8
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/parse", methods=["GET"])
def parse_master_playlist():
    url = request.args.get("url")
    referer = request.args.get("referer", "")

    if not url:
        return jsonify({"error": "Missing M3U8 URL"}), 400

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Referer": referer
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch M3U8 file"}), 500

        master_playlist = m3u8.loads(response.text)

        if not master_playlist.is_variant:
            return jsonify({"error": "Not a master playlist"}), 400

        streams = [
            {
                "resolution": playlist.stream_info.resolution,
                "bandwidth": playlist.stream_info.bandwidth,
                "url": playlist.uri
            }
            for playlist in master_playlist.playlists
        ]

        return jsonify({"streams": streams})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Required for Vercel deployment
def handler(event, context):
    return app(event, context)
