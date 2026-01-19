from flask import Flask, render_template, request
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_link', methods=['POST'])
def get_link():
    url = request.form.get('video_url')
    if not url:
        return render_template('index.html', error="Kripya link paste karein!")

    # Block se bachne ke liye Cookies file ka istemal
    cookie_path = 'cookies.txt'

    try:
        ydl_opts = {
            # 'best' format se teeno sites ke links nikal aayenge
            'format': 'best',
            'noplaylist': True,
            'quiet': True,
            'nocheckcertificate': True,
            'cookiefile': cookie_path if os.path.exists(cookie_path) else None,
            # Professional User-Agent
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            title = info.get('title', 'Social Media Video')
            thumb = info.get('thumbnail', 'https://via.placeholder.com/300x200?text=No+Thumbnail')

        return render_template('index.html', direct_url=video_url, title=title, thumb=thumb)

    except Exception as e:
        print(f"Error: {e}")
        return render_template('index.html', error="Link nahi mil paya. Link sahi hai ya nahi, ye check karein.")

app = app
