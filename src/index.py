from flask import Flask, request, jsonify, Response
import yt_dlp

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "ok", "message": "YouTube Downloader API on Vercel"})

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing ?url= parameter"}), 400

    try:
        # Use yt-dlp in memory (no file saving)
        ydl_opts = {
            'format': 'mp4',
            'quiet': True,
            'outtmpl': '-',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            stream_url = info['url']

        return jsonify({
            "title": info.get("title"),
            "duration": info.get("duration"),
            "direct_url": stream_url
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def handler(event, context):
    return app(event, context)
