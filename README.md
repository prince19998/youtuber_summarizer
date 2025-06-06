# YouTube Video Summarizer

A Flask web application that summarizes YouTube videos using their transcripts and Google Gemini (Generative AI).

## Features
- Simple web interface to input YouTube video links
- Fetches video transcript automatically
- Summarizes the transcript using Google Gemini (Generative AI)
- Displays the summary in under 250 words
- Shows the video thumbnail
- Handles errors for invalid links or API issues

## Demo
![Demo Screenshot](screenshot.png) <!-- Add a screenshot if available -->

## Tech Stack
- Python 3
- Flask
- Google Generative AI (Gemini)
- YouTube Transcript API
- HTML/CSS (Jinja2 templates)

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd video_summarizer_youtube
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv youvenv
   source youvenv/bin/activate  # On Windows: youvenv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Create a `.env` file in the project root.
   - Add your Google API key:
     ```env
     GOOGLE_API_KEY=your_google_api_key_here
     ```

5. **Run the application:**
   ```bash
   python app.py
   ```
   The app will be available at `http://127.0.0.1:5000/`.

## Usage
1. Open the web app in your browser.
2. Enter a YouTube video link (e.g., `https://www.youtube.com/watch?v=VIDEO_ID`).
3. Click "Get Detailed Notes".
4. View the summary and video thumbnail.

## File Structure
```
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # HTML template for the web UI
├── youvenv/              # (Optional) Virtual environment
└── README.md             # Project documentation
```

## Notes
- Make sure the YouTube video has transcripts available (auto-generated or manual).
- The Google Gemini API key is required for summarization.

## License
MIT License 