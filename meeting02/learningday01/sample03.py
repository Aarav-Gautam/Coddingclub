'''import speech_recognition as sr
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))'''


import speech_recognition as sr

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

# Reading Microphone as source
# listening the speech and store in audio_text variable
with sr.Microphone() as source:
    print("Talk")
    audio_text = r.listen(source, timeout=None, phrase_time_limit=11)
    print("Listening finished")

    try:
        print("Text:", r.recognize_google(audio_text))
    except Exception as e:
        print("Error:", e)