YouTube Video Transcription Tool
This project provides a tool to transcribe YouTube videos into text. The tool downloads the audio from a YouTube video, uses the Whisper model to transcribe the audio into text, and formats the transcription into readable paragraphs. The transcribed text is then saved to a JSON file.

Features
YouTube URL Input: Enter the YouTube URL of the video you want to transcribe.
Audio Downloading: Automatically downloads the audio from the YouTube video using the yt-dlp library.
Transcription: Uses OpenAI's Whisper model to transcribe the audio into text.
Text Formatting: Formats the transcription into paragraphs with a customizable word limit per paragraph.
Save Transcription: Saves the transcribed text in a well-structured JSON file.
Requirements
To run this project, make sure you have the following dependencies installed:

Python 3.7 or higher
yt-dlp: A command-line program to download videos from YouTube and other video sites.
whisper: OpenAI’s Whisper model for transcription.
Install the required dependencies using pip:

bash
Copy code
pip install yt-dlp whisper
Usage
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/YouTube-Video-Transcription-Tool.git
cd YouTube-Video-Transcription-Tool
Run the script:

bash
Copy code
python transcribe_youtube.py
The script will prompt you to enter the YouTube video URL. After entering the URL, the transcription will start and the result will be saved to transcription.json.

Example:
bash
Copy code
Please paste your YouTube video URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Functions
get_youtube_url()
Prompts the user to enter a valid YouTube video URL.

download_audio_with_yt_dlp(youtube_url, output_dir)
Downloads the audio from the provided YouTube video URL and saves it in the specified output directory.

format_text_to_paragraphs(text, max_words_per_paragraph=100)
Formats the transcribed text into paragraphs with a specified maximum number of words per paragraph.

transcribe_youtube_video(youtube_url)
Transcribes the audio of the YouTube video using Whisper and returns the transcription in paragraph format.

save_transcription_to_json(transcription, output_file='transcription.json')
Saves the transcription text to a JSON file.
