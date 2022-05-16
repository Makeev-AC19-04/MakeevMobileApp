from kivymd.app import MDApp
from kivy.app import App
from kivymd.theming import ThemeManager
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
import requests
import json

#GithubTest
#Crossplatform kaif
#Комментарий от Ильи

KV = """
MDNavigationLayout:
    ScreenManager: #Отрисовка текущего экрана
        id: screen_manager
        Screen:
            BoxLayout:
                orientation: "vertical"
                MDToolbar:
                    title: "Navigation Drawer"
                    left_action_items: [['menu', lambda x: nav_drawer.set_state('toggle')]]
                    elevation: 10
                Widget:
        DoctorsScreen:
        OtherScreen:
        AuthorizationScreen:
    MDNavigationDrawer: #Отрисовка панели навигации
        id: nav_drawer 
        BoxLayout:
            orientation: 'vertical'   
            MDLabel:
                text: 'Меню'
            ScrollView:
                MDList:
                    OneLineListItem:
                        text: 'Список всех докторов'
                        on_press:
                            #nav_drawer.set_state("close") 
                            screen_manager.current = 'Doctors'
                    OneLineListItem:
                        text: 'Открыть другой экран'
                        on_press:
                            #nav_drawer.set_state("close") 
                            screen_manager.current = 'Other'
                    OneLineListItem:
                        text: 'Авторизоваться'
                        on_press:
                            #nav_drawer.set_state("close") 
                            screen_manager.current = 'Authorization'
        ContentNavigationDrawer:
            id: content_drawer

<OtherScreen>
    name: 'Other'
    orientation: "vertical"
    MDLabel:
        id: text_label
        font_size: "30sp"
        color: "000000"
        text: "Other text"
        pos_hint: {"center_x": 0.5, "center_y":0.5}

<AuthorizationScreen>
    name: 'Authorization'
    orientation: "vertical"
    MDLabel:
        id: text_label
        font_size: "30sp"
        color: "000000"
        text: "Вход в аккаунт"
        pos_hint: {"center_x": 1, "center_y":1}
    MDTextField:
        id: text_login
        required: True
        hint_text: "Логин"
        pos_hint: {"center_x": 0.5, "center_y": 0.55}
        size_hint_x:None
        width:300
    MDTextField:
        id: text_password
        line_color_focus: self.theme_cls.opposite_bg_normal
        required: True
        password: True
        password_mask: "*" #●
        hint_text: "Пароль"
        pos_hint: {"center_x": 0.5, "center_y": 0.45}
        size_hint_x:None
        width:300
    MDRectangleFlatButton:
        id: button_auth
        text: "Войти"
        background_color:'#00FFCE'
        pos_hint: {"center_x":1, "center_y":1}
        on_press: root.changetitle()
    MDLabel:
        id: text_role
        font_size: "30sp"
        color: "000000"
        text: "Ваша роль: " + "aaa"
        pos_hint: {"center_x": 0.5, "center_y": 0.25}
        
<DoctorsScreen>
    name: 'Doctors'
    orientation: "vertical"
    MDLabel:
        id: text_label
        font_size: "30sp"
        color: "000000"
        text: root.data_label
        pos_hint: {"center_x": 0.5, "center_y":0.5}
    MDRectangleFlatButton:
        id: button_label
        text: "Изменить надпись"
        background_color:'#00FFCE'
        pos_hint: {"center_x": 0.5, "center_y":0.4}
        on_press: root.changetitle()
    MDRectangleFlatButton:
        id: button_label1
        text: "Вывести список докторов"
        bold: True
        background_color:'#00FFCE'
        on_press: root.GetDoctors()
    #MDTextField:
     #   id: text_input
      #  hint_text: "No helper text"
        

""" # Включаем виджеты для верстки



class ContentNavigationDrawer(BoxLayout): #Отрисовка элементов панели навигации
    pass

class DoctorsScreen(Screen):
    data_label = StringProperty("Текст")
    data_role = StringProperty()

    def changetitle(self):
        name = self.ids.text_input.text
        self.ids.text_label.text = name  # f'hello {name}' - для вывода дополненного текста
        self.ids.text_input.text = ''

    def GetDoctors(self):  # Получим список всех докторов
        doctors = requests.get('https://localhost:5001/doctors', verify=False) #        self.ids.text_label.text = str(json.loads(doctors.text)) #Формируем список словарей из полученного json текста
        self.ids.text_label.text = doctors.text
    pass

class OtherScreen(Screen):
    pass

class AuthorizationScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(DoctorsScreen(name='Doctors'))
sm.add_widget(OtherScreen(name='Other'))
sm.add_widget(AuthorizationScreen(name='Authorization'))

class MyApp(MDApp):
    #theme_cls = ThemeManager()
    def build(self):
       screen = Builder.load_string(KV)
       return screen

MyApp().run()
