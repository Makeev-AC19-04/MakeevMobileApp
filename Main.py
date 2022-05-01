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
    MDNavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    orientation: "vertical"
                    MDToolbar:
                        title: "Navigation Drawer"
                        elevation: 10
                        left_action_items: [['menu', lambda x: nav_drawer.set_state('toggle')]]
                    Widget:
                        orientation: "vertical"
                        MDLabel:
                            id: text_label
                            font_size: "30sp"
                            color: "000000"
                            text: root.data_label
                            pos_hint: {"center_x": 1, "center_y":1}
                        MDRectangleFlatButton:
                            id: button_label
                            text: "Изменить надпись"
                            background_color:'#00FFCE'
                            pos_hint: {"center_x":1, "center_y":1}
                            on_press: root.changetitle()
                        MDRectangleFlatButton:
                            id: button_label1
                            text: "Вывести список докторов"
                            bold: True
                            background_color:'#00FFCE'
                            size_hint: (1,0.5)
                            on_press: root.GetDoctors()
                        MDTextField:
                            id: text_input
                            hint_text: "No helper text"
                        
                    
                        
                        
        MDNavigationDrawer:
            id: nav_drawer 
            ContentNavigationDrawer:
        
""" # Включаем виджеты для верстки

class ContentNavigationDrawer(BoxLayout): #Отрисовка элементов панели навигации
    pass

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
        self.ids.text_label.text = doctors.text


class MyApp(MDApp):
    data_label = StringProperty("Текст")

    def changetitle(self):
        name = self.ids.text_input.text
        self.ids.text_label.text = name #f'hello {name}' - для вывода дополненного текста
        self.ids.text_input.text = ''

    def GetDoctors(self): #Получим список всех докторов
        doctors = requests.get('https://localhost:5001/doctors', verify = False)
        self.ids.text_label.text = str(json.loads(doctors.text)) #Формируем список словарей из полученного json текста

    def build(self):
        return Builder.load_string(KV)

MyApp().run()
