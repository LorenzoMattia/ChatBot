import random
import time
import os 
from gtts import gTTS 
import speech_recognition as sr
import spacy
from SpeechParser import Parser
import numpy as np

#["Please provide us your complaint in order to assist you", "Please mention your complaint, we will reach you and sorry for any inconvenience caused"]


#sistemare la conferma della prenotazione volo

class Bea():

    def __init__(self, recognizer, microphone, limit):
        self.shop_list = ['mediaworld', 'nike', 'adidas', 'mcdonald']
        self.shop_type_list = ['electronics stores', 'restaurants', 'clothes shops', 'cafe', 'hairdresser', 'supermarket']
        self.recognizer = recognizer
        self.microphone = microphone
        self.limit = limit
        self.parser = Parser()
        
    def recognize_speech_from_mic(self, recognizer, microphone):
        # check that recognizer and microphone arguments are appropriate type
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        # adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught,
        #     update the response object accordingly
        try:
            response["transcription"] = recognizer.recognize_google(audio)
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"

        return response
        
    def hear(self):
        for j in range(self.limit):
            print('Speak!')
            guess = self.recognize_speech_from_mic(self.recognizer, self.microphone)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. What did you say?\n")

            # if there was an error, stop the game
            if guess["error"]:
                print("ERROR: {}".format(guess["error"]))
                break

        # show the user the transcription
        print("You said: {}".format(guess["transcription"]))
        return guess
        
    def speak(self, sentence):
        language = 'en'
        myobj = gTTS(text=sentence, lang=language, slow=False) 
        myobj.save("welcome.mp3") 
        os.system("mpg321.exe welcome.mp3")
    
    def greeting(self, sentence):
        print("Hi, how can I help you?")
        self.speak("Hi, how can I help you?")
    
    def shops(self, sentence):
        rnd1 = random.randint(0,len(self.shop_list)-1)
        rnd2 = random.randint(0,len(self.shop_list)-1)
        while rnd1 == rnd2:
            rnd2 = random.randint(0,len(self.shop_list)-1)
        print('Some of the shops you can find here are the followings: ' +  self.shop_list[rnd1] + ', ' + self.shop_list[rnd2])
        self.speak('Some of the shops you can find here are the followings: ' +  self.shop_list[rnd1] + ', ' + self.shop_list[rnd2])
        
    def shoptypes(self, sentence):
        rnd1 = random.randint(0,len(self.shop_type_list)-1)
        rnd2 = random.randint(0,len(self.shop_type_list)-1)
        while rnd1 == rnd2:
            rnd2 = random.randint(0,len(self.shop_type_list)-1)
        print('For example you can find these types of shops: ' +  self.shop_type_list[rnd1] + ', ' + self.shop_type_list[rnd2])
        self.speak('For example you can find these types of shops: ' +  self.shop_type_list[rnd1] + ', ' + self.shop_type_list[rnd2])
        
    def shoppresence(self, sentence):
        result = self.parser.parse(sentence)
        complobj = result['dobj']
        print(complobj)
        if (complobj in self.shop_list) or (complobj in self.shop_type_list):
            print("Yes, you can find " + complobj + ' in our mall!')
            self.speak("Yes, you can find " + complobj + ' in our mall!')
        else:
            rnd1 = random.randint(0,len(self.shop_type_list)-1)
            rnd2 = random.randint(0,len(self.shop_type_list)-1)
            while rnd1 == rnd2:
                rnd2 = random.randint(0,len(self.shop_type_list)-1)
            print("No, I'm really sorry about this. But you can find some other very interesting shops like: "+  self.shop_type_list[rnd1] + ', ' + self.shop_type_list[rnd2])
            self.speak("No, I'm really sorry about this. But you can find some other very interesting shops like: "+  self.shop_type_list[rnd1] + ', ' + self.shop_type_list[rnd2])
    
    def help(self, sentence):
        self.speak("How can I help you?")
        
    def goodbye(self, sentence):
        answers = ["See you later", "Have a nice day", "Bye!", "Bye! Come back again"]
        choice = random.randint(0,3)
        self.speak(answers[choice])
        
    def thanks(self, sentence):
        answers = ["Happy to help!", "Any time!", "My pleasure", "You're most welcome!"]
        choice = random.randint(0,3)
        self.speak(answers[choice])
        
        
    def findcities(self, children, prep):
        city = None
        if prep in children:
            try:
                city = children[prep][0]
            except:
                return city
        return city
    

    def flight(self, sentence):
        dependencies, children= self.parser.parse(sentence)
        departure = self.findcities(children, 'from')
        destination = self.findcities(children, 'to')
        while departure is None:
            self.speak("from where do you want to leave?")
            guess = self.hear()
            entities = self.parser.entities(guess["transcription"])
            print(entities)
            try:
                departure = entities["GPE"]
            except:
                departure = None
            
        while destination is None:
            self.speak("where do you want to go?")
            guess = self.hear()
            entities = self.parser.entities(guess["transcription"])
            try:
                destination = entities["GPE"]
            except:
                destination = None
            
        if 'for' in children:
            when = children['for'][0]
        else:    
            self.speak("when do you want to leave?")
            guess = self.hear()
            when = guess["transcription"]
            
        return departure, destination, when
        
    def flightconf(self, departure, destination, when):
        guess = self.hear()
        conf = guess["transcription"]
        conf = conf.lower()
        print(conf)
        words = self.parser.words(conf)
        print(words)
        if "no" in words:
            self.speak("okay, I'm here for you when you want")
        elif "yes" in words:
            self.speak("okay, I'm booking a flight for you from " + str(departure) + " to " + str(destination) + " for " + str(when))
        else:
            self.speak("I did not get it, sorry, can you please repeat?")
            self.flightconf(departure, destination, when)
        
        
    def flightbooking(self, sentence):
        departure, destination, when = self.flight(sentence)
        self.speak("I'm booking a flight for you from " + str(departure) + " to " + str(destination) + " for " + str(when) + ". Do you want to confirm it?")
        self.flightconf(departure, destination, when)
    
    def flightinfo(self, sentence):
        randomprice = random.randint(20,400)
        randomtime = random. randint(8, 22)
        randomexistence = random.randint(0,1)
        
        if randomexistence == 0:
            self.speak("No, I'm really sorry about this, try asking me for another day!")
        else:
            departure, destination, when = self.flight(sentence)
            self.speak("Yes, there is a flight from " + str(departure) + " to " + str(destination) + " for " + str(when) + ". It's cost is " + str(randomprice) + "euros " +\
            "and it leaves at " + str(randomtime) + "o'clock. Do you want me to book it for you?")
            self.flightconf(departure, destination, when)

    
    def yes(self, sentence):
        self.speak("Okay! Done")
        
    def no(self, sentence):
        self.speak("I'm here for you when you want!")
        
    def notunderstood(self):
        self.speak("I have not understood, can you please repeat?")
        
if __name__ == "__main__":
    PROMPT_LIMIT = 5
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    guess = hear()
    

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(guess["transcription"])

    for chunk in doc.noun_chunks:
        print(chunk.text, chunk.root.text, chunk.root.dep_,
                chunk.root.head.text)
        if chunk.root.dep_ == "dobj":
            objcompl = chunk.root.text
        print('\n')
    
    print('\n\n')
        
    for token in doc:
        print(token.text, token.dep_, token.head.text, token.head.pos_,
                [child for child in token.children])
        if str(token) == "order":
            verb = "order"
        print('\n')
        
    my_text = "What kind of " + objcompl + "do you want to " + verb
