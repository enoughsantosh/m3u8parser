const fetch = require("node-fetch");
const m3u8Parser = require("m3u8-parser");

module.exports = async (req, res) => {
    res.setHeader("Content-Type", "application/json");

    const { url } = req.query;
    if (!url) {
        return res.status(400).json({ error: "M3U8 URL is required" });
    }

    try {
        const response = await fetch(url, {
            method: "GET",
            headers: {
                "Referer": "https://toonstream.co",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
            }
        });

        if (!response.ok) {
            return res.status(400).json({ error: "Failed to fetch M3U8 playlist" });
        }

        const playlistText = await response.text();
        const parser = new m3u8Parser.Parser();
        parser.push(playlistText);
        parser.end();

        return res.json({ success: true, parsedData: parser.manifest });
    } catch (error) {
        return res.status(500).json({ error: "Internal server error", details: error.message });
    }
};
