from openai import OpenAI
import pyttsx3
import speech_recognition as sr
import time

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Speak")
    print("User:", end="")
    time.sleep(1) 
    audio_text = r.listen(source, timeout=None, phrase_time_limit=11)
    print("Listening finished")

    try:
        print(r.recognize_google(audio_text))
    except Exception as e:
        print("Error:", e)

userprompt=r.recognize_google(audio_text)

openai_client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

completion = openai_client.chat.completions.create(
    model="openai/gpt-4o",
    extra_body={
        "models": ["anthropic/claude-3.5-sonnet", "gryphe/mythomax-l2-13b"],
    },
    messages=[
        {
            "role": "user",
            "content": userprompt
        }
    ]
)


def speak(word=completion.choices[0].message.content):
    engine = pyttsx3.init()

# For Mac, If you face error related to "pyobjc" when running the `init()` method :
# Install 9.0.1 version of pyobjc : "pip install pyobjc>=9.0.1"

    engine.say(word)
    engine.runAndWait()
print(f"AI: {completion.choices[0].message.content}")
speak()
