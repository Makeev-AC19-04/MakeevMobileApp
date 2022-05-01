import socket

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.network.urlrequest import UrlRequest
import requests
import json
import threading

#Window.size = (720, 1280) #Разрешение экрана моего телефона

KV = """ 
MyBL:
        orientation: "vertical"
        size_hint: (0.95, 0.95)
        pos_hint: {"center_x": 0.5, "center_y":0.5}
        Label:
                id: text_label
                font_size: "30sp"
                color: "000000"
                text: root.data_label
        TextInput:
                id: text_input
                multiline: False
                size_hint: (1,0.3)
        Button:
                id: button_label
                text: "Изменить надпись"
                bold: True
                background_color:'#00FFCE'
                size_hint: (1,0.5)
                on_press: root.changetitle()
        Button:
                id: button_label1
                text: "Вывести список докторов"
                bold: True
                background_color:'#00FFCE'
                size_hint: (1,0.5)
                on_press: root.GetDoctors()
        Button:
                id: button_label2
                text: "Кнопка2"
                bold: True
                background_color:'#00FFCE'
                size_hint: (1,0.5)
                on_press: root.callback() 
        
""" # Включаем виджеты для верстки

class MyBL(BoxLayout):

    data_label = StringProperty("Текст")

   # def __init__(self, **kwargs):
    #    super().__init__(**kwargs)
        #threading.Thread(target=self.get_data).start() #Инициализируем поток, для функции GetDoctors

    def changetitle(self):
        name = self.ids.text_input.text
        self.ids.text_label.text = name #f'hello {name}' - для вывода дополненного текста
        self.ids.text_input.text = ''

    def GetDoctors(self): #Получим список всех докторов
        doctors = requests.get('https://localhost:5001/doctors', verify = False)
        self.ids.text_label.text = str(json.loads(doctors.text)) #Формируем список словарей из полученного json текста



class MyApp(MDApp):
    running = True

    def build(self):
        return Builder.load_string(KV)

    def on_stop(self):
        self.running = False

app = MyApp()
app.run()
