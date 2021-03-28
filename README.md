# ChatBot

I have realized a chatbot that performs the task of helping people in a generic airport of London. It has some useful functionalities solving typical situations and problems. To use it, just download the repository and run the "chat.py" file.

## Technologies used
The structure of the program can be divided in four main parts:
- A class entirely dedicated to the agent, in which I handle the recognition of my speech, the speaking of the agent and the dialogue management
  - The speech recognition is done through the use of the *SpeechRecognition* library provided by python.
  - The speaking of the agent is instead implemented thanks to the *Google TextToSpeech* library.
  - All the other methods that handle the dialogues are implemented with python code.
  - Some other useful libraries I have used are: numpy, random, os.
- A class devoted to the text analysis implemented using the spacy library.
- The brain of the agent, the language understanding, is made with a neural network realized with *Tensorflow* and *Keras*. The input of the network is written in JSON format.
The model, the label encoder and the tokenizer are saved thanks to the *pickle* library
- Last, the management of the conversation turns is done in one last file.

## Language understanding (LU)
As anticipated, the understanding of the user sentences is done with a neural network.
Its input is a JSON file in which are defined some intents, composed by a tag representing the name of the intent and a list of patterns, i.e. some possible ways of saying sentences belonging to that tag.

After training the network on a dataset built in this way, with a total amount of more than ten different tags with a relatively small number of patterns as example each, it becomes able to map a given sentence to one of the tags with a certain confidence. 
For each tag I have defined a method in the agent class, handling that particular situation.
It is important to underline that the tag and the respective method to handle that situation must have the same name, in such a way it is possible to call the agent’s method starting from the tag predicted by the network, using the *getattribute* method, which takes as parameter the exact name of the attribute of the given class that we want to obtain.

## Preprocessing
The first step has been iterating on the two JSON files containing the training set and the validation set, saving in a list the example sentences contained in the dataset and in another list the corresponding label of each sentence. 
Simultaneously all the labels names are collected in a list without duplicates.
Then the data has been preprocessed to adapt their format to the one requested from the network. In particular:
- Since the output of the network cannot be a string value, the labels have been encoded in integer values in range 0 and num-classes -1.
- In addition to this, to obtain a numerical version of the sentences (as requested by the network), represented by a different numerical value for each word, all the sentences have been tokenized through to the keras Tokenizer.
Since each sentence has a different length, to obtain sequences all of the same length they have been padded to a fixed dimension.
At this point the preprocessing of the data is complete and they are given to the network.

## Network structure
As said before, the brain of the agent is realized with a small neural network.
Below a brief explanation of the structure of the network:
- The first layer is an Embedding layer. Practically it maps each tokenized word to a vector which describes the features of the word. Words having similar semantic meaning are mapped to similar vectors
- Below there are three convolutional layers that work in parallel. Each one having a different dimension of the filters. This is because the dimension defines the number of words that are analyzed together for extracting features and it is important to do this not only on one word per time or only on groups of words but both the things. In this way the network is able to recognize both key words and sentences structure.
Then, the outputs of these layers are concatenated.
- Two other layers for feature extraction that are put below are:
  - GlobalMaxPooling1D
  - Dense layer with 32 neurons
- The last layer is a dense layer with a number of neurons equal to the number of classes, with a SoftMax activation function. It implements the real final classification.
The output of the network, thanks to the *SoftMax* activation function used on the last layer, is the probability value of being the right class associated to each class.
The final prediction of the network is the tag with the highest probability.

## Text-To-Speech and Speech-To-Text
As said before these two fundamental parts of the project are done using respectively the Google Text To Speech and the Speech Recognition libraries.
1. In the first case I have defined a method in the agent class called “speak”, that given a certain sentence uses the gTTS library to save the speaking version of the textual sentence provided in an mp3 file. Then using built-in python library os I execute the file reproducing the audio.
2. For the speech to text, I have used the library to access the microphone of my pc and from it capturing the audio. The function returns a dictionary with three keys:
  - Transcription, which has as value the textual version of what has been said in the microphone
  - Error, which has as value string explaining, if any occurred, the error.
  - Success, which is True by default and becomes False if there has been an error
  
## Speech Parsing
A fundamental step in handling the different situations has been the parsing of the sentences with the spacy library. Thanks to this library it is possible to extract important information about the sentence and the words of which it is composed to be used in the assistant answers.
In particular I have used mainly two of the functionalities offered by the library:
- The dependency parsing, thanks to which it is possible to obtain the dependencies between words. The parsing is done starting from building a dependency tree showing the links between words, and thanks to the library it is possible to navigate the tree in various ways.
- The name entity recognition, thanks to which it is possible to detect the presence of words or groups of words belonging to some particular fields (geopolitical entities like countries or cities, money, time, date...)
The first feature has been very useful to extract from the sentences some particular words depending on their role in the sentence. For example:
- One of the functionalities of my chatbot allow the user to ask if a certain item is sold somewhere in the airport. In general, the item is the direct object of the sentence, and exploiting this feature it is possible to extract it from the sentence and use it to construct the answer.
The second feature has been useful too, to extract name of cities or dates from the sentence. I have exploited it also to check, for example, if the answer to the “where do you want to go” question is actually a city and not something else.

## Functionalities
It is possible to interact with the agent in the following situations:
- Greetings
- Thanks
- Request of help. The agent will answer you asking you how it can help you.
- Complaints. The agent will answer asking you to communicate it to the management. It will also thank you for the communication.
- Question about the possibility of buying an asked item somewhere in the airport.
- Request of booking a flight. The agent will answer you asking where do you want to go and when do you want to leave. If in the given date there is a flight available for the specified destination, the agent will tell you the time of the leaving and the flight price. Then, it asks you if you definitively want to confirm the booking, and after your confirmation asks you the name in which it should make the reservation.
- Question about the status of a flight given its code. The agent will answer telling you if the specified flight is in time, cancelled or delayed.
- Question about the gate of a flight given its code.
- Question about the terminal of a flight given its code
- Question about services for disable people offered by the airport. The agent will list you some possible services offered and asks you if you are interested in one of them and when do you need it.
- Question about the possibility of renting a car for transfer from the airport.
- Request of suggestion about a possible hotel near the airport.
