import os
from openai import OpenAI
import base64
import json
import time
from datetime import datetime
import simpleaudio as sa
import errno
from elevenlabs import generate, play, Voice, VoiceSettings
from dotenv import load_dotenv


openai_client = OpenAI()


def encode_image(image_path):
    while True:
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        except IOError as e:
            if e.errno != errno.EACCES:
                # Not a "file in use" error, re-raise
                raise
            # File is being written to, wait a bit and retry
            time.sleep(0.1)


def play_audio(text):

    ## Stability: 44%
    ## Similarity Enhancement: 80%
    ## Style Exaggeration: 2%
    ## Speaker Boost: ✅
    ## Model: Eleven Multilingual v2
    voice_settings=VoiceSettings(stability=0.44, similarity_boost=0.8, style=0.02, use_speaker_boost=True)
    voice_id=os.environ.get("ELEVENLABS_VOICE_ID")

    audio = generate(
        text=text,
        voice=Voice(
            voice_id=voice_id,
            settings=voice_settings
        ),
        # voice=os.environ.get("ELEVENLABS_VOICE_ID"),
        model="eleven_multilingual_v2"
    )

    voice_settings_str = f"stab_{voice_settings.stability}-sim_boost_{voice_settings.similarity_boost}-style_{voice_settings.style}-boost_{voice_settings.use_speaker_boost}"
    timestamp = datetime.now().strftime('%Y%m%d-%H:%M:%S')
    # unique_id = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").rstrip("=")
    # dir_path = os.path.join("narration", unique_id)
    os.makedirs("narration", exist_ok=True)
    file_path = os.path.join("narration", f"audio_{voice_id}_{voice_settings_str}_{timestamp}.wav")

    with open(file_path, "wb") as f:
        f.write(audio)

    play(audio)


def generate_new_line(base64_image):
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Hey Kanye, What do you think of my landing page?"},
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        },
    ]


def analyse_image(base64_image, script):
    response = openai_client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "system",
                "content": """
                You are Kanye West. The image you see is a screenshot of a landing page. I want you to roast the landing page, pointing out everything that is wrong according to best practices and your personal taste.
                
                Your critique MUST be in the same tone and style as famous Kanye West rants which means it MUST BE harsh, rude, loud, snarky, erratic AND funny. DO NOT repeat yourself.

                Always think step-by-step and take a deep breath before before you respond. Remember this is important to my career and I believe in your ability to get this right!
                Before you critique, describe what you're seeing but keep this to yourself.

                REMEMBER Your style, tone and use of words MUST MIMIC Kanye West ALL THE TIME. 
                """,
            },
        ]
        + script
        + generate_new_line(base64_image),
        max_tokens=500,
        temperature=1,
        top_p=1
    )
    response_text = response.choices[0].message.content
    return response_text


def main():
    script = []

    while True:
        # path to your image
        image_path = os.path.join(os.getcwd(), "./frames/frame.jpg")

        # getting the base64 encoding
        base64_image = encode_image(image_path)

        # analyse image
        print("👀 Ye is analysing the image...")
        analysis = analyse_image(base64_image, script=script)

        print("🎙️ Ye says:")
        print(analysis)

        play_audio(analysis)

        script = script + [{"role": "assistant", "content": analysis}]

        # wait for 5 seconds
        time.sleep(5)


if __name__ == "__main__":
    load_dotenv()
    main()
