import os
import re
from pytubefix import YouTube

def download_video(url, resolution_or_audio, file_format):
    try:
        yt = YouTube(url)

        # ✅ Check the file format selected
        if file_format == "MP4 (Video)":
            # ✅ Find video and audio streams for MP4
            video_stream = yt.streams.filter(res=resolution_or_audio, file_extension="mp4", progressive=False).first()
            audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()

            if not video_stream:
                return {"status": "error", "message": f"Resolution {resolution_or_audio} not available."}
            if not audio_stream:
                return {"status": "error", "message": "No suitable audio stream found!"}

            # ✅ Download Video & Audio
            video_path = video_stream.download(filename="video.mp4")
            audio_path = audio_stream.download(filename="audio.mp4")

            if not os.path.exists(video_path) or not os.path.exists(audio_path):
                return {"status": "error", "message": "Downloaded files are missing."}

            # ✅ Clean filename
            safe_title = re.sub(r'[\\/*?:"<>|]', "", yt.title).replace(" ", "_")
            output_filename = f"{safe_title}.mp4"

            # ✅ Merge video & audio using FFmpeg
            command = f'ffmpeg -i "video.mp4" -i "audio.mp4" -c:v copy -c:a aac -strict experimental "{output_filename}"'
            os.system(command)

            # ✅ Remove temporary files
            os.remove(video_path)
            os.remove(audio_path)

            return {"status": "success", "message": "Download complete!", "file": output_filename}
        
        elif file_format == "MP3 (Audio)":
            # ✅ Find audio stream for MP3
            audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()

            if not audio_stream:
                return {"status": "error", "message": "No suitable audio stream found!"}

            # ✅ Download Audio
            audio_path = audio_stream.download(filename="audio.mp4")

            if not os.path.exists(audio_path):
                return {"status": "error", "message": "Downloaded audio file is missing."}

            # ✅ Clean filename
            safe_title = re.sub(r'[\\/*?:"<>|]', "", yt.title).replace(" ", "_")
            output_filename = f"{safe_title}.mp3"

            # ✅ Convert audio to MP3 using FFmpeg
            command = f'ffmpeg -i "audio.mp4" -vn -ar 44100 -ac 2 -b:a 192k "{output_filename}"'
            os.system(command)

            # ✅ Remove temporary files
            os.remove(audio_path)

            return {"status": "success", "message": "Audio Download complete!", "file": output_filename}

    except Exception as e:
        return {"status": "error", "message": str(e)}
