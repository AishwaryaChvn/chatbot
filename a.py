import streamlit as st
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

import tkinter
import tk
import _tkinter
from tkinter import *
from datetime import datetime




from tensorflow.keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


st.header('Welcome to Food Delivery Service')
nav = st.sidebar.radio("MENU",["Pizza-100/-","Burger-150/-","Sandwich-100/-","Cutlet-150/-","Idli-80/-","Dosa-100/-"])
st.image('image.jpg')



def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words
# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words) 
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list



def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(text):
    ints = predict_class(text, model)
    res = getResponse(ints, intents)
    return res

##Creating GUI with tkinter


#date time
now = datetime.now()
current_time = now.strftime("%D - %H:%M \n")

# send function: add entry to chat window and get chatbot response
def send():
    # get written message and save to variable
    msg = EntryBox.get("1.0",'end-1c').strip()
    # remove message from entry box
    EntryBox.delete("0.0",END)
    
    if msg == "Message":
        # if the user clicks send before entering their own message, "Message" gets inserted again
        # no prediction/response
        ChatLog.config(foreground="#0000CC", font=("Helvetica", 12))
        ChatLog.insert(END, current_time, ("small","right","colour"))
        EntryBox.insert(END, "Message")
        pass
        # if user clicks send and proper entry
    elif msg != '':
        # activate chat window and insert message
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, current_time, ("small","right","colour"))
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#0000CC", font=("Helvetica", 12))
        
        # insert bot response to chat window
        res = chatbot_response(msg)
        ChatLog.insert(END, current_time, ("small","right","colour"))
        ChatLog.insert(END, "Chatbot: " + res + '\n\n')
        
        # make window read-only again
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)

def clear_search(event):
    EntryBox.delete("0.0",END)
    EntryBox.config(foreground="black", font=("Verdana", 12))
    
base = Tk()
base.title("Chatbot")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)




#Chat window
ChatLog = Text(base, bd=0, height="8", width="50", font="Helvetica", wrap="word")
ChatLog.config(state=NORMAL)
ChatLog.tag_config("right", justify="left")
ChatLog.tag_config("small", font=("Helvetica", 7))
ChatLog.tag_config("colour", foreground="#333333")
ChatLog.insert(END, current_time, ("small","right","colour"))
ChatLog.insert(END, "Chatbot:Welcome to ABC Food Delivery Services\n\n")
ChatLog.insert(END,'\n')
ChatLog.config(foreground="#0000CC", font=("Helvetica", 9))



# disable window = read-only
ChatLog.config(state=DISABLED)

# bind scrollbar to ChatLog window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

# create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="9", height=5,
                    bd=0, bg="sky blue", activebackground="gold",fg='#ffffff',
                    command= send )


# Create the box to enter message
EntryBox = Text(base, bd=0, fg="#000000", bg="#fff5f5", highlightcolor="#750216",
                width="29", height="5", font=("Arial",10), wrap="word")

#Placeholder config and text:
Placeholder = Text(base, bd=0, fg="#A0A0A0", bg="#fff5f5", highlightcolor="#750216",
                   width="29", height="5", font=("Arial",10), wrap="word")
Placeholder.insert("1.0", "Ask a question")

# The following two functions are defined to add a placeholder text or to delete it.
def deletePlaceholder(event):
    Placeholder.place_forget()
    EntryBox.focus_set()


def addPlaceholder(event):
    if placeholderFlag == 1:
        Placeholder.place(x=6, y=421, height=70, width=265)



# place components at given coordinates in window (x=0 y=0 top left corner)
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=370)
EntryBox.place(x=6, y=401, height=90, width=265)
SendButton.place(x=282, y=401, height=90)
Placeholder.place(x=6, y=421, height=70, width=276)
Placeholder.bind("<FocusIn>", deletePlaceholder)
EntryBox.bind("<FocusOut>", addPlaceholder)

# Refresh GUI window every 0.1 seconds, mainly for the "SEND" button.
# If the entry box does not contain text --> 'Send' button is inactive, otherwise it's activated.

def update():
    global placeholderFlag
    if (EntryBox.get("1.0", 'end-1c').strip() == ''):
        SendButton['state'] = DISABLED
        placeholderFlag = 1
    elif EntryBox.get("1.0", 'end-1c').strip() != '':
        SendButton['state'] = ACTIVE
        placeholderFlag = 0
    base.after(100, update)


base.bind('<Return>', send)
update()



base.mainloop() 





