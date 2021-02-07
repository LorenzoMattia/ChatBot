import json 
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from Alfred import Bea
import random
import pickle
import speech_recognition as sr

PROMPT_LIMIT = 5
recognizer = sr.Recognizer()
microphone = sr.Microphone()
assistent = Bea(recognizer, microphone, PROMPT_LIMIT)

with open("intents.json") as file:
    data = json.load(file)

def chat():
    # load trained model
    model = keras.models.load_model('chat_model')

    # load tokenizer object
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open('label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    # parameters
    max_len = 20
    
    while True:
        print("User: ")
        '''
        inp = input()
        if inp.lower() == "quit":
            break
        '''
        guess = assistent.hear()
        inp = guess["transcription"].lower()
        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                             truncating='post', maxlen=max_len))
        tag = lbl_encoder.inverse_transform([np.argmax(result)])
        '''
        for i in data['intents']:
            if i['tag'] == tag:
                print("ChatBot: ", np.random.choice(i['responses']))
        '''
        method = None 
        try:
            method = getattr(assistent, tag[0])
        except AttributeError:
            raise NotImplementedError('Error')
        method(inp)    
        # print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL,random.choice(responses))

print("Start messaging with the bot (type quit to stop)!")
chat()