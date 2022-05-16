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

access_token = '' #Токен авторизации

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

class MainScreen(Screen):
    pass

class NavigationLayout(Screen):
    pass

class OtherScreen(Screen):
    pass

class AuthorizationScreen(Screen):
    def Auth(self):
        session = requests.Session()
        auth_data = {"login":self.ids.text_login.text,"password":self.ids.text_password.text}
        auth_body = session.post('https://localhost:5001/account/login', json=auth_data, verify=False)
        if auth_body.status_code == 400:
            self.ids.text_role.text = "Неверный логин или пароль!"
        else:
            access_token = auth_body.json()["access_token"]
            role = session.get('https://localhost:5001/values/getrole', headers={'Authorization': "Bearer {}".format(access_token)}, verify=False)
            self.ids.text_role.text = str(role.text)
    pass


class MainApp(MDApp):
    #theme_cls = ThemeManager()
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='Main'))
        sm.add_widget(NavigationLayout(name='Nav'))
        sm.add_widget(DoctorsScreen(name='Doctors'))
        sm.add_widget(OtherScreen(name='Other'))
        sm.add_widget(AuthorizationScreen(name='Authorization'))
       #screen = Builder.load_string(KV)
        return sm

MainApp().run()