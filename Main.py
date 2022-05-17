from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import MDList, TwoLineListItem
from kivy.uix.scrollview import ScrollView
from kivy.core.clipboard import Clipboard
import requests
from kivy.clock import Clock
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
    data_label = StringProperty("Список докторов")
    #data_role = StringProperty()

    def GetDoctors(self):  # Получим список всех докторов
        self.ids.mdlist_doctors.clear_widgets() # Очищаем список для предотвращения дублирования
        doctors = requests.get('https://localhost:5001/doctors', verify=False) #        self.ids.text_label.text = str(json.loads(doctors.text)) #Формируем список словарей из полученного json текста
        doctors = json.loads(doctors.text)
        for i in doctors:
            self.ids.mdlist_doctors.add_widget(TwoLineListItem(text = i['name'],
                                                               secondary_text = 'id:' + str(i['id']),
                                                               on_press=lambda x: Clipboard.copy(self.secondary_text)))
    pass

class MainScreen(Screen):
    pass

class NavigationLayout(Screen):
    pass

class ChangeDoctorScreen(Screen):
    global access_token
    doctorsdata = {}

    def ChangeLabel(self, text):
        self.ids.text_label.text = text

    def SearchDoctor(self):
        label = self.ids.text_label.text
        doctor = requests.get('https://localhost:5001/doctors/' + self.ids.text_searchdoctor.text, verify=False)
        if doctor.status_code == 404:
            Clock.schedule_once(lambda dt: self.ChangeLabel("Доктор не найден!"))
            Clock.schedule_once(lambda dt: self.ChangeLabel("Изменить данные о докторе"), 1.5)
        else:
#            self.ids.text_label.text = "Редактировать данные о докторе"
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
            Clock.schedule_once(lambda dt: self.ChangeLabel("Данные сохранены"))
            Clock.schedule_once(lambda dt: self.ChangeLabel("Изменить данные о докторе"), 1.5)
        elif putreq.status_code == 401:
            Clock.schedule_once(lambda dt: self.ChangeLabel("Вы не авторизованы"))
            Clock.schedule_once(lambda dt: self.ChangeLabel("Изменить данные о докторе"), 1.5)
        else:
            Clock.schedule_once(lambda dt: self.ChangeLabel("Произошла ошибка"))
            Clock.schedule_once(lambda dt: self.ChangeLabel("Изменить данные о докторе"), 1.5)
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
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='Main'))
        sm.add_widget(NavigationLayout(name='Nav'))
        sm.add_widget(DoctorsScreen(name='Doctors'))
        sm.add_widget(AuthorizationScreen(name='Authorization'))
        sm.add_widget(ChangeDoctorScreen(name='ChangeDoctor'))
        return sm

MainApp().run()