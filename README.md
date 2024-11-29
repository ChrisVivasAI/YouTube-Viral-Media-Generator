# YouTube Viral Media Generator

A Streamlit application that uses AI to identify and transform viral moments from YouTube videos into shareable social media content.

## Features

- Extract transcripts from YouTube videos
- Identify top viral moments using Together AI's NLP analysis
- Generate engaging audio clips with text-to-speech
- Interactive web interface built with Streamlit
- Download options for generated content

## Prerequisites

- Python 3.7+
- A Together AI API key

## Installation

1. Clone the repository:
```bash
git clone <https://github.com/ChrisVivasAI/YouTube-Viral-Media-Generator.git>
cd youtube-viral-video
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Together AI API key:
```
TOGETHER_API_KEY=your_api_key_here
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run src/app.py
```

2. Open your web browser and navigate to the provided URL (typically `http://localhost:8501`)

3. Enter a YouTube video URL and click "Create Viral Content"

4. The app will:
   - Extract the video transcript
   - Analyze for viral moments
   - Generate audio clips
   - Provide download options

## Project Structure

```
youtube-viral-video/
├── src/
│   ├── __init__.py
│   ├── app.py              # Streamlit web application
│   ├── transcript_analyzer.py  # YouTube transcript analysis
│   └── audio_generator.py   # Audio generation functionality
├── requirements.txt        # Project dependencies
├── .env                    # Environment variables
└── README.md              # Project documentation
```

## Dependencies

- `streamlit`: Web application framework
- `youtube_transcript_api`: YouTube transcript extraction
- `together`: AI-powered text analysis
- `gTTS`: Text-to-speech conversion
- `python-dotenv`: Environment variable management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 