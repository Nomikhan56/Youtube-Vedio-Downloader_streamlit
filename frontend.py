import os
import streamlit as st
import time
from backend import download_video  # Backend function for downloading videos

# ✅ Streamlit Page Config
st.set_page_config(
    page_title="YouTube Downloader",
    page_icon="🎥",
    layout="centered",
    menu_items={"Get help": None, "Report a bug": None, "About": None}  # Hides extra menu options
)

# ✅ Custom CSS
st.markdown("""
    <style>
        /* Fix Header to Top */
        .header-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #334075;
            padding: 15px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            z-index: 1000;
        }
        .block-container { padding-top: 80px !important; }
        .header-container .left {
            font-size: 22px;
            font-weight: bold;
            color: white;
            margin-left: 20px;
        }
        .header-container .right {
            display: flex;
            gap: 20px;
            margin-right: 20px;
            align-items: center;
        }
        .header-container a, .header-container select {
            color: white;
            font-size: 16px;
            text-decoration: none;
            border: none;
            background: none;
            transition: color 0.3s ease;
        }
        .header-container a:hover { color: #f8d210; }
        .header-container select {
            color: black;
            padding: 5px;
            border-radius: 5px;
            background-color: white;
        }
        header {visibility: hidden;}
        @media (max-width: 768px) {
            .header-container {
                flex-direction: column;
                padding: 10px;
            }
            .header-container .right {
                flex-direction: column;
                gap: 10px;
                margin-right: 0;
            }
        }
    </style>
""", unsafe_allow_html=True)

# ✅ Header (Fixed to Top)
st.markdown("""
    <div class="header-container">
        <div class="left">YT5s</div>
        <div class="right">
            <a href="#">YouTube Downloader</a>
            <a href="#">YouTube To Mp3</a>
            <a href="#">YouTube To Mp4</a>
            <select id="language">
                <option>English</option>
                <option>Urdu</option>
                <option>French</option>
            </select>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h3 style="color: #334075;">YT5s : YouTube Video Downloader</h3>
        <p style="color: #555;">Convert and download YouTube videos in high quality.</p>
    </div>
""", unsafe_allow_html=True)

# ✅ Input Fields
url = st.text_input("🔗 Enter YouTube Video URL", placeholder="Paste the YouTube link here...")
file_format = st.selectbox("📁 Choose File Format", ["MP4 (Video)", "MP3 (Audio)"])

if file_format == "MP4 (Video)":
    resolution = st.selectbox("📺 Choose Resolution", ["360p", "720p", "1080p"])

# ✅ Start Download Button
if st.button("🚀 Start Download"):
    if not url:
        st.error("⚠ Please enter a YouTube video URL!")
    else:
        # ✅ Progress Bar Initialization
        progress_bar = st.progress(0)
        progress_text = st.empty()  # Text to show progress updates
        processing_popup = st.empty()  # Placeholder for the "Processing..." message
        
        start_time = time.time()  # Track start time

        # Simulating Progress Update
        for i in range(1, 101, 10):  
            time.sleep(0.5)  # Simulate delay
            progress_bar.progress(i)
            progress_text.text(f"🔄 Downloading... {i}% completed")

            # ✅ Show popup only if downloading takes longer
            if i >= 90 and (time.time() - start_time > 5):
                processing_popup.markdown('<div class="popup">⏳ Please wait, the video is being processed... Once done, the video will be downloaded and saved directly to your Downloads folder</div>', unsafe_allow_html=True)
                time.sleep(1.5)  

        # ✅ Calling Backend Function
        result = download_video(url, resolution if file_format == "MP4 (Video)" else "audio", file_format)  # Pass the selected format
        
        # ✅ Handling Download Result
        if result["status"] == "success":
            progress_bar.progress(100)
            progress_text.text("✅ Download Complete!")
            processing_popup.empty()  # ✅ Remove processing popup
            st.success(result["message"])
            
            with open(result["file"], "rb") as file:
                st.download_button("⬇ Download File", file, file_name=result["file"], key="download_file")
            
            os.remove(result["file"])  # ✅ Delete after showing download button
        else:
            progress_text.text("")  # Clear progress text
            progress_bar.empty()  # Hide progress bar
            processing_popup.empty()  # ✅ Remove processing popup
            st.error(result["message"])
# ✅ Centered Text Below Download Button
st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)
st.markdown("""
    <div style=" text-align: center;">
        <h4 style="color: #334075;">Online YouTube Video Downloader</h4>
        <p style="max-width: 800px; margin: 0 auto; text-align: justify; color: #555;">
            YT5s is your go-to online tool for easy YouTube video downloading and conversion.
            Our YouTube Downloader allows you to download YouTube videos into various formats
            including MP4, 3GP, WMA, FLV, WEBM, MP3, and more. With its user-friendly interface,
            you can download and convert unlimited high-quality YouTube videos such as 320p, 420p, 
            720p, 1080p, etc. This YouTube Downloader works on all devices such as mobile, 
            desktop, and tablet. A key feature of YT5s is that it allows you to download 
            YouTube videos without software installation or account creation. With our 
            YouTube Video Downloader, you can easily download your favorite YouTube videos 
            to enjoy offline, anytime and anywhere.
        </p>
    </div>
""", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)


st.markdown("""
    <div style="display: flex; flex-wrap: wrap; gap: 40px;">
        <div style="flex: 1; min-width: 300px;">
            <h5 style="color: #334075;">⚙️ No Software Installation Needed</h5>
            <p style="color: #555;">
                YT5s is an online YouTube video downloader, so you don’t need to install any software or create an account. 
                You can simply visit the website and start downloading YouTube videos immediately.
            </p>
        </div>
          <div style="flex: 1; min-width: 300px;">
            <h5 style="color: #334075;">⚡ Fast Download Speed</h5>
            <p style="color: #555;">
                The platform offers fast download speeds, allowing you to quickly download YouTube videos at up to 1GB/s without delays, even for longer content..  
            </p>
        </div>
         <div style="flex: 1; min-width: 300px;">
        <h5 style="color: #334075;">🎥 High-Quality Downloads</h5>
            <p style="color: #555;">
                You can choose the quality of the video before downloading, with many options such as 360p, 420p, 720p, 1080p, and 4K. This ensures you get the best quality for your device and storage needs..  
            </p>
        </div>
              <div style="flex: 1; min-width: 300px;">
                   <h5 style="color: #334075;">🔒 Secure and Safe</h5>
            <p style="color: #555;">
                Our YouTube Downloader ensures that your downloads are secure, with no malware, viruses, or harmful software. The site is free from risks, making it a safe choice for users..  
            </p>
        </div>
""", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)

st.markdown("""
        <div style=" margin-bottom: 10px; text-align: center;">
        <h4 style="color: #334075;">How to download YouTube videos?</h4>
    </div>
    <div style="display: flex; flex-wrap: wrap; gap: 40px;">
        <div style="flex: 1; min-width: 300px;">
            <h5 style="color: #334075;">Step 1</h5>
            <p style="color: #555;">
              Simply copy the YouTube link you want to convert, then paste it into the search box.
            </p>
    </div>
        </div>
          <div style="flex: 1; min-width: 300px;">
            <h5 style="color: #334075;">Step 2</h5>
            <p style="color: #555;">
               Choose the 360p,720p or 1080p Resoultion you want, then click the download button.  
            </p>
        </div>
         <div style="flex: 1; min-width: 300px;">
        <h5 style="color: #334075;">Step 3</h5>
            <p style="color: #555;">
             Wait for the conversion to finish, it may take some time depending on the resolution you selected. Then, download the file. It will be directly saved in your downloads folder..  
            </p>
        </div>
""", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)




