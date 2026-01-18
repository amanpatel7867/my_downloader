from flask import Flask, render_template, request
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_link', methods=['POST'])
def get_link():
    url = request.form.get('video_url')
    if not url:
        return render_template('index.html', error="Kripya ek valid link paste karein!")

    try:
        # ydl_opts ko optimize kiya gaya hai download link nikalne ke liye
        ydl_opts = {
            'format': 'best',  # Sabse acchi quality jisme audio+video dono ho
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            # Kabhi-kabhi user-agent ki wajah se block hota hai, isliye ye zaruri hai:
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Metadata extract karein
            info = ydl.extract_info(url, download=False)
            
            # Direct link nikalne ka sahi tarika
            video_url = info.get('url')
            title = info.get('title')
            thumbnail = info.get('thumbnail')

            if not video_url:
                return render_template('index.html', error="Video link nahi mil paya. Dusra video try karein.")

            return render_template('index.html', 
                                 direct_url=video_url, 
                                 title=title, 
                                 thumb=thumbnail)

    except Exception as e:
        print(f"Error details: {e}") # Terminal mein error check karne ke liye
        return render_template('index.html', error="Kuch galat hua. Shayad link galat hai ya site blocked hai.")

if __name__ == "__main__":
    app.run(debug=True)