import random
import time
import os 
import string
from gtts import gTTS 
import speech_recognition as sr
import spacy
from SpeechParser import Parser
import numpy as np


'''
{"tag": "shoppresence",
	"patterns": ["Can I find a supermarket in the airport", "can I find some electronic shops here", "can I find an Armani store in the airport", 
	"is there a GameStop here", "is there an hairdresser in the airport", "is there a cafe", "Are there any restaurants", 
	"are there any videogames stores here", "are there any clothes shops in the airport"]
	},
    
	{"tag": "shoppresence",
	"patterns": ["is it possible to find a supermarket", "can I find here a toy store", "is there any Gucci store in the airport"]
	},
'''

class Bea():

    def __init__(self, recognizer, microphone, limit):
        self.shop_types = ["souvenir stores", "supermarket duty free", "luxury shops", "restaurants", "cafes"]
        self.shop_list = ['mediaworld', 'nike', 'adidas', 'mcdonald']
        self.shop_type_list = ['electronic', 'restaurant', 'clothes', 'cafe', 'hairdresser', 'supermarket']
        self.cities = ["Rome", "Berlin", "Amsterdam", "Dublin", "Madrid", "Milan", "Dublin", "Helsinki", "Oslo", "New York", "Los Angeles"]
        self.items = ["souvenir", "toy", "clothes", "magnet", "perfume", "pizza", "sandwich", "charger"]
        self.shops = [["London souvenirs", "Souvenirs from England", "U.K. souvenirs"], ["Game Stop", "Toys U.K"], \
                    ["Burberry", "Gucci", "Fendi"], ["London souvenirs", "Magnets Love", "U.K. souvenirs"], ["duty free"], ["pizza hut", "italy pizza"],\
                    ["super sandwich", "subway"], ["mediaworld", "euronics"]]
        self.car_models = ["luxury car"," mini van","utilitarian car"]
        self.items2shops = dict(zip(self.items, self.shops))
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
            #print("I didn't catch that. What did you say?\n")

            # if there was an error, stop the game
            if guess["error"]:
                #print("ERROR: {}".format(guess["error"]))
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
        self.speak("Hi, I'm the London's airport vocal assistent. I'm ready to help you, tell me what you need")
        return True
    
    def help(self, sentence):
        self.speak("How can I help you?")
        return True
        
    def goodbye(self, sentence):
        answers = ["See you later", "Have a nice day", "Bye!", "Bye! Come back again"]
        choice = random.randint(0,len(answers)-1)
        self.speak(answers[choice])
        return False
        
    def thanks(self, sentence):
        answers = ["Happy to help!", "Any time!", "My pleasure", "You're most welcome!"]
        choice = random.randint(0,len(answers)-1)
        self.speak(answers[choice])
        return False
    
    def complaint(self, sentence):
        answers = ["Please provide your complaint to the management to help them improving our services", 
        "Please mention your complaint to the management, they will be able to assist you"]
        choice = random.randint(0,len(answers)-1)
        self.speak(answers[choice])
        return False
        
    '''
    def shoppresence(self, sentence):
        complobj = None
        chunks = self.parser.noun_chunks(sentence)
        complobj = chunks['dobj'] if 'dobj' in chunks.keys() else chunks['attr']
        while complobj is None:
            self.speak("I've not understood. Please repeat.")
            guess = self.hear()
            sentence = guess["transcription"]
            chunks = self.parser.noun_chunks(sentence)
            complobj = chunks['dobj'] if 'dobj' in chunks.keys() else chunks['attr']
        
        complobj = complobj.lower()
        here = False
        for string in self.shop_list:
            if complobj in string or string in complobj:
                complobj = string
                here = True
        if not here:
            for string in self.shop_type_list:
                if complobj in string or string in complobj:
                    complobj = string
                    here = True
        if here:
            self.speak("Yes, you can find " + complobj + ' in our airport!')
        else:
            rnd1 = random.randint(0,len(self.shop_type_list)-1)
            rnd2 = random.randint(0,len(self.shop_type_list)-1)
            while rnd1 == rnd2:
                rnd2 = random.randint(0,len(self.shop_type_list)-1)
            self.speak("No, I'm really sorry about this. But you can find some other very interesting shops like: "+  self.shop_type_list[rnd1] + ', ' + self.shop_type_list[rnd2])
        return True  
    '''    
    
    def buildgatecode(self):
        letter = random.choice(string.ascii_letters)
        number = random.randint(10, 99)
        return letter + str(number)
    
    def checkflightcode(self, code):
        if len(code) is not 6:
            return False
        else:
            for i in range(len(code)):
                if i is 1 or i is 0:
                    if not code[i].isalpha():
                        return False
                else:
                    if not code[i].isdigit:
                        return False
        return True
        
    def flightgate(self, sentence):
        self.speak("To avoid any mistake looking for the gate of your flight, please tell me only the code of your flight with clear voice")
        guess = self.hear()["transcription"]
        isValid = False
        while guess is None or not isValid:
            self.speak("I've not understood. Please repeat")
            guess = self.hear()
            guess = guess["transcription"]
            if self.checkflightcode(guess):
                isValid = True
            else:
                self.speak("That is not a valid code. Try again please.")
        code = guess.lower()
        gatecode = self.buildgatecode()
        self.speak("The gate of your flight " + code.replace(" ", "") + "is " + gatecode)
        return True
       
    def flightcheckin(self,sentence):
        self.speak("To avoid any mistake looking for the terminal of your flight, please tell me only the code of your flight with clear voice")
        guess = self.hear()["transcription"]
        isValid = False
        while guess is None or not isValid:
            self.speak("I've not understood. Please repeat")
            guess = self.hear()
            guess = guess["transcription"]
            if self.checkflightcode(guess):
                isValid = True
            else:
                self.speak("That is not a valid code. Try again please.")
        code = guess.lower()
        terminalnum = random.randint(1, 10)
        self.speak("The terminal for your flight " + code.replace(" ", "") + " is the number " + str(terminalnum) +". There you can check in for the flight. Enjoy it.")
        return True
        
    def flightinfo(self, sentence):
        self.speak("To avoid any mistake looking for the status of your flight, please tell me only the code of your flight with clear voice")
        guess = self.hear()["transcription"]
        isValid = False
        while guess is None or not isValid:
            self.speak("I've not understood. Please repeat")
            guess = self.hear()
            guess = guess["transcription"]
            if self.checkflightcode(guess):
                isValid = True
            else:
                self.speak("That is not a valid code. Try again please.")
        code = guess.lower()
        
        rnd1 = random.randint(0,len(self.cities)-1)
        '''
        rnd2 = random.randint(0,len(self.shop_type_list)-1)
        while rnd1 == rnd2:
            rnd2 = random.randint(0,len(self.shop_type_list)-1)
        departure = self.cities[rnd1]
        '''
        destination = self.cities[rnd1]
        
        delays = ["15 minutes", "30 minutes", "1 hour", "2 hours", "4 hours"]
        status = ["in time", "cancelled", "delayed"]
        rnd = random.randint(0,len(status)-1)
        rndstatus = status[rnd]
        
        randomtime = random. randint(8, 22)
        
        #s = "Your flight with code " + code.replace(" ", "") + "from " + departure + " to " + destination +"is " + rndstatus
        s = "Your flight with code " + code.replace(" ", "") + " to " + destination +"is " + rndstatus
        
        if rndstatus == "delayed":
            rnd = random.randint(0,len(delays)-1)
            rnddelay = delays[rnd]
            statussentence = " of " + rnddelay + " .I'm sorry"
        elif rndstatus == "in time":
            statussentence = " .So it will leave at " + str(randomtime) + "o'clock."
        else:
            statussentence = " I'm really sorry about this."
            
        self.speak(s+statussentence)
        return True
    
    def findcities(self, children, entities, prep):
        city = None
        print(children)
        print(entities)
        if prep in children:
            try:
                for word in children[prep]:
                    if str(word) in entities['GPE']:
                        city = word
                if city is None:
                    city = entities['GPE'][0]
            except:
                return city
        return city
    
    def book_name(self):
        self.speak("In what name should I make the reservation?")
        guess = None
        guess = self.hear()["transcription"]
        while guess is None:
            self.speak("I've not understood. Please repeat")
            guess = self.hear()
            guess = guess["transcription"]
        
        return guess
    
    def flightconf(self, destination, when):
        conf = self.hear()["transcription"]
        while conf is None:
            self.speak("I've not understood. Please repeat")
            guess = self.hear()
            conf = guess["transcription"]
        conf = conf.lower()
        words = self.parser.words(conf)
        if "no" in words:
            self.speak("okay, I'm here for you when you want")
        elif "yes" in words:
            name = self.book_name()
            #self.speak("okay, I'm booking a flight for you from " + str(departure) + " to " + str(destination) + " for " + str(when))
            self.speak("okay, I'm booking a flight for you to" + str(destination) + "for" + str(when) + "in name" + name)
        else:
            self.speak("I did not get it, sorry, can you please repeat?")
            #self.flightconf(departure, destination, when)
            self.flightconf(destination, when)
    
    def flight(self, sentence):
        children = self.parser.parse(sentence)
        entities = self.parser.entities(sentence)
        #departure = self.findcities(children, entities, 'from')
        destination = self.findcities(children, entities,'to')
        while destination is None:
            self.speak("where do you want to go?")
            guess = self.hear()
            try:
                ent = self.parser.entities(guess["transcription"])
                destination = ent["GPE"]
            except:
                destination = None

        if 'DATE' in entities.keys():
            when = entities["DATE"]
        else:    
            self.speak("when do you want to leave?")
            guess = self.hear()["transcription"]
            while guess is None:
                self.speak("I've not understood. Please repeat")
                guess = self.hear()
                guess = guess["transcription"]
                try:
                    ent = self.parser.entities(guess)
                    guess = ent["DATE"]
                except: 
                    guess = None
            when = guess
         
        #return departure, destination, when
        return destination, when
        
    def flightbooking(self, sentence):
        randomprice = random.randint(20,400)
        randomtime = random. randint(8, 22)
        randomexistence = random.randint(0,1)
        
        #departure, destination, when = self.flight(sentence)
        destination, when = self.flight(sentence)
        while randomexistence == 0:
            self.speak("I'm really sorry about this, but there are no flights to" + str(destination) + str(when) + "try asking me for another date")
            guess = self.hear()["transcription"]
            while guess is None:
                self.speak("I've not understood. Please repeat")
                guess = self.hear()
                guess = guess["transcription"]
                try:
                    ent = self.parser.entities(guess)
                    guess = ent["DATE"]
                except: 
                    guess = None
            when = guess
            randomexistence = random.randint(0,1)
        #self.speak("Yes, there is a flight from " + str(departure) + " to " + str(destination) + " for " + str(when) + ". It's cost is " + str(randomprice) + "euros " +\
        self.speak("Yes, there is a flight to" + str(destination) + "for" + str(when) + ". It's cost is " + str(randomprice) + "euros " +\
        "and it leaves at" + str(randomtime) + "o'clock. Do you want me to book it for you?")
        #self.flightconf(departure, destination, when)
        self.flightconf(destination, when)
        return True
        
    def disablepeople(self, sentence):
        self.speak("Dear customer, we offer any kind of assistance for people with disabilities. \
        The airport offers assistance for any displacement in the airport, help for flights information and for luggage displacement\
        . Which kind of assistance do you need?")
        guess = self.hear()["transcription"]
        while guess is None:
            self.speak("I've not understood. Please repeat")
            guess = self.hear()
            guess = guess["transcription"]
        assistance_needed = guess
        self.speak("When do you need it?")
        guess = self.hear()["transcription"]
        while guess is None:
            self.speak("I've not understood. Please repeat")
            guess = self.hear()
            guess = guess["transcription"]
            try:
                ent = self.parser.entities(guess)
                guess = ent["DATE"][0]
            except: 
                guess = None
        when = guess
        self.speak("Perfect, one of our dependents will be available for you" + when + "for the assistance service you have chosen: "+ assistance_needed)
        return True
    
    def getItem(self, chunks):
        item = None
        try:
            item = chunks['dobj'] if 'dobj' in chunks.keys() else None
        except:
            return None
        return item
    
    def wheretobuy(self, sentence):
        chunks = self.parser.noun_chunks(sentence)
        item = self.getItem(chunks)
        guess = None
        
        while item is None:
            while guess is None:
                self.speak("I've not understood. Please, tell me what you want to buy.")
                guess = self.hear()
                guess = guess["transcription"]
            item = self.getItem(self.parser.noun_chunks(guess))
        
        soldhere = False 
        
        for string in self.items:
            if string in item or item in string:
                soldhere = True
                break
            
        if soldhere:
            str = ""
            for i in self.items2shops[string]:
                str = str + i
                str = str + ", "
            self.speak("You can buy " + item + "in the following shops: "+ str)
            
        else:
            self.speak("I'm really sorry, there are no shops selling what you are looking for")
        return True
    
    def rentacar(self,sentence):
        self.speak("Yes, the followings are the models we have available: luxury car, mini van, utilitarian car. Which one are you interested in?")
        guess = self.hear()["transcription"]
        while guess is None or guess not in self.car_models:
            self.speak("I've not understood. Please repeat")
            guess = self.hear()
            guess = guess["transcription"]
            if guess not in self.car_models:
                self.speak("this model is not available, sorry, try with another one")
        car_model = guess
        isValid = False
        self.speak("For how many days do you need it?. Please specify the exact number of days")
        guess = self.hear()["transcription"]
        while guess is None:
            self.speak("I've not understood. Please repeat")
            guess = self.hear()
            guess = guess["transcription"]
            try:
                ent = self.parser.entities(guess)
                guess = ent["DATE"][0]
            except: 
                guess = None
        num_days = guess
        
        self.speak("Ok, you have rent a" + car_model + "for "+ num_days)
        return True

    def bookhotel(self, sentence):
        self.speak("I can suggest you a wonderful hotel near the airport. The Royal hotel. Do you want me to book a room there for you?")
        guess = self.hear()["transcription"]
        while guess is None:
            self.speak("I've not understood. Please repeat")
            guess = self.hear()
            guess = guess["transcription"]
        confirm = guess
        if "yes" in confirm or "Yes" in confirm:
            self.speak("For how many days do you need it?. Please specify the exact number of days")
            guess = self.hear()["transcription"]
            while guess is None:
                self.speak("I've not understood. Please repeat")
                guess = self.hear()
                guess = guess["transcription"]
                try:
                    ent = self.parser.entities(guess)
                    guess = ent["DATE"][0]
                except: 
                    guess = None
            num_days = guess
            
            name = self.book_name()
            self.speak("Ok, I have booked for you a room in the Royal hotel for" + num_days + "in name" + name)
        else:
            self.speak("Ok, I'm here for you when you want")
        return True
        
    def yes(self, sentence):
        self.speak("Okay! Done")
        
    def no(self, sentence):
        self.speak("I'm here for you when you want!")
        
    def notunderstood(self):
        self.speak("I have not understood, can you please repeat?")