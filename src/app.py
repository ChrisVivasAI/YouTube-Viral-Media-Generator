import streamlit as st
import os
from transcript_analyzer import TranscriptAnalyzer
from audio_generator import AudioGenerator
import base64

def get_binary_file_downloader_html(bin_file, file_label='File'):
    """Generate a download link for binary files"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

def main():
    st.title("YouTube Viral Media Generator")
    st.write("Transform YouTube content into viral social media clips!")

    analyzer = TranscriptAnalyzer()
    audio_gen = AudioGenerator()

    video_url = st.text_input("Enter YouTube Video URL:")

    if st.button("Create Viral Content"):
        try:
            with st.spinner("Creating viral content..."):
                viral_moments = analyzer.find_viral_moments(video_url)
                
                for i, moment in enumerate(viral_moments, 1):
                    with st.expander(f"Viral Content {i}"):
                        result = audio_gen.generate_audio(moment)
                        
                        # Display timestamp and content
                        st.write("⏰ Timestamp:", analyzer.format_timestamp(result['start']))
                        
                        st.write("📝 Original Content:")
                        st.text(result['text'])
                        
                        st.write("✨ Viral Script:")
                        st.text(result['script'])
                        
                        st.write("🔊 Audio Preview:")
                        st.audio(result['audio_path'])
                        
                        # Download audio button
                        st.markdown(
                            get_binary_file_downloader_html(
                                result['audio_path'],
                                f'viral_audio_{i}.mp3'
                            ),
                            unsafe_allow_html=True
                        )

        except Exception as e:
            st.error(f"Error: {str(e)}")
        finally:
            audio_gen.cleanup()

    with st.sidebar:
        st.subheader("How it works")
        st.write("""
        This app helps you find the most engaging moments in YouTube videos and craft viral social media content.
        
        How it works:
        1. Enter a YouTube video URL
        2. The app analyzes the video transcript
        3. AI identifies the most viral moments
        4. AI Generates Viral Scripts for Social Content         
        5. Audio clips are generated for each piece of Content
        5. Download and share!
        """)

if __name__ == "__main__":
    main() 