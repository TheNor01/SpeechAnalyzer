import speech_recognition as sr
import json
import os
from json import dumps
import pyaudio
from kafka import KafkaProducer
from rfc5654Language import RfcLanguage



import threading,time
WAIT_TIME_SECONDS = 1


import joblib

with open('user.txt', 'r') as file:
    data = file.read().split(' ')


#Informazioni
 #Nome
 #Compagnia (Topic)
 #Language (English, Italian, ecc...)

#print("MyLG")
#print(RfcLanguage[data[2]].value)


from MachineL.API import MLAPI
model = MLAPI()
from googletrans import Translator
translator = Translator()




r = sr.Recognizer()
#name = input("Benvenuto, digita il tuo nome per entrare: ")
#name = "turi"

name = data[0]
topic = data[1].lower()
myLanguage=RfcLanguage[data[2]].value

print("******")


def check_offline(text):
    list_pro = open('./python/bin/badwords.txt','r+')
    content = list_pro.read()
    list_content = content.split('\n')
    for word in list_content :
        if word in text :
            remplacement = "*" * len(word)
            text = text.replace(word ,remplacement)
    return text


def main():
    

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

        print("Comincia a parlare")

        audio = r.listen(source)
        #print(audio)
        print("elaboro il messaggio")

       # file = open("testo.txt","w+")

        try:
            text = r.recognize_google(audio,language=myLanguage)
            final_txt= (''.join(text)).lower()
            filter_text=check_offline(final_txt)

            scrString = myLanguage.split('-')[0]
            print(scrString)

            translated = translator.translate(filter_text, src=scrString,dest='en')
            print("Testo tradotto  : "+translated.text)
                 
            
            number = model.getPrediction(translated.text)
            print( " predetto : -- "+str(number))

            wordArray=translated.text.split(' ')
            #print(wordArray)
            #print("Passed split")

            #prefabs
            
            key="key"
            fieldname="name"
            topic = "topic"

            '''
            #approccio 1
            json_str='{"'+fieldname+'":"'+name+'" , "message" : [ '
            for word in wordArray[:-1]:

                print(date)
                tmp='{"'+key+'":"'+word+'"},'
                json_str+=tmp

            #date=datetime_Rome.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
            json_str+='{"'+key+'":"'+wordArray[-1]+'"}'
            json_str+=']}'
            

            #approccio 2
            json_str = ''
            for word in wordArray[:-1] :
                json_str += '{"' + name + '" : "' + word + '"}, '

            json_str += '{"' + name + '" : "' + wordArray[-1] + '"}'
            '''

            #approccio 3
            json_str='{"'+fieldname+'":"'+name+'" , "message" : "'
            for word in wordArray[:-1] :
                json_str += word + ' '
            json_str += wordArray[-1] +'","'+topic+'" : "'+str(number)+'","language" : "'+scrString+'"}'

            print(json_str)

            producer = KafkaProducer(bootstrap_servers=['192.168.1.28:9092'],
            value_serializer=lambda x: 
            dumps(x).encode('utf-8')
            )
            
            data = json_str

            producer.send('myTap',value=data)
           


            producer.flush()


        except Exception as e:
            print("Error : "+str(e))

ticker = threading.Event()
while not ticker.wait(WAIT_TIME_SECONDS):
    #print(os.getcwd())
    main()
