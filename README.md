# Loki Assistant 🎙️

A voice-controlled personal assistant that recognizes speech commands and performs various tasks through natural conversation.

## Features

- **Voice Recognition**: Listen and respond to voice commands
- **Text-to-Speech**: Receive audio feedback from the assistant
- **Web Browsing**: Open popular websites (YouTube, Google, Instagram, Facebook, LinkedIn, GitHub)
- **Music Playback**: Play songs from a custom music library
- **News Updates**: Get the latest US news headlines
- **Information Search**: Wikipedia searches and Google lookups
- **Time & Date**: Ask for current time and date
- **Wake Words**: Activate with "Loki", "Lo ki", or "Hey Loki"
- **Exit Commands**: Graceful shutdown with exit keywords

## Requirements

Ensure you have Python 3.6+ installed. The project requires the following libraries:

- `speech_recognition` - For audio input and recognition
- `pyttsx3` - For text-to-speech functionality
- `requests` - For API calls
- `wikipedia` - For Wikipedia searches
- `webbrowser` - (Built-in) For opening web browsers

## Installation

1. Clone or download the project:
```bash
git clone <repository-url>
cd Minor-Assistant
```

2. Install required dependencies:
```bash
pip install SpeechRecognition pyttsx3 requests wikipedia-api
```

3. **API Key Setup**: 
   - The assistant uses NewsAPI for news updates
   - Replace the API key in the code with your own from [newsapi.org](https://newsapi.org)
   - Current key in code: `9c4c4c43ffa349068f6c81ac76fc64b6` (consider replacing for security)

## Usage

Run the assistant:
```bash
python Loki-Assistant.py
```

### Wake Words
The assistant listens for these activation phrases:
- "Loki"
- "Lo ki"
- "Hey Loki"

### Available Commands

After activation, you can use:

| Command | Example | Action |
|---------|---------|--------|
| Open websites | "open youtube", "open google" | Opens the specified website |
| Play music | "play wolf" | Plays songs from music library |
| News | "news" | Reads latest US news headlines |
| Search | "search for Python" | Searches Wikipedia/Google |
| Knowledge | "what is machine learning" | Provides Wikipedia summary |
| Time | "time" | Announces current time |
| Date | "date" | Announces today's date |
| Exit | "exit", "quit", "bye", "goodbye" | Shuts down the assistant |

### Exit Commands
- "exit"
- "quit"
- "goodbye"
- "stop"
- "bye"
- "shut down"

## Project Structure

```
Minor-Assistant/
├── Loki-Assistant.py      # Main assistant application
├── music_lib.py           # Music library with song links
├── README.md              # This file
└── __pycache__/           # Python cache directory
```

## Configuration

### Adding Songs to Music Library

Edit `music_lib.py` to add more songs:

```python
music = {
    "wolf": "https://youtu.be/2Sadfj-6wWI",
    "your_song": "https://youtu.be/VIDEO_ID"
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "I didn't catch that" | Speak clearly into your microphone |
| No internet connection error | Check your network connectivity |
| Microphone not working | Ensure microphone is connected and permissions are granted |
| API key error for news | Update the NewsAPI key in `command_execution()` |
| Speech recognition fails | Try adjusting timeout values in the code |

## Error Handling

The assistant handles various error scenarios:
- **UnknownValueError**: When speech isn't recognized
- **RequestError**: When API calls fail or no internet connection
- **General Exceptions**: Catches unexpected errors gracefully

## Notes

- The assistant requires an active internet connection for most features
- Google Speech Recognition API is used for voice-to-text conversion
- Microphone permissions must be granted by the operating system
- Text-to-speech quality depends on your system's audio output

## Security Note

The NewsAPI key is hardcoded in the script. For production use:
- Store API keys in environment variables
- Use a `.env` file and load it with `python-dotenv`

Example:
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('NEWS_API_KEY')
```

## Future Enhancements

Potential features to add:
- Weather updates
- Email management
- Calendar integration
- Smart home control
- More music platforms
- Custom wake words
- Improved NLP capabilities

## License

This project is open source and available for educational purposes.

## Author

Developed by :  Prateek Dewangan.

---

**Enjoy using Loki Assistant!** 🚀
