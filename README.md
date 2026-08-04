# Loki Assistant 🎙️

A voice-controlled personal assistant that recognizes speech commands and performs various tasks through natural conversation.

## Features

- **Web Interface**: Modern chat UI with dark theme, animated mascot, and quick-command chips
- **Voice Recognition**: Microphone input via the browser (Chrome/Edge/Safari) or CLI
- **Text-to-Speech**: Audio feedback in the browser and in CLI mode
- **Web Browsing**: Open popular websites (YouTube, Google, Instagram, Facebook, LinkedIn, GitHub)
- **Music Playback**: Play songs from a custom music library
- **News Updates**: Get the latest US news headlines
- **Information Search**: Wikipedia searches and Google lookups
- **Time & Date**: Ask for current time and date
- **Wake Words**: Activate with "Loki", "Lo ki", or "Hey Loki" (CLI mode)
- **Exit Commands**: Graceful shutdown with exit keywords

## Requirements

Ensure you have Python 3.6+ installed. Install dependencies with:

```bash
# Web interface (all deployments)
pip install -r requirements.txt
```

```bash
# Extra dependencies for CLI voice mode (microphone + text-to-speech)
pip install -r requirements-cli.txt
```

Key libraries: `Flask` (web server), `speech_recognition` (CLI audio input), `pyttsx3` (CLI text-to-speech), `requests` (API calls), `wikipedia` (searches), `python-dotenv` (API keys), `webbrowser` (built-in).

## Installation

1. Clone or download the project:
```bash
git clone <repository-url>
cd Minor-Assistant
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. **API Key Setup**:
   - The assistant uses NewsAPI for news updates
   - Copy `.env.example` to `.env` and set your own key from [newsapi.org](https://newsapi.org)
   - The key is loaded from the `.env` file via `python-dotenv`

## Usage

### Web Interface (recommended)

A chat-style web frontend with an animated mascot, microphone support (Chrome/Edge/Safari), and text input:

```bash
python app.py
```

Then open http://127.0.0.1:5000 in your browser. The assistant replies with text and voice in the browser.

### CLI Voice Mode

The original voice-assistant loop with wake words ("Loki", "Lo ki", "Hey Loki"):

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
├── app.py                 # Flask web server (web interface)
├── loki_core.py           # Command logic shared by web and CLI modes
├── Loki-Assistant.py      # CLI voice assistant (wake words, TTS)
├── music_lib.py           # Music library with song links
├── templates/index.html   # Web UI page
├── static/style.css       # Web UI styling and animations
├── static/app.js          # Web UI logic (mic, chat, TTS)
├── static/mascot.png      # Animated mascot image
├── requirements.txt       # Web dependencies (also used by Vercel)
├── requirements-cli.txt   # Extra dependencies for CLI voice mode
├── vercel.json            # Vercel function configuration
├── .env.example           # Environment variable template
├── README.md              # This file
└── .env                   # Your API keys (not tracked in git)
```

## Deployment

The web interface is fully serverless-friendly and deploys to Vercel as a Flask function.

### Deploy to Vercel (GitHub import)

1. Push this repository to GitHub
2. Go to [vercel.com](https://vercel.com) → **Add New Project** → import the repository (framework auto-detects Flask)
3. In **Settings → Environment Variables**, add `NEWS_API_KEY` with your [NewsAPI](https://newsapi.org) key
4. Click **Deploy** — the app is now live, e.g. `https://minor-assistant-loki.vercel.app`

Future pushes to the main branch redeploy automatically.

### Deploy with Vercel CLI

```bash
npx vercel login
npx vercel dev        # test locally through Vercel's runtime
npx vercel env add NEWS_API_KEY production
npx vercel --prod
```

Notes:
- `vercel.json` configures the function (`maxDuration: 60`)
- Voice recognition runs in the browser (Web Speech API) — no server changes needed
- Websites and songs open in the user's browser, not on the server
- The NewsAPI free tier allows 100 requests per day

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
| API key error for news | Update the `NEWS_API_KEY` in your `.env` file |
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

API keys are stored in a `.env` file, which is ignored by git. The NewsAPI key is loaded at runtime with `python-dotenv`:

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('NEWS_API_KEY')
```

Never commit your `.env` file.

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
