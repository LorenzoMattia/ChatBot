import random
import time
import os 
import string
from gtts import gTTS 
import speech_recognition as sr
import spacy
from SpeechParser import Parser
import numpy as np


class BeaNew():

    def __init__(self, recognizer, microphone, limit):
        self.shop_types = ["souvenir stores", "supermarket duty free", "luxury shops", "restaurants", "cafes"]
        self.shop_list = ['mediaworld', 'nike', 'adidas', 'mcdonald']
        self.shop_type_list = ['electronic', 'restaurant', 'clothes', 'cafe', 'hairdresser', 'supermarket']
        self.cities = ["Rome", "Berlin", "Amsterdam", "Dublin", "Madrid", "Milan", "Dublin", "Helsinki", "Oslo", "New York", "Los Angeles"]
        self.items = ["souvenir", "toy", "clothes", "magnet", "perfume", "pizza", "sandwich", "charger"]
        self.shops = [["London souvenirs", "Souvenirs from England", "U.K. souvenirs"], ["Game Stop", "Toys U.K"], \
                    ["Burberry", "Gucci", "Fendi"], ["London souvenirs", "Magnets Love", "U.K. souvenirs"], ["duty free"], ["pizza hut", "italy pizza"],\
                    ["super sandwich", "subway"], ["mediaworld", "euronics"]]
        self.car_models = ["luxury car","utilitarian car"]
        self.items2shops = dict(zip(self.items, self.shops))
        self.recognizer = recognizer
        self.microphone = microphone
        self.limit = limit
        self.parser = Parser()
        
    def recognize_speech_from_mic(self, recognizer, microphone):
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        try:
            response["transcription"] = recognizer.recognize_google(audio)
        except sr.RequestError:
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            response["error"] = "Unable to recognize speech"
        #print(response)
        return response["transcription"]
        
    def hear(self):
        guess = self.recognize_speech_from_mic(self.recognizer, self.microphone)
        #print(guess)
        while guess is None:
            print('Speak!')
            self.speak("I've not understood, please repeat or tell me stop to end the conversation")
            guess = self.recognize_speech_from_mic(self.recognizer, self.microphone)
        # show the user the transcription
        print("You said: {}".format(guess))
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
    
    def hereforyou(self):
        self.speak("okay, I'm here for you when you want")
        return True
        
    def buildgatecode(self):
        letter = random.choice(string.ascii_letters)
        number = random.randint(10, 99)
        return letter + str(number)
    
    def checkflightcode(self, code):
        code = code.replace(" ", "")
        if code is None:
            return False
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
        guess = self.hear()
        if guess == "stop" or "stop" in guess:
            return self.hereforyou()
        isValid = self.checkflightcode(guess)
        while not isValid:
            self.speak("There is a problem with the code, try again")
            guess = self.hear()
            if guess == "stop" or "stop" in guess:
                return self.hereforyou()
            if self.checkflightcode(guess):
                isValid = True
        code = guess.lower()
        gatecode = self.buildgatecode()
        self.speak("The gate of your flight " + code.replace(" ", "") + "is " + gatecode)
        return True
       
    def flightcheckin(self,sentence):
        self.speak("To avoid any mistake looking for the terminal of your flight, please tell me only the code of your flight with clear voice")
        guess = self.hear()
        if guess == "stop" or "stop" in guess:
            return self.hereforyou()
        isValid = self.checkflightcode(guess)
        while not isValid:
            self.speak("There is a problem with the code, try again")
            guess = self.hear()
            if guess == "stop" or "stop" in guess:
                return self.hereforyou()
            if self.checkflightcode(guess):
                isValid = True
        code = guess.lower()
        terminalnum = random.randint(1, 10)
        self.speak("The terminal for your flight " + code.replace(" ", "") + " is the number " + str(terminalnum) +". There you can check in for the flight. Enjoy it.")
        return True
        
    def flightinfo(self, sentence):
        self.speak("To avoid any mistake looking for the status of your flight, please tell me only the code of your flight with clear voice")
        guess = self.hear()
        if guess == "stop" or "stop" in guess:
            return self.hereforyou()
        isValid = self.checkflightcode(guess)
        while not isValid:
            self.speak("There is a problem with the code, try again")
            guess = self.hear()
            if guess == "stop" or "stop" in guess:
                return self.hereforyou()
            if self.checkflightcode(guess):
                isValid = True
        code = guess.lower()
        
        ent = self.parser.entities(sentence)
        if 'GPE' in ent.keys():
            destination = ent['GPE'][0]
        else:
            rnd1 = random.randint(0,len(self.cities)-1)
            destination = self.cities[rnd1]
        
        delays = ["15 minutes", "30 minutes", "1 hour", "2 hours", "4 hours"]
        status = ["in time", "cancelled", "delayed"]
        rnd = random.randint(0,len(status)-1)
        rndstatus = status[rnd]
        
        #randomtime = random. randint(8, 22)
        
        s = "Your flight with code " + code.replace(" ", "") + " to " + destination +"is " + rndstatus
        
        if rndstatus == "delayed":
            rnd = random.randint(0,len(delays)-1)
            rnddelay = delays[rnd]
            statussentence = " of " + rnddelay + " .I'm sorry"
        elif rndstatus == "in time":
            statussentence = " .So it will leave at the scheduled time"
        else:
            statussentence = " I'm really sorry about this."
            
        self.speak(s+statussentence)
        return True
    
    def findcities(self, children, entities, prep):
        city = None
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
        guess = self.hear()
        return guess
    
    def flightconf(self, destination, when):
        conf = self.hear()
        conf = conf.lower()
        words = self.parser.words(conf)
        if "no" in words:
            self.speak("okay, I'm here for you when you want")
        elif "yes" in words:
            name = self.book_name()
            self.speak("okay, I'm booking a flight for you to" + str(destination) + "for" + str(when) + "in name" + name)
        else:
            self.speak("I'm not sure about your confirmation, try again")
            self.flightconf(destination, when)
    
    def extract_entity(self, sentence, label):
        try:
            ent = self.parser.entities(sentence)
            guess = ent[label][0]
        except:
            guess = None
        return guess
    
    def flight(self, sentence):
        children = self.parser.parse(sentence)
        entities = self.parser.entities(sentence)
        #departure = self.findcities(children, entities, 'from')
        destination = self.findcities(children, entities,'to')
        
        while destination is None:
            self.speak("invalid destination, try again")
            guess = self.hear()
            if guess == "stop" or "stop" in guess:
                return "stop", "stop"
            destination = self.extract_entity(guess, "GPE")

        if 'DATE' in entities.keys():
            when = entities["DATE"][0]
        else:    
            self.speak("when do you want to leave?")
            guess = self.hear()["transcription"]
            date = self.extract_entity(guess, "DATE")
            while date is None:
                guess = self.hear()
                if guess == "stop" or "stop" in guess:
                    return "stop", "stop"
                date = self.extract_entity(guess, "DATE")
            when = date
        return destination, when
        
    def flightbooking(self, sentence):
        randomprice = random.randint(20,400)
        randomtime = random. randint(8, 22)
        randomexistence = random.randint(0,1)
        #randomexistence = 0
        destination, when = self.flight(sentence)
        
        if str(destination) == "stop" and str(when) == "stop":
            return self.hereforyou()
            
        while randomexistence == 0:
            self.speak("I'm really sorry about this, but there are no flights to" + str(destination) + str(when) + ", try asking me for another date or tell me stop to end the research")
            guess = self.hear()
            if guess == "stop" or "stop" in guess:
                return self.hereforyou()
            date = self.extract_entity(guess, "DATE")
            while date is None:
                guess = self.hear()
                if guess == "stop" or "stop" in guess:
                    return self.hereforyou()
                date = self.extract_entity(guess, "DATE")
            when = date
            randomexistence = random.randint(0,1)
        self.speak("Yes, there is a flight to" + str(destination) + "for" + str(when) + ". It's cost is " + str(randomprice) + "euros " +\
        "and it leaves at" + str(randomtime) + "o'clock. Do you want me to book it for you?")
        self.flightconf(destination, when)
        return True
        
    def disablepeople(self, sentence):
        self.speak("Dear customer, we offer any kind of assistance for people with disabilities: \
        support to get around into the airport, help for flights information and for luggage displacement\
        . Which kind of assistance do you need?")
        guess = self.hear()
        
        if guess == "stop" or "stop" in guess:
            return self.hereforyou()
        assistance_needed = guess
        
        self.speak("When do you need it?")
        guess = self.hear()
        date = self.extract_entity(guess, "DATE")
        while date is None:
            guess = self.hear()
            if guess == "stop" or "stop" in guess:
                return self.hereforyou()
            date = self.extract_entity(guess, "DATE")
        when = date
        self.speak("Perfect, one of our dependents will be available for you" + when + "for the assistance service you have chosen: "+ assistance_needed)
        return True
    
    def getItem(self, chunks):
        item = None
        try:
            item = chunks['dobj'] if 'dobj' in chunks.keys() else None
            if item is None:
                self.speak("what do you want to buy?")
        except:
            return None
        return item
    
    def wheretobuy(self, sentence):
        chunks = self.parser.noun_chunks(sentence)
        item = self.getItem(chunks)
        while item is None:
            guess = self.hear()
            if guess == "stop" or "stop" in guess:
                return self.hereforyou()
            item = guess
        soldhere = False 
        
        for string in self.items:
            if string in item or item in string:
                item = string
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
        self.speak("Yes, the followings are the models we have available: luxury car, utilitarian car. Which one are you interested in?")
        guess = self.hear()
        if guess == "stop" or "stop" in guess:
            return self.hereforyou()
        while guess not in self.car_models:
            self.speak("There are some problem with your request, maybe I've not understood or the model you have asked for is not available. Try again or tell me stop to end the conversation")
            guess = self.hear()
            if guess == "stop" or "stop" in guess:
                return self.hereforyou()
        car_model = guess
        
        self.speak("For how many days do you need it?. Please specify the exact number of days")
        guess = self.hear()
        if guess == "stop" or "stop" in guess:
            return self.hereforyou()
        days = self.extract_entity(guess, "DATE")
        while days is None:
            guess = self.hear()
            if guess == "stop" or "stop" in guess:
                return self.hereforyou()
            days = self.extract_entity(guess, "DATE")
            if days is None:
                days = self.extract_entity(guess, "CARDINAL")
        num_days = days
        if not("day" in num_days or "days" in num_days):
            if num_days == "1" or "1" in num_days:
                num_days = num_days + " day"
            else:
                num_days = num_days + " days"
        name = self.book_name()
        self.speak("Ok, you have rent a" + car_model + "for "+ num_days + "in name" + name)
        return True

    def bookhotel(self, sentence):
        self.speak("I can suggest you a wonderful hotel near the airport. The Royal hotel. Do you want me to book a room there for you?")
        confirm = self.hear()
        
        if confirm == "stop" or "stop" in confim:
            return self.hereforyou()

        if "yes" in confirm or "Yes" in confirm:
            self.speak("For how many days do you need it?. Please specify the exact number of days")
            guess = self.hear()
            days = self.extract_entity(guess, "DATE")
            if days is None:
                days = self.extract_entity(guess, "CARDINAL")
            while days is None:
                guess = self.hear()
                if guess == "stop" or "stop" in guess:
                    return self.hereforyou()
                days = self.extract_entity(guess, "DATE")
                if days is None:
                    days = self.extract_entity(guess, "CARDINAL")
            num_days = days
            if not("day" in num_days or "days" in num_days):
                if num_days == "1" or "1" in num_days:
                    num_days = num_days + " day"
                else:
                    num_days = num_days + " days"
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