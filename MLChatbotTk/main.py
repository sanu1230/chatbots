from telnetlib import EC
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from tkinter import *
import pyttsx3 as pp
import speech_recognition as sp
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import os

# pyttsx is for audio
# to initialise audio


engine = pp.init()

voices = engine.getProperty('voices')  # get all voices
engine.setProperty('voice', voices[1].id)


def speak(word):
    engine.say(word)
    engine.runAndWait()


chatbot = ChatBot("Eve", storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
                  preprocessors=['chatterbot.preprocessors.clean_whitespace',
                                 'chatterbot.preprocessors.unescape_html'],
                  filters='chatterbot.filters.RepetitiveResponseFilter',
                  # logic_adapters=[
                  #   {
                  #       "import_path": ["chatterbot.logic.BestMatch",
                  #                       "chatterbot.logic.TimeLogicAdapter",
                  #                       "chatterbot.logic.MathematicalEvaluation"],
                  #       'maximum_similarity_threshold': 0.90,
                  #       'default_response': ['I am sorry, but I do not understand.',
                  #                            "Sorry I dont understand you, try rephrasing your sentence",
                  #                            "Sorry I didnt get what you said"]
                  #       "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
                  #       "response_selection_method": "chatterbot.response_selection.get_first_response",
                  #}],
                  )


trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")
trainer.train('./data')


music = ['play music', 'song', 'play', 'music', 'video']

# takes query: it takes audio as input from user and convert it to string


def speech_query():
    sr = sp.Recognizer()
    sr.pause_threshold=1
    with sp.Microphone() as m:
        try:
            audio = sr.listen(m)
            query = sr.recognize_google(audio, language="eng-in")
            words = list(query.split(" "))
            if any(x in words for x in music):
                textF.delete(0, END)
                textF.insert(0, query)
                driver = webdriver.Chrome('./chromedriver.exe')
                driver.maximize_window()
                driver.get('https://www.youtube.com')
                searchbox = driver.find_element_by_xpath('/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div/div[1]/input')
                searchbox.send_keys(str(query))
                searchButton = driver.find_element_by_xpath('//*[@id="search-icon-legacy"]')
                searchButton.click()
                all_elements = driver.find_elements(By.CLASS_NAME, 'style-scope yt-img-shadow')
                all_elements[0].click()
                full_screen = driver.find_element_by_xpath('//*[@id="movie_player"]/div[32]/div[2]/div[2]/button[9]')
                full_screen.click()
                skip_ad = driver.find_element_by_xpath('//*[@id="skip-button:x"]/span/button')
                skip_ad.click()
                response = "Here is what you are looking for."
                msgs.insert(END, "You: " + query)
                msgs.insert(END, "Eve: " + response)
                speak(response)
                msgs.yview(END)
                visible = EC.visibility_of_element_located
                wait = WebDriverWait(driver, 3)
                wait.until(visible(By.ID, "video-title"))
            else:
                textF.delete(0, END)
                textF.insert(0, query)
                response_from_bot()
        except Exception as e:
            print(e)
            print("not recognize")


def response_from_bot():
    query = textF.get()
    response = str(chatbot.get_response(query))
    msgs.insert(END, "You: " + query)
    msgs.insert(END, "Eve: " + response)
    speak(response)
    textF.delete(0, END)
    msgs.yview(END)


main = Tk()
main.geometry("450x600")
main.title("Your Friend 'Eve-Bot'")

img = PhotoImage(file="Eve1.png")

photoL = Label(main, image=img)
photoL.pack(pady=5)

# Creating a frame
frame = Frame(main)
frame.pack()

# Creating scrollbar in frame
sc = Scrollbar(frame)
sc.pack(side=RIGHT, fill=Y)

# Creating a message box in frame
msgs = Listbox(frame, width=80, height=20)
msgs.pack(side=LEFT, fill=BOTH, pady=10)

# Creating text field
textF = Entry(main, font=("Bahnschrift", 20))
textF.pack(fill=X, pady=10)

# Creating button
btn = Button(main, text="Send", font=("Bahnschrift", 15), command=response_from_bot)
btn.pack()


def enter_function(event):
    btn.invoke()



# going to bind main window with enter key
main.bind('<Return>', enter_function)


def repeatl():
    while True:
        speech_query()


t = threading.Thread(target=repeatl)
t.start()

main.mainloop()
