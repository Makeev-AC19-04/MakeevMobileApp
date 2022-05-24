from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import MDList, TwoLineListItem
from kivy.uix.scrollview import ScrollView
from kivymd.toast.kivytoast.kivytoast import toast
from kivy.clock import Clock
from kivy.lang import Builder
import json
import requests

#GithubTest
#Crossplatform kaif
#Комментарий от Ильи

KV = '''
#:kivy 1.0.9
#:set SidebarW 300
MainScreen:
<MainScreen>:
    MDToolbar:
        id: toolbar
        pos_hint: {"top": 1}
        elevation: 10
        title: "Медицинский центр"
        specific_text_color: 1,1,1,0.9
        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

    NavigationLayout:
        ScreenManager: #Отрисовка текущего экрана
            id: screen_manager
            Screen:
            DoctorsScreen:
            AuthorizationScreen:
            ChangeDoctorScreen:
            ChangeAdressScreen:
        MDNavigationDrawer: #Отрисовка панели навигации
            id: nav_drawer
            ContentNavigationDrawer:
                BoxLayout:
                    orientation: 'vertical'
                    MDLabel:
                        text: 'Меню'
                    ScrollView:
                        MDList:
                            OneLineListItem:
                                text: 'Список всех докторов'
                                on_press:
                                    nav_drawer.set_state("close")
                                    screen_manager.current = 'Doctors'
                            OneLineListItem:
                                text: 'Авторизоваться'
                                on_press:
                                    nav_drawer.set_state("close")
                                    screen_manager.current = 'Authorization'
                            OneLineListItem:
                                text: 'Изменить данные доктора'
                                on_press:
                                    nav_drawer.set_state("close")
                                    screen_manager.current = 'ChangeDoctor'
                            OneLineListItem:
                                text: 'Изменить адрес сервера'
                                on_press:
                                    nav_drawer.set_state("close")
                                    screen_manager.current = 'ChangeAdress'
                    #GridLayout:
                    #StackLayout:
                    BoxLayout:
                        size_hint_x:0.8
                        pos_hint: {"center_x": 0.45, "center_y":0}
                        MDLabel:
                            pos_hint: {"center_x": 0.3, "center_y":0.8}
                            #halign: "center"
                            text: 'Изменить тему'
                            #width: 20
                        MDSwitch:
                            pos_hint: {"center_x": 0.5, "center_y":0.8}
                            #halign: "center"
                            on_press:
                                app.ChangeTheme()


<AuthorizationScreen>:
    name: 'Authorization'
    orientation: "vertical"
    MDLabel:
        id: text_label
        font_size: "30sp"
        color: "000000"
        text: "Вход в аккаунт"
        halign: "center"
        pos_hint: {"center_x": 0.5, "center_y":0.8}
    MDTextField:
        id: text_login
        required: True
        hint_text: "Логин"
        pos_hint: {"center_x": 0.5, "center_y": 0.55}
        size_hint_x:None
        size_hint_x:0.3
    MDTextField:
        id: text_password
        line_color_focus: self.theme_cls.opposite_bg_normal
        required: True
        password: True
        password_mask: "*" #●
        hint_text: "Пароль"
        pos_hint: {"center_x": 0.5, "center_y": 0.45}
        size_hint_x:None
        size_hint_x:0.3
    MDRectangleFlatButton:
        id: button_auth
        text: "Войти"
        background_color:'#00FFCE'
        pos_hint: {"center_x":0.5, "center_y":0.3}
        size_hint_x:0.3
        on_press: root.Auth()
    MDLabel:
        id: text_role
        font_size: "30sp"
        color: "000000"
        text: "Ваша роль: "
        halign: "center"
        pos_hint: {"center_x": 0.5, "center_y": 0.15}

<DoctorsScreen>
    name: 'Doctors'
    orientation: "vertical"
    MDLabel:
        id: text_label
        halign: "center"
        font_size: "30sp"
        color: "000000"
        text: root.data_label
        pos_hint: {"center_x": 0.5, "center_y":0.85}
    MDRectangleFlatButton:
        id: button_label1
        text: "Вывести список докторов"
        bold: True
        background_color:'#00FFCE'
        on_press: root.GetDoctors()
        size_hint_x:0.3
        pos_hint: {"center_x": 0.5, "center_y":0.1}
    ScrollView:
        id: list_doctors
        size_hint_y: 0.6
        pos_hint: {"center_x": 0.5, "center_y":0.5}
        MDList:
            id: mdlist_doctors
            pos_hint: {"center_x": 0.5, "center_y":0.5}

<ChangeDoctorScreen>:
    name: 'ChangeDoctor'
    orientation: "vertical"
    MDLabel:
        id: text_label
        font_size: "30sp"
        color: "000000"
        text: "Изменить данные доктора"
        halign: "center"
        pos_hint: {"center_x": 0.5, "center_y":0.8}
    MDTextField:
        id: text_searchdoctor
        required: True
        hint_text: "id доктора"
        pos_hint: {"center_x": 0.5, "center_y": 0.55}
        size_hint_x:None
        size_hint_x:0.3
    MDRectangleFlatButton:
        id: button_searchdoctor
        text: "Найти доктора"
        background_color:'#00FFCE'
        pos_hint: {"center_x":0.5, "center_y":0.4}
        size_hint_x:0.3
        on_press: root.SearchDoctor()
    MDTextField:
        id: text_doctorsname
        required: True
        hint_text: "ФИО доктора"
        pos_hint: {"center_x": 0.5, "center_y": 0.3}
        size_hint_x:None
        size_hint_x:0.3
    MDTextField:
        id: text_doctorsspeciality
        required: True
        hint_text: "id специальности доктора"
        pos_hint: {"center_x": 0.5, "center_y": 0.2}
        size_hint_x:None
        size_hint_x:0.3
    MDRectangleFlatButton:
        id: button_searchdoctor
        text: "Сохранить"
        background_color:'#00FFCE'
        pos_hint: {"center_x":0.25, "center_y":0.1}
        on_press: root.ChangeDoctor()
        size_hint_x:0.2
    MDRectangleFlatButton:
        id: button_deletedoctor
        text: "Удалить"
        background_color:'#00FFCE'
        pos_hint: {"center_x":0.75, "center_y":0.1}
        on_press: root.DeleteDoctor()
        size_hint_x:0.2
    MDRectangleFlatButton:
        id: button_postdoctor
        text: "Добавить"
        background_color:'#00FFCE'
        pos_hint: {"center_x":0.5, "center_y":0.1}
        on_press: root.PostDoctor()
        size_hint_x:0.2

<ChangeAdressScreen>:
    name: 'ChangeAdress'
    orientation: "vertical"
    MDLabel:
        id: text_label
        font_size: "30sp"
        color: "000000"
        text: "Текущий адрес сервера"
        halign: "center"
        pos_hint: {"center_x": 0.5, "center_y":0.8}
    MDTextField:
        id: text_adress
        text: root.link
        pos_hint: {"center_x": 0.5, "center_y": 0.55}
        size_hint_x:None
        size_hint_x:0.3
    MDRectangleFlatButton:
        id: button_changeadress
        text: "Сохранить адрес"
        background_color:'#00FFCE'
        pos_hint: {"center_x":0.5, "center_y":0.1}
        size_hint_x:0.3
        on_press: root.ChangeAdress()
'''

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
        try:
            doctor = requests.get(access_token.link+'doctors/' + self.ids.text_searchdoctor.text, verify=False)
        except requests.exceptions.ConnectionError:
            toast("Ошибка соединения")
        else:
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
        try:
            putreq = requests.put(access_token.link+'doctors/' + self.ids.text_searchdoctor.text,
                                  verify=False,
                                  json=self.doctorsdata,
                                  headers={'Authorization': "Bearer {}".format(access_token.token)})
        except requests.exceptions.ConnectionError:
            toast("Ошибка соединения")
        else:
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
        try:
            delreq = requests.delete(access_token.link+'doctors/' + self.ids.text_searchdoctor.text,
                                  verify=False,
                                  headers={'Authorization': "Bearer {}".format(access_token.token)})
        except requests.exceptions.ConnectionError:
            toast("Ошибка соединения")
        else:
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
        try:
            putreq = requests.post(access_token.link+'doctors/',
                                  verify=False,
                                  json=doctorsdata,
                                  headers={'Authorization': "Bearer {}".format(access_token.token)})
        except requests.exceptions.ConnectionError:
            toast("Ошибка соединения")
        else:
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
        try:
            auth_body = session.post(access_token.link+'account/login', json=auth_data, verify=False)
        except requests.exceptions.ConnectionError:
            toast("Ошибка соединения")
        else:
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
        sm = Builder.load_string(KV)
        return sm

    def on_start(self):
        self.theme_cls.primary_palette = "Green"

    def ChangeTheme(self):
        if self.theme_cls.theme_style == "Dark":
            self.theme_cls.theme_style = "Light"
        else:
            self.theme_cls.theme_style = "Dark"

MainApp().run()