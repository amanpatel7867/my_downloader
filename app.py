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
        return render_template('index.html', error="Kripya URL paste karein!")

    # Block se bachne ke liye cookies zaroori hain
    cookie_path = 'cookies.txt'

    try:
        ydl_opts = {
            'format': 'best',
            'noplaylist': True,
            'quiet': True,
            'nocheckcertificate': True,
            'cookiefile': cookie_path if os.path.exists(cookie_path) else None,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # Facebook/Instagram ke liye specific handle
            video_url = info.get('url')
            if not video_url and 'entries' in info:
                video_url = info['entries'][0].get('url')
            
            return render_template('index.html', 
                                 direct_url=video_url, 
                                 title=info.get('title', 'Social Media Video'), 
                                 thumb=info.get('thumbnail', 'https://via.placeholder.com/400x225?text=Video+Found'))

    except Exception as e:
        print(f"Error: {e}")
        return render_template('index.html', error="Link nahi mil paya. Kripya cookies update karein ya sahi link daalein.")

app = app
