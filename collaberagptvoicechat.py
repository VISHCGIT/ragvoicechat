import openai
# from transformers import GPT2Tokenizer, GPT2LMHeadModel
import speech_recognition as sr
import pyttsx3
import time
import streamlit as st
 
PREDICT_ENDPOINT="https://collaberadigital.katonic.ai/650439b72985b42b4d431681/genai/gd-f3cda8ba-14b7-42b8-9848-311111f769b7/api/v1/predict"
SECURE_TOKEN="gd-f3cda8ba-14b7-42b8-9848-311111f769b7-650439b72985b42b4d431681-API_Key_SME eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzMTExMTFmNzY5YjctOGVlZDA3ZWVmNDZmNDI4MmI4MWI1MDkwYjY0OTQ0N2ZrYXRvbmljIiwiZXhwIjozMzIzMjA4MjA5MDM2NH0.VzTeNRzXMCAHGfMv5V35CwSVvOmc3SKXPvNyvLZWdYY"
 
 
#openai.api_key = "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"
openai.api_key = "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"
engine=pyttsx3.init()
 
def transcribe_audio_to_test(filename):
    recogizer=sr.Recognizer()
    with sr.AudioFile(filename)as source:
        audio=recogizer.record(source)
    try:
        return recogizer.recognize_google(audio)
    except:
        print("skipping unkown error")
 
def generate_response(prompt):
    data = {"data": prompt}
    result = requests.post(PREDICT_ENDPOINT, json = data,verify=False, headers = {"Authorization":SECURE_TOKEN})
    response = result.text
    # response= openai.Completion.create(
    #     engine="gpt-3.5-turbo-instruct",
    #     prompt=prompt,
    #     max_tokens=4000,
    #     n=1,
    #     stop=None,
    #     temperature=0.5,
    # )
    return response
 
def speak_text(text):
    engine.say(text)
    engine.runAndWait()
 
def main():
    st.title('Voice Assistant')
    start_button = st.button('Start')
    if start_button:
        with sr.Microphone() as source:
            recognizer=sr.Recognizer()
            audio=recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower()=="hello":
                    #record audio
                    filename ="input.wav"
                    st.write("Please Say your Question")
                    with sr.Microphone() as source:
                        recognizer=sr.Recognizer()
                        source.pause_threshold=1
                        audio=recognizer.listen(source,phrase_time_limit=None,timeout=None)
                        with open(filename,"wb")as f:
                            f.write(audio.get_wav_data())
                       
                    text=transcribe_audio_to_test(filename)
                    if text:
                        st.write(f"You Just Said...-> {text}\n")
                       
                        #Generate the response
                        response = generate_response(text)
                        st.write(f"ChatGPT3 says \n{response}\n")
                           
                        #read resopnse using GPT3
                        speak_text(response)
                       
            except Exception as e:  
                st.write("An error ocurred : {}".format(e))
                       
if __name__=="__main__":
    main()