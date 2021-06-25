import pyttsx3
import speech_recognition as sr
import os
import subprocess
#from requests import request , session
#from pprint import pprint as pp
import json
import requests 
import datetime 
from datetime import date
import time
import calendar
import warnings
import random
import wikipedia
import webbrowser
from pywhatkit import sendwhatmsg_instantly
import smtplib
import sys
import pyjokes
import pyautogui
import PyPDF2
from tkinter.filedialog import *
import psutil
import speedtest
import wolframalpha

warnings.filterwarnings("ignore") #ignoring all the warnings

if sys.platform == "win32":
    engine=pyttsx3.init('sapi5')
    voices=engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
else:
    engine=pyttsx3.init('nsss')   #sapi5 - SAPI5 on Windows    #nsss - NSSpeechSynthesizer on Mac OS X     #espeak - eSpeak on every other platform
    voices=engine.getProperty('voices')
    #for i in range(48):
        #print(voices[i].id)
    engine.setProperty('voice',voices[10].id)#10b 17 26 28 37 39

def speak(audio): #fn for talking txt to spch,audio is string
    engine.say(audio)#say fn for speaking
    print(audio)
    engine.runAndWait()

def take_command():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print('Go ahead,I am listening....')
        #r.pause_threshold=1
        r.adjust_for_ambient_noise(source)
        audio=r.listen(source)
    try:
        print('Hold on a momment,Recognizing...')
        query=r.recognize_google(audio,language='en-in')
        print(f'User said:{query}\n')
    except:
        speak("There was some problem please try again")  
        return "None"
    return query

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am COSMOS. How may I help you")

def open_file(filename,filename1):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        try:
            opener = f'/Applications/{filename}.app/Contents/MacOS/{filename1}' 
            subprocess.call([opener]) 
        except:
            opener = f'/System/Applications/{filename}.app/Contents/MacOS/{filename1}' 
            subprocess.call([opener]) 

def sendEmail(to,content):
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.login("email","password")
    server.sendmail("email id",to,content)
    server.close()

def news():
    #https://newsapi.org/  ##get apikey from here
    api_key='Your api key here!!!'
    main_url = f'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey={api_key}'

    main_page = requests.get(main_url).json()
    # print(main_page)
    articles = main_page["articles"]
    # print(articles)
    head = []
    numbers=["first","second","third","fourth","fifth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range (len(numbers)):
        speak(f"today's {numbers[i]} news is: {head[i]}")

def crypto(slug):
    #https://coinmarketcap.com/  ##get apikey from here
    apiurl='https://pro-api.coinmarketcap.com'
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'Your api key here!!!',
    }

    session=requests.session()
    session.headers.update(headers)

    def coins_price(apiurl,slug):
        url=apiurl+'/v1/cryptocurrency/quotes/latest'
        parameters={'slug':slug}
        r=session.get(url,params=parameters)
        data=r.json()['data']
        all=str(data)
        x=all.find('price')
        all=all[x:x+20]
        for p in all.split():
            try: 
                float(p)
                price=p
            except:
                pass
        speak(f'{slug} price is {price}')
        return price
    
    #pp(coins_price(apiurl,slug))
    coins_price(apiurl,slug)

def weather():
    def loc():
        try:
            ipadd=requests.get("https://api.ipify.org").text
            url="https://get.geojs.io/v1/ip/geo/"+ipadd+".json"
            geo_requests= requests.get(url)
            geo_data=geo_requests.json()
            city=geo_data['city']
        except:
            city='delhi'
        return city

    #https://home.openweathermap.org/   ##get apikey from here
    api_key = 'Your api key here!!!'
    base_url = 'https://api.openweathermap.org/data/2.5/weather?'
    city_name = loc()
    url = base_url + "&q=" + city_name + "&appid=" + api_key 
    session=requests.session()
    r = session.get(url)
    data = r.json()
    #data
    if data["cod"] != "404":
        y = data["main"]
        current_temperature = y["temp"]
        current_humidiy = y["humidity"]
        z = data["weather"]
        weather_description = z[0]["description"]
        #print(" Temperature is " +str(int(current_temperature-273.15)) +" degree celcius\n humidity is " + str(current_humidiy) +"%\n description  " + str(weather_description))
        speak(" Temperature is " +str(int(current_temperature-273.15)) +" degree celcius\n humidity is " + str(current_humidiy) +"%\n with  " + str(weather_description)+'in '+city_name)
                    

