import os
import json
import re
import shutil
import tempfile
import whisper
import yt_dlp

def get_youtube_url():
    """
    Prompt the user to enter a YouTube URL.
    
    Returns:
        str: YouTube video URL
    """
    while True:
        url = input("Please paste your YouTube video URL: ").strip()
        
        # Basic URL validation
        if url.startswith(('https://www.youtube.com/', 'http://www.youtube.com/', 
                           'https://youtu.be/', 'http://youtu.be/')):
            return url
        else:
            print("Invalid YouTube URL. Please enter a valid YouTube video URL.")

def download_audio_with_yt_dlp(youtube_url, output_dir):
    """
    Download audio using yt-dlp library with more robust handling
    
    Args:
        youtube_url (str): YouTube video URL
        output_dir (str): Directory to save the audio file
    
    Returns:
        str: Path to the downloaded audio file
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(youtube_url, download=True)
            # Get the filename of the downloaded file
            audio_filename = ydl.prepare_filename(info_dict)
            
            # Change extension to wav
            base, _ = os.path.splitext(audio_filename)
            audio_filename = base + '.wav'
            
            return audio_filename
        except Exception as e:
            print(f"Error downloading audio: {e}")
            raise

def format_text_to_paragraphs(text, max_words_per_paragraph=100):
    """
    Convert transcribed text into paragraphs.
    
    Args:
        text (str): Raw transcribed text
        max_words_per_paragraph (int): Maximum words per paragraph
    
    Returns:
        list: Paragraphs of text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Split into words
    words = text.split()
    
    paragraphs = []
    current_paragraph = []
    
    for word in words:
        current_paragraph.append(word)
        
        # Create a new paragraph when word count reaches the max
        if len(current_paragraph) >= max_words_per_paragraph:
            paragraphs.append(' '.join(current_paragraph))
            current_paragraph = []
    
    # Add any remaining words as a final paragraph
    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))
    
    return paragraphs

def transcribe_youtube_video(youtube_url):
    """
    Transcribe a YouTube video directly from its audio stream using Whisper.
    
    Args:
        youtube_url (str): URL of the YouTube video to transcribe
    
    Returns:
        dict: Transcription details
    """
    # Create a temporary directory to store the audio
    temp_dir = tempfile.mkdtemp()
    try:
        # Download audio using yt-dlp
        audio_filename = download_audio_with_yt_dlp(youtube_url, temp_dir)
        
        # Load the Whisper model (you can change the model size as needed)
        print("\nLoading Whisper model... (this may take a moment)")
        model = whisper.load_model("base")
        
        # Transcribe the audio
        print("Transcribing audio... Please wait.")
        result = model.transcribe(audio_filename)
        
        # Format text into paragraphs
        paragraphs = format_text_to_paragraphs(result['text'])
        
        return {
            'paragraphs': paragraphs
        }
    
    finally:
        # Ensure temporary directory is always removed
        try:
            shutil.rmtree(temp_dir)
        except Exception as cleanup_error:
            print(f"Warning: Could not remove temporary directory: {cleanup_error}")

def save_transcription_to_json(transcription, output_file='transcription.json'):
    """
    Save the transcription text to a JSON file.
    
    Args:
        transcription (dict): Transcribed text details
        output_file (str): Path to save the JSON file
    """
    # Write to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(transcription, f, ensure_ascii=False, indent=4)
    
    print(f"Transcription saved to {output_file}")

def main():
    print("YouTube Video Transcription Tool")
    print("--------------------------------")
    
    try:
        # Get YouTube URL from user
        youtube_url = get_youtube_url()
        
        # Transcribe the video
        print("\nTranscribing video... This may take a few minutes.")
        transcription = transcribe_youtube_video(youtube_url)
        
        # Save transcription to JSON
        save_transcription_to_json(transcription)
        
        print("\nTranscription completed successfully!")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check if the video is publicly accessible")
        print("2. Ensure you have a stable internet connection")
        print("3. Verify the video URL is correct")
        print("4. Make sure FFmpeg is installed and in your system PATH")

if __name__ == "__main__":
    main()