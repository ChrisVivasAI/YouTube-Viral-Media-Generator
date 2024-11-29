import os
from gtts import gTTS
from typing import Dict
import tempfile
import together
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set API key using environment variable directly
os.environ["TOGETHER_API_KEY"] = os.getenv("TOGETHER_API_KEY", "")  # Fallback to empty string if not found

class AudioGenerator:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.model = "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo"
    
    def create_viral_script(self, text: str) -> str:
        """Create a viral social media script from the transcript."""
        prompt = f"""As a viral TikTok/Instagram content creator, transform this video segment into an engaging script.
        Original text: {text}
        
        Create a conversational, engaging script that:
        1. Starts with a catchy hook
        2. Uses trending social media language and phrases
        3. Sounds natural and authentic
        4. Includes a strong call-to-action at the end
        5. Is optimized for social sharing
        
        Important:
        - Write ONLY the spoken words
        - Do NOT include any scene descriptions, camera directions, or speaker labels
        - Do NOT include any formatting or annotations
        - Write the script as a continuous piece of speech
        - Do not add quotes or other formatting 
        - Do not add introductions to the script like "Here's the rewritten script: or Here is the transformed script: or Here is the script:"
        
        Example format:
        Yo, you won't believe what I just discovered! [rest of the script] Don't forget to smash that like button!
        """
        
        try:
            response = together.Complete.create(
                prompt=prompt,
                model=self.model,
                max_tokens=300,
                temperature=0.7
            )
            
            if isinstance(response, dict) and 'choices' in response:
                script = response['choices'][0]['text'].strip()
            elif isinstance(response, dict) and 'output' in response and 'choices' in response['output']:
                script = response['output']['choices'][0]['text'].strip()
            else:
                raise Exception("Unexpected API response format")
                
            # Clean up any remaining formatting
            script = script.replace("Host:", "").replace("(", "").replace(")", "")
            script = script.replace("[Music]", "").replace("[Sound Effect]", "")
            lines = [line.strip() for line in script.split("\n") if line.strip() and not line.startswith(("Scene:", "Cut to:", "Camera:", "*"))]
            
            return " ".join(lines)
                
        except Exception as e:
            raise Exception(f"Error creating viral script: {str(e)}")
    
    def generate_audio(self, viral_moment: Dict) -> Dict:
        """Generate audio from viral script."""
        try:
            # Create viral script
            script = self.create_viral_script(viral_moment['text'])
            
            # Generate audio file
            filename = f"viral_moment_{int(viral_moment['start'])}.mp3"
            filepath = os.path.join(self.temp_dir, filename)
            
            tts = gTTS(text=script, lang='en', slow=False)
            tts.save(filepath)
            
            return {
                **viral_moment,
                "script": script,
                "audio_path": filepath
            }
            
        except Exception as e:
            raise Exception(f"Error generating content: {str(e)}")
    
    def cleanup(self):
        """
        Clean up temporary audio files.
        Should be called when the application shuts down.
        """
        try:
            for file in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            os.rmdir(self.temp_dir)
        except Exception as e:
            print(f"Error cleaning up audio files: {str(e)}") 