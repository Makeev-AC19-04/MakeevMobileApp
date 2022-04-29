from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.clock import Clock


KV = """ 
MyBL:
        Label:
                id: text_label
                font_size: "30sp"
                text: root.data_label
        TextInput:
                id: text_input
                multiline: False
                size_hint: (0.5,0.1)
        Button:
                id: button_label
                text: "Кнопка"
                bold: True
                background_color:'#00FFCE'
                size_hint: (1,0.5)
                on_press: root.callback()
""" # Включаем виджеты для верстки

class MyBL(BoxLayout):
    data_label = StringProperty("Текст")
    def callback(self):
        data_label = StringProperty("Вы нажали на кнопку")
        name = self.ids.text_input.text
        self.ids.text_label.text = name

class MyApp(App):
    running = True

    def build(self):
        return Builder.load_string(KV)

    def on_stop(self):
        self.running = False

app = MyApp()
app.run()