def pdf_reader():
    book=askopenfilename()
    try: 
        pdfreader=PyPDF2.PdfFileReader(book)
        pages=pdfreader.numPages
        speak(f"Total numbers of pages in this pdf are {pages}")
        speak("sir please enter the page number you want me to read")
        pg=int(input("please enter the page number:"))
        for num in range(pg,pages):
            page=pdfreader.getPage(pg)
            text=page.extractText()
            speak(text)
    except :
        speak("Operation Cancelled !")        
            
def adv_search():
    query=input('Question: ')
    #https://products.wolframalpha.com/api/   ##get apikey from here
    app_id='Your api key here!!!'
    client=wolframalpha.Client(app_id)
    if 'no thanks' in query or 'thanks' in query or 'close advance search mode' in query:
        speak('closing advance search mode')
    else:
        res=client.query(query)
        ans=next(res.results).text
        speak(ans)
        speak('want to search anything else?')
        adv_search() 

def TaskExecution():

    # function for coin toss task
    def htLine1():
        speak("It's " + res)
    def htLine2():
        speak("You got " + res)
    def htLine3():
        speak("It landed on " + res)

    wish()
    bye=True
    while bye:

        query=take_command().lower()
        #query=input() ##comment above and remove this for typing instead of speaking for testing

        # Tasks
        if "what is your name" in query:
            speak('I am COSMOS your virtual assistant.')
            continue
        
        if "tell me about yourself" in query:
            speak('I am COSMOS your virtual assistant. What can I do for you?')
            continue

        elif 'why cosmos' in query or 'Why is your name cosmos' in query:
            speak("Just like cosmos is filled with endless possibilities this program also have endless possibilites and thats why cosmos")
            continue

        elif 'price of' in query or 'tell me the price of' in query:
            query=query.replace('tell me the price of ','')
            query=query.replace('price of ','')
            crypto(query)
            speak('need something else?')

        elif 'weather' in query:
            #query=query.replace('how is the weather in',' ')## can be made to take location ##not implemented
            #query=query.replace('weather in',' ')
            #query=query.replace('weather',' ')
            weather()
            speak('need something else?')

        elif "open notepad" in query:
            npath="C:\\WINDOWS\\system32\\notepad.exe"
            os.startfile(npath)

        elif "open command prompt" in query:
            os.system("start cmd") 
            bye=False 

        elif 'the time' in query:
            strTime=datetime.datetime.now().strftime('%H:%M')
            #print(f'its {strTime}')
            speak(f'its {strTime}')
            speak('you want me to do anything else?')

        elif "todays date" in query or "the date"in query:
            today = date.today()
            d2 = today.strftime("%B %d, %Y")
            speak(f"Today is {d2}") 
            speak('you want me to do anything else?')

        elif "ip address" in query:
            ip=requests.get('https://api.ipify.org').text#.text returns ip in unicode
            speak(f"Your IP Address is {ip}")
            speak('you want me to do anything else?')

        elif 'wikipedia' in query:
            speak('Searching in wikipedia')
            query=query.replace('wikipedia',' ')
            results=wikipedia.summary(query,sentences=2)
            speak('According to wikipedia')
            #print(results)
            speak(results)
            speak('you want me to do anything else')
            
        elif 'open google' in query:
            webbrowser.open("https://google.com")
            bye=False
        
        elif 'open youtube' in query:
            webbrowser.open('https://youtube.com')
            bye=False

        elif 'what is' in query:
            #query=query.replace('what is',' ')
            result=wikipedia.summary(query,sentences=2)
            #print(result)
            speak(result)
            speak('anything else?')
        
        elif 'search in youtube' in query or 'open in youtube' in query:      #search in youtube
            query=query.replace('search in youtube',' ')
            query=query.replace('open in youtube',' ')
            webbrowser.open(f'https://www.youtube.com/results?search_query={query}')
            speak(f'searchin in youtube {query}')
            bye=False

        #walframalpha
        elif 'advance search mode' in query or 'advanced search mode' in query:
            ##not gonna work by speaking input
            speak('Advance search mode activated')
            try:
                adv_search()
            except Exception as e:
                speak("Sorry,I am currently unable to find the answers.Please try again later")  
            speak('do you want me to do anything else?')    
            continue

        elif 'search' in query or 'search in google' in query or 'open in google' in query:         #search in google tab
            query=query.replace('search',' ')
            query=query.replace('search in google',' ')
            query=query.replace('open in google',' ')
            webbrowser.open(f"https://google.com/search?q={query}")
            speak(f'searching in google {query}')
            bye=False


        elif ("open gfg" in query or "open geeksforgeeks" in query):
            webbrowser.open("https://www.geeksforgeeks.org")
            bye=False

        elif "send message on whatsapp" in query or 'send message' in query:
            speak("To whom should I send a message")
            speak(" Please type the number ")
            no=input("Enter the number:")
            speak(" what should I send ?")
            speak('You will have to scan for whatsapp web.')
            subquery=take_command().lower()
            sendwhatmsg_instantly(f"+91{no}",f"{subquery}")
            bye=False

        elif "email" in query:
            try:
                speak("To whom do you want to send mail?")
                to=input("Enter the mail id to whom you want to send:")
                speak("what should i say?")
                subquery=take_command().lower()
                sendEmail(to,subquery)
                speak("Email has been sent.")
                speak('want to do anything else?')
                
            except Exception as e:
                speak("Sorry,I am currently unable to send the email.Please try again later")  
                speak('do you want me to do anything else?')

        elif 'visual studio code' in query or 'open code' in query or 'code' in query or 'visual code' in query:
            open_file('Visual Studio Code','Electron')
            speak('visual studio code is open now')
            bye=False
        
        elif 'safari' in query:
            open_file('Safari','Safari')
            speak('Safari is open now')
            bye=False
        
        elif 'calculator' in query:
            open_file('Calculator','Calculator')
            speak('Calculator is open now')
            bye=False

        elif 'chrome' in query:
            open_file('Google Chrome','Google Chrome')
            speak('Chrome is open now')
            bye=False

        elif "close notepad" in query:
            speak("okay sir, closing notepad")
            os.system("taskkill/f /im notepad.exe")
            speak('you want me to do anything else?')
            
        elif ("close cmd"in query or "close command prompt" in query):
            speak("okay sir, closing cmd")
            os.system("taskkill /f /im cmd.exe")
            speak('you want me to do anything else?')

        elif 'joke' in query or 'jokes' in query:
            joke = pyjokes.get_joke('en','all')
            #print(joke)
            speak(joke)
            speak('anything else?')

        elif 'jobs' in query or 'job' in query or 'job recommandation' in query or 'work' in query:
            platforms = [
                'linkedin', 'indeed', 'glassdoor', 'hackerrank', 'naukri',
                'intern shala'
            ]
            speak("Select a platform that you prefer:")
            print('\n'.join(platforms))
            statement1 = take_command().lower()
            #statement1 = input()
            if (statement1 == 0):
                continue
            if 'linkedin' in statement1 or 'LinkedIn' in statement1 or 'Linkedin' in statement1:
                webbrowser.open_new_tab("https://www.linkedin.com/jobs")
                speak("LinkedIn is open now")
                break
            elif 'indeed' in statement1:
                webbrowser.open_new_tab("https://www.indeed.com/jobs")
                speak("Indeed is open now")
                break
            elif 'glassdoor' in statement1:
                webbrowser.open_new_tab("https://www.glassdoor.com/jobs")
                speak("Glassdoor is open now")
                break
            elif 'hackerrank' in statement1:
                webbrowser.open_new_tab(
                    "https://www.hackerrank.com/jobs/search")
                speak("HackerRank is open now")
                break
            elif 'naukri' in statement1:
                webbrowser.open_new_tab("https://www.naukri.com/jobs")
                speak("Naukri is open now")
                break
            elif 'intern shala' in statement1:
                webbrowser.open_new_tab('internshala.com')
                speak('Intern Shala is open now')
                break
            else:
                speak("Sorry we couldn't find your search!!!")
                speak('you want me to do anything else?')
            #time.sleep(3)
            

        elif "shut down the system" in query:
            os.system("shutdown /s /t 5")

        elif 'movie ticket booking' in query or 'movie booking' in query or 'movie ticket' in query:
            speak('opening bookmyshow')
            webbrowser.open_new_tab("https://in.bookmyshow.com/")
            speak(" Book my show website is open now")
            bye=False

        elif "restart the system" in query:
            os.system("shutdown /r /t 5")

        elif 'online courses' in query or 'course' in query:
            platforms = [
                'coursera', 'udemy', 'edx', 'skillshare', 'datacamp', 'udacity'
            ]
            speak("Select a platform that you prefer : ")
            print("\n".join(platforms))
            statement1 = take_command().lower()
            if statement1 == 0:
                continue
            if 'coursera' in statement1:
                webbrowser.open_new_tab("https://www.coursera.org")
                speak("Coursera is open now")
                bye=False
            elif 'udemy' in statement1:
                webbrowser.open_new_tab("https://www.udemy.com")
                speak("udemy is open now")
                bye=False
            elif 'edx' in statement1:
                webbrowser.open_new_tab("https://www.edx.org/")
                speak("edx is open now")
                bye=False
            elif 'skillshare' in statement1:
                webbrowser.open_new_tab("https://www.skillshare.com")
                speak("skill share is open now")
                bye=False
            elif 'datacamp' in statement1:
                webbrowser.open_new_tab("https://www.datacamp.com")
                speak("datacamp is open now")
                bye=False
            elif 'udacity' in statement1:
                webbrowser.open_new_tab("https://www.udacity.com")
                speak("udacity is open now")
                bye=False
            else:
                speak("Sorry we couldn't find your search!!!")
                speak('you want me to do anything else?')

        elif 'train ticket booking' in query or 'train booking' in query or 'train ticket' in query or 'train ticket' in query:
            speak('opening website for train ticket booking')
            webbrowser.open_new_tab("https://www.railyatri.in/train-ticket/")
            speak(" IRCTC website is open now, have a good journey !")
            bye=False

        elif 'bus ticket booking' in query or 'bus booking' in query or 'bus ticket' in query:
            speak('opening website for bus ticket booking')
            webbrowser.open_new_tab("https://www.redbus.in")
            speak(" Red bus website is open now, have a good journey !")
            bye=False

        elif 'airplane ticket booking' in query or 'airplane booking' in query or 'airplane ticket' in query:
            speak('opening website for airplane ticket booking')
            webbrowser.open_new_tab("https://www.goindigo.in")
            speak(" Indigo website is open now, have a good journey !")
            bye=False

        elif "hotel" in query or "hotel booking" in query:
            speak('Opening go ibibo .com')
            webbrowser.open_new_tab('https://goibibo.com/hotels')
            bye=False

        elif "sleep the system" in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        elif 'switch the window' in query:
            if sys.platform == "win32":
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")  
                bye=False
            else:
                pyautogui.keyDown("command")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("command")  
                bye=False

        elif ("tell me news" in query or "news" in query):
            speak("Please wait, Fetching the latest news")
            news()
            speak('need something else?')

        elif ("tell me my location" in query or "location" in query):
            speak("Hold on,Locating our current location")
            try:
                ipadd=requests.get("https://api.ipify.org").text
                url="https://get.geojs.io/v1/ip/geo/"+ipadd+".json"
                geo_requests= requests.get(url)
                geo_data=geo_requests.json()
                city=geo_data['city']
                country=geo_data['country']
                speak(f"We are in {city},{country}")
                speak('need something else?')

            except Exception as e:
                speak("Sorry,I am unable to locate our current location due to poor connectivity. Please try after sometime.")
                bye=False

        elif "take a screenshot" in query or "take screenshot" in query:
            name=datetime.datetime.now()
            speak("taking screenshot...")
            time.sleep(3)
            img=pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("Screenshot taken")  
            speak('need anything else?')

        elif  "read pdf" in query or " read book " in query :
            pdf_reader()
            bye=False
            
        elif "how much battery is left" in query or "how much power is left" in query or "battery" in query:
            battery=psutil.sensors_battery()
            percentage=battery.percent
            speak(f"We have {percentage} percent battery. ")
            if percentage>=50:
                speak("We have enough power to go on.")
            elif percentage>=20 and percentage<50:
                speak("You shall connect the system to a charging point")    
            elif percentage<20:
                speak("Battery about to die,connect to a charging point as soon as possible")
            speak('you want me to do anything else')

        elif "internet speed" in query:
            speak("Checking internet speed")
            st=speedtest.Speedtest()
            dl=round(float(st.download())/8000000,2)
            up=round(float(st.upload())/8000000,2)
            speak(f"Current downloading speed is {dl}mb/s while uploading speed is {up}")   
            speak('you want me to do anything else?')

        elif "volume up" in query:
            pyautogui.press("volumeup")
            speak('you want me to do anything else?')
        elif "volume down" in query:
            pyautogui.press("volumedown")
            speak('you want me to do anything else?')
        elif "volume mute" in query or "mute" in query:
            pyautogui.press("volumemute")   
            speak('you want me to do anything else?')

        elif 'flip the coin' in query or 'toss the coin' in query or 'toss a coin' in query or 'flip a coin' in query:
            chances = ['Heads', 'Tails']
            res = random.choice(chances)
            picLine = random.randint(1, 3)
            lines = [htLine1, htLine2, htLine3]
            lines[picLine - 1]()
            speak('you want me to do anything else?')

        elif 'dice' in query:
            num = random.randint(1, 6)
            speak("Your rolled " + str(num))   
            speak('you want me to do anything else?')

        elif 'bye' in query or 'no' in query or ' no thanks' in query:
            speak('Untill next time')
            bye=False

        else:
            speak("Sorry,I don't know how to do that right now but i am still learning how to be more helpful")
            speak('anything else?')
        #time.sleep(2)

if __name__=="__main__":
    TaskExecution()