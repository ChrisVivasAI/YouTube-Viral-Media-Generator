import os
from typing import List, Dict, Tuple
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import together
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set API key using environment variable directly
os.environ["TOGETHER_API_KEY"] = os.getenv("TOGETHER_API_KEY", "")  # Fallback to empty string if not found

class TranscriptAnalyzer:
    def __init__(self):
        self.model = "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo"
        
    def extract_video_id(self, url: str) -> str:
        """Extract video ID from YouTube URL."""
        if "youtu.be" in url:
            return url.split("/")[-1]
        elif "youtube.com" in url:
            return url.split("v=")[1].split("&")[0]
        raise ValueError("Invalid YouTube URL")

    def get_transcript(self, video_url: str) -> List[Dict]:
        """Fetch transcript from YouTube video."""
        try:
            video_id = self.extract_video_id(video_url)
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return transcript
        except Exception as e:
            raise Exception(f"Error fetching transcript: {str(e)}")

    def segment_transcript(self, transcript: List[Dict], segment_duration: int = 30) -> List[Dict]:
        """Segment transcript into 30-second chunks."""
        segments = []
        current_segment = {
            "text": "",
            "start": 0,
            "duration": 0
        }
        
        for entry in transcript:
            if current_segment["duration"] + entry["duration"] <= segment_duration:
                current_segment["text"] += " " + entry["text"]
                current_segment["duration"] += entry["duration"]
            else:
                segments.append(current_segment)
                current_segment = {
                    "text": entry["text"],
                    "start": entry["start"],
                    "duration": entry["duration"]
                }
        
        if current_segment["text"]:
            segments.append(current_segment)
            
        return segments

    def analyze_segment(self, segment: str) -> bool:
        """Analyze if a segment would make good viral content."""
        prompt = f"""As a social media expert, determine if this video segment would make engaging viral content.
        Consider humor, emotional impact, quotability, and general appeal.
        Only respond with 'yes' or 'no'.
        
        Segment: {segment}"""
        
        try:
            response = together.Complete.create(
                prompt=prompt,
                model=self.model,
                max_tokens=10,
                temperature=0.3,
            )
            
            if isinstance(response, dict) and 'choices' in response:
                text = response['choices'][0]['text'].strip().lower()
            elif isinstance(response, dict) and 'output' in response and 'choices' in response['output']:
                text = response['output']['choices'][0]['text'].strip().lower()
            else:
                return True  # Default to including segment if response format is unexpected
                
            return 'yes' in text
            
        except Exception as e:
            print(f"Error analyzing segment: {str(e)}")
            return True  # Default to including segment on error
            
    def find_viral_moments(self, video_url: str, num_moments: int = 3) -> List[Dict]:
        """Find potential viral moments in the video."""
        # Get transcript (keeping existing method)
        transcript = self.get_transcript(video_url)
        segments = self.segment_transcript(transcript)
        
        # Analyze segments for viral potential
        prompt = f"""As a social media expert, analyze these video segments and identify the 3 most viral-worthy moments.
        Consider entertainment value, emotional impact, and share-worthy content.
        For each segment, explain why it would make great social media content.
        
        Segments to analyze:
        {[seg['text'] for seg in segments]}
        
        Return exactly 3 segments that would make the best viral content, numbered 1-3.
        """
        
        try:
            response = together.Complete.create(
                prompt=prompt,
                model=self.model,
                max_tokens=500,
                temperature=0.7
            )
            
            # Extract response
            if isinstance(response, dict) and 'choices' in response:
                analysis = response['choices'][0]['text']
            elif isinstance(response, dict) and 'output' in response and 'choices' in response['output']:
                analysis = response['output']['choices'][0]['text']
            else:
                raise Exception("Unexpected API response format")
            
            # Match analysis with original segments
            viral_moments = []
            for segment in segments:
                if segment['text'] in analysis:
                    viral_moments.append({
                        "text": segment['text'],
                        "start": segment['start'],
                        "duration": segment['duration']
                    })
                if len(viral_moments) >= 3:
                    break
                    
            return viral_moments[:3]
            
        except Exception as e:
            raise Exception(f"Error finding viral moments: {str(e)}")

    def format_timestamp(self, seconds: float) -> str:
        """Convert seconds to MM:SS format."""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}" 