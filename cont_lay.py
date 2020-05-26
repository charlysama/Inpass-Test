from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
import kivy.utils
from kivy.graphics import Color,Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
import requests
import json
from kivy.app import App
from functools import  partial

class ImageButton(ButtonBehavior, Image):
    pass
class LabelButton(ButtonBehavior, Label):
    pass
class ContactoBanner(GridLayout):
    def __init__(self, **kwargs):
        self.rows = 1
        super(ContactoBanner, self).__init__()
    #Queery by ID use local_id to read all
        check_rqe = requests.get('https://innpass-62327.firebaseio.com/.json?orderBy="ID"&equalTo=' + kwargs['ContactoID'])
        print(check_rqe.ok)
        unique_ID = check_rqe.json().keys()
        temp = list(unique_ID)
        print(temp[0])
        data = check_rqe.json()
        print(data)
    #Add friend Avatar
        elavatar = data[temp[0]]['avatar']
        print(elavatar)
        image_button = ImageButton(source="icon/" + elavatar,size_hint=(.2,.8), pos_hint ={"top":1 , "right":0},
                                   on_release=partial(App.get_running_app().load_pac_screen,kwargs['ContactoID']))
        print("Avatar ok")
        self.add_widget(image_button)
        # Add friend ID

        print("ID ok")
        elid = data[temp[0]]['ID']
        elid_button = LabelButton(text=str(elid), size_hint=(.2, .2), pos_hint={"top": 1, "right": 0})
        self.add_widget(elid_button)

    #Add friend Weitgh and date
        if data[temp[0]]['Pesos'] != '':
            print("tenemos Peso")
            elpeso = data[temp[0]]['Pesos']
            tempi = list(elpeso)
            pesoenKG = data [temp[0]]['Pesos'][tempi[0]]
            labelpeso = pesoenKG['PesoKg']
            peso_button = LabelButton (text = str(labelpeso),size_hint=(.4,.5), pos_hint ={"top":1 , "right":.4},
                                   on_release=partial(App.get_running_app().load_pac_peso,kwargs['ContactoID']))
            labelfecha = pesoenKG['Fecha']
            fecha_button = LabelButton(text=str(labelfecha),size_hint=(.4,.5), pos_hint ={"top":1 , "right":.4},
                                   on_release=partial(App.get_running_app().load_pac_peso,kwargs['ContactoID']))
            self.add_widget(fecha_button)
            self.add_widget(peso_button)
        else:
            peso_button = LabelButton(text='No data', size_hint=(.4, .5), pos_hint={"top": 1, "right": .4},
                                   on_release=partial(App.get_running_app().load_pac_peso,kwargs['ContactoID']))
            fecha_button = LabelButton(text='No data', size_hint=(.4, .5), pos_hint={"top": 1, "right": .4},
                                   on_release=partial(App.get_running_app().load_pac_peso,kwargs['ContactoID']))
            self.add_widget(fecha_button)
            self.add_widget(peso_button)

    #Add Friend Name
        print("Nombre ok")
        elnombre =  data[temp[0]]['Nombre']
        elnombre_button = LabelButton(text=elnombre,size_hint=(.4,.5), pos_hint ={"top":1 , "right":0.8},
                                   on_release=partial(App.get_running_app().load_pac_perfil,kwargs['ContactoID']))
        self.add_widget(elnombre_button)
    #Add Friend Apellido
        print("Apellido ok")
        elapellido = data[temp[0]]['Apellido']
        elapellido_button = LabelButton(text=elapellido,size_hint=(.4,.5), pos_hint ={"top":1 , "right":0.8},
                                   on_release=partial(App.get_running_app().load_pac_perfil,kwargs['ContactoID']))
        self.add_widget(elapellido_button)


