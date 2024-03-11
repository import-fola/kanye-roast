# Kanye West Roasts your landing page. 


## Setup
### Code setup

Clone this repo, and setup and activate a virtualenv:

```bash
python3 -m pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
```

Install the dependencies:
```
pip install -r requirements.txt
```

Create a an empty `.env` file.

### Account setup

Create an [OpenAI](https://beta.openai.com/) account. Create a secret API key, copy the key and add it to your `.env` file. **PS**: Remember to buy credits for your account.

```python
OPENAI_API_KEY=<token>
```

Create an [ElevenLabs](https://elevenlabs.io) account. Create a secret API key, copy the key and add it to your `.env` file. 


```
ELEVENLABS_API_KEY=<eleven-token>
```

### Voice setup
Make a new voice in Eleven and get the voice id of that voice using their [get voices](https://elevenlabs.io/docs/api-reference/voices) API, or by clicking the flask icon next to the voice in the VoiceLab tab. 

If you want to clone a voice, you can use their [Instant Voice Cloning](https://elevenlabs.io/docs/voicelab/instant-voice-cloning) feature. You need at least 3 minutes of clear audio of the voice you want to clone.

Play around with the [voice settings](https://elevenlabs.io/docs/speech-synthesis/voice-settings) to get the voice to sound how you want it to.

Add the voice id to your `.env` file:

```
ELEVENLABS_VOICE_ID=<voice-id>
```

## Run it!

### Browser capture
If you want to take screenshots of your browser, you need to:
1. On your screen, have your terminal and browser window in the same screen. On a Mac, you just need to drag one screen into the other one (one of the screens needs to be full screen for this to work).
2. Get the title of the browser window you want to capture. You can do this by hovering your mouse over the browser tab and you will see the window title.

In one terminal, run the browser capture:

```bash
python browser_capture.py "Your window title"
```
In another terminal, run the narrator:

```bash
python narrator.py
```

### Webcam capture
If you want the screenshots from your webcam instead then:

In one terminal, run the webcam capture:

```bash
python webcam_capture.py
```
In another terminal, run the narrator:

```bash
python narrator.py
```