from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import MDList, TwoLineListItem
from kivy.uix.scrollview import ScrollView
from kivymd.toast.kivytoast.kivytoast import toast
from kivy.clock import Clock
import json
import requests

#GithubTest
#Crossplatform kaif
#Комментарий от Ильи

class AccessToken():
    token = 'token'
    link = 'https://localhost:5001/'
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
        try:
            doctors = requests.get(access_token.link+'doctors/', verify=False)
        except requests.exceptions.ConnectionError:
            toast("Ошибка соединения")
        else:
            doctors = json.loads(doctors.text)  # Формируем список словарей из полученного json текста
            for i in doctors:
                self.ids.mdlist_doctors.add_widget(TwoLineListItem(text = i['name'], secondary_text = 'id:' + str(i['id'])))
    pass

class MainScreen(Screen):
    pass

class NavigationLayout(Screen):
    pass

class ChangeAdressScreen(Screen):
    global access_token
    link = access_token.link
    def ChangeAdress(self):
        access_token.link = self.ids.text_adress.text
        toast("Адрес изменен")
    pass

class ChangeDoctorScreen(Screen):
    global access_token
    doctorsdata = {}

    def ChangeLabel(self, text):
        self.ids.text_label.text = text

    def SearchDoctor(self):
        label = self.ids.text_label.text
        doctor = requests.get(access_token.link+'doctors/' + self.ids.text_searchdoctor.text, verify=False)
        if doctor.status_code == 404:
            Clock.schedule_once(lambda dt: self.ChangeLabel("Доктор не найден!"))
            Clock.schedule_once(lambda dt: self.ChangeLabel("Изменить данные о докторе"), 1.5)
        else:
            self.ids.text_doctorsname.text = str(doctor.json()["name"])
            self.ids.text_doctorsspeciality.text = str(doctor.json()["specialityId"])
            self.doctorsdata = doctor.json()

    def ChangeDoctor(self):
        self.doctorsdata['name'] = self.ids.text_doctorsname.text
        self.doctorsdata['specialityId'] = self.ids.text_doctorsspeciality.text
        putreq = requests.put(access_token.link+'doctors/' + self.ids.text_searchdoctor.text,
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

    def DeleteDoctor(self):
        delreq = requests.delete(access_token.link+'doctors/' + self.ids.text_searchdoctor.text,
                              verify=False,
                              headers={'Authorization': "Bearer {}".format(access_token.token)})
        if delreq.status_code == 204:
            Clock.schedule_once(lambda dt: self.ChangeLabel("Доктор удален"))
            Clock.schedule_once(lambda dt: self.ChangeLabel("Изменить данные о докторе"), 1.5)
        elif delreq.status_code == 401:
            Clock.schedule_once(lambda dt: self.ChangeLabel("Вы не авторизованы"))
            Clock.schedule_once(lambda dt: self.ChangeLabel("Изменить данные о докторе"), 1.5)
        else:
            Clock.schedule_once(lambda dt: self.ChangeLabel("Произошла ошибка"))
            Clock.schedule_once(lambda dt: self.ChangeLabel("Изменить данные о докторе"), 1.5)

    def PostDoctor(self):
        doctorsdata={}
        doctorsdata['name'] = self.ids.text_doctorsname.text
        doctorsdata['specialityId'] = self.ids.text_doctorsspeciality.text
        putreq = requests.post(access_token.link+'doctors/',
                              verify=False,
                              json=doctorsdata,
                              headers={'Authorization': "Bearer {}".format(access_token.token)})
        if putreq.status_code == 201:
            Clock.schedule_once(lambda dt: self.ChangeLabel("Доктор добавлен"))
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
        auth_body = session.post(access_token.link+'account/login', json=auth_data, verify=False)
        if auth_body.status_code == 400:
            self.ids.text_role.text = "Неверный логин или пароль!"
        else:
            access_token.token = auth_body.json()["access_token"]
            role = session.get(access_token.link+'values/getrole',
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
        sm.add_widget(ChangeAdressScreen(name='ChangeAdress'))
        return sm

MainApp().run()