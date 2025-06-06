# from flask import Flask, render_template, request, jsonify
# from dotenv import load_dotenv
# import os
# import google.generativeai as genai
# from youtube_transcript_api import YouTubeTranscriptApi

# load_dotenv()

# app = Flask(__name__)

# # Configure Gemini
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# PROMPT = """You are YouTube video summarizer. You will be taking the transcript text
# and summarizing the entire video and providing the important summary in points
# within 250 words. Please provide the summary of the text given here: """

# def extract_transcript_details(youtube_video_url):
#     try:
#         video_id = youtube_video_url.split("=")[1]
#         transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
#         transcript = " ".join([i["text"] for i in transcript_text])
#         return transcript
#     except Exception as e:
#         raise e

# def generate_gemini_content(transcript_text, prompt):
#     model = genai.GenerativeModel("gemini-pro")
#     response = model.generate_content(prompt + transcript_text)
#     return response.text

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     summary = None
#     error = None
#     thumbnail_url = None
    
#     if request.method == 'POST':
#         youtube_link = request.form.get('youtube_link')
#         if youtube_link:
#             try:
#                 video_id = youtube_link.split("=")[1]
#                 thumbnail_url = f"http://img.youtube.com/vi/{video_id}/0.jpg"
                
#                 transcript_text = extract_transcript_details(youtube_link)
#                 if transcript_text:
#                     summary = generate_gemini_content(transcript_text, PROMPT)
#             except Exception as e:
#                 error = f"Error processing video: {str(e)}"
    
#     return render_template('index.html', summary=summary, error=error, thumbnail_url=thumbnail_url)

# if __name__ == '__main__':
#     app.run(debug=True)





from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

load_dotenv()

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

PROMPT = """You are YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here: """

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1].split("&")[0]  # Handle URLs with additional parameters
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript
    except TranscriptsDisabled:
        raise Exception("Transcripts are disabled for this video")
    except NoTranscriptFound:
        raise Exception("No transcript available for this video")
    except VideoUnavailable:
        raise Exception("Video is unavailable or private")
    except Exception as e:
        raise Exception(f"Error retrieving transcript: {str(e)}")

def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        raise Exception(f"Error generating summary: {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    error = None
    thumbnail_url = None
    
    if request.method == 'POST':
        youtube_link = request.form.get('youtube_link')
        if youtube_link:
            try:
                # Extract video ID (handling various URL formats)
                if "youtu.be/" in youtube_link:
                    video_id = youtube_link.split("youtu.be/")[1].split("?")[0]
                else:
                    video_id = youtube_link.split("v=")[1].split("&")[0]
                
                thumbnail_url = f"http://img.youtube.com/vi/{video_id}/0.jpg"
                
                try:
                    transcript_text = extract_transcript_details(youtube_link)
                    if transcript_text:
                        summary = generate_gemini_content(transcript_text, PROMPT)
                except Exception as e:
                    error = str(e)
                    
            except Exception as e:
                error = f"Invalid YouTube URL: {str(e)}"
    
    return render_template('index.html', 
                         summary=summary, 
                         error=error, 
                         thumbnail_url=thumbnail_url)

if __name__ == '__main__':
    app.run(debug=True)