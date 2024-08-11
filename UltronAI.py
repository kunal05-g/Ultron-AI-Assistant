import openai
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import pyttsx3
import pyaudio

openai.api_key = '' # Use API Key obtained from OpenAI Account
# Pyttsx engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# sounddevice engine setup
def record_audio(duration=5,samplerate=16000):
    print("Ultron is Online...")   # Indicates that the program has executed
    recording = sd.rec(int(duration*samplerate), samplerate=samplerate, channels=1 ,dtype='int16' )
    sd.wait()
    return recording.flatten()

#convert audio to text
def recognize_speech(audio_data,samplerate=16000):
    recognizer= sr.Recognizer()
    audio= sr.AudioData(audio_data,samplerate,2)
    try:
        text= recognizer.recognize_google(audio) # type: ignore
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("Sorry, there was an Issue with Speech Recognition")
        return None
    
# get AI Respone
def get_openai_response(prompt):
    response = openai.Completion.create( 
        engine="",  # Use the appropriate voice model from OPENAI
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip() # type: ignore

#Playing Audio
def play_audio(audio_data, samplerate=16000):
    p= pyaudio.PyAudio()
    stream=p.open(format=pyaudio.paInt16,channels=1,rate=samplerate,output=True)
    stream.write(audio_data)
    stream.stop_stream()
    stream.close()
    p.terminate()


# Main Code, integrates everything
def main():
    while True:
        audio_data=record_audio(duration=5)
        user_input=recognize_speech(audio_data)
        if user_input:   
            response=get_openai_response(user_input)  
            print(f"Ultron says: {response}")

        response_audio= engine.getProperty('voice')
        response_audio_data= np.frombuffer(response.encode('utf-8'), dtype=np.int16)
        play_audio(response_audio_data)  

if __name__ == "__main__":
    main()           
