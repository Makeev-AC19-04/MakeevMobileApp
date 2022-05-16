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

class AccessToken():
    token = 'token'
    def __init__(self, newtkn):
        token = newtkn

access_token = AccessToken('tut token') #Токен авторизации

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

class ChangeDoctorScreen(Screen):
    global access_token
    doctorsdata = {}

    def SearchDoctor(self):
        doctor = requests.get('https://localhost:5001/doctors/' + self.ids.text_searchdoctor.text, verify=False)
        if doctor.status_code == 404:
            self.ids.text_label.text = "Доктор не найден!"
        else:
            self.ids.text_label.text = "Редактировать данные о докторе"
            self.ids.text_doctorsname.text = str(doctor.json()["name"])
            self.ids.text_doctorsspeciality.text = str(doctor.json()["specialityId"])
            self.doctorsdata = doctor.json()

    def ChangeDoctor(self):
        self.doctorsdata['name'] = self.ids.text_doctorsname.text
        self.doctorsdata['specialityId'] = self.ids.text_doctorsspeciality.text
        putreq = requests.put('https://localhost:5001/doctors/' + self.ids.text_searchdoctor.text,
                              verify=False,
                              json=self.doctorsdata,
                              headers={'Authorization': "Bearer {}".format(access_token.token)})
        if putreq.status_code == 200:
         self.ids.text_label.text = "Данные сохранены"
        elif putreq.status_code == 401:
         self.ids.text_label.text = "Вы не авторизованы"
        else:
         self.ids.text_label.text = "Произошла ошибка"
    pass

class AuthorizationScreen(Screen):
    global access_token
    def Auth(self):
        session = requests.Session()
        auth_data = {"login":self.ids.text_login.text,"password":self.ids.text_password.text}
        auth_body = session.post('https://localhost:5001/account/login', json=auth_data, verify=False)
        if auth_body.status_code == 400:
            self.ids.text_role.text = "Неверный логин или пароль!"
        else:
            access_token.token = auth_body.json()["access_token"]
            role = session.get('https://localhost:5001/values/getrole',
                               headers={'Authorization': "Bearer {}".format(access_token.token)},
                               verify=False)
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
        sm.add_widget(ChangeDoctorScreen(name='ChangeDoctor'))
       #screen = Builder.load_string(KV)
        return sm

MainApp().run()