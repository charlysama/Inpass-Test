from kivy.app import App
from kivy.lang import Builder
from kivy import utils
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from peso_lay import PesoBanner
from cont_lay import ContactoBanner
from act_lay import ActBanner
import requests
import json
from kivy.uix.label import Label
from os import walk
from functools import partial
from kivy.uix.textinput import TextInput
from firedata import MyFire
from datetime import date

class ImageButton(ButtonBehavior, Image):
    pass
class LabelButton(ButtonBehavior, Label):
    pass
class HomeScreen(Screen):
    pass
class SettingScreen(Screen):
    pass
class FotoScreen(Screen):
    pass
class PesoScreen(Screen):
    pass
class ActScreen(Screen):
    pass

class ChangeScreen(Screen):
    pass

class LoginScreen(Screen):
    pass
class AddScreen(Screen):
    pass
class AddActividadScreen(Screen):
    pass
class PerfilScreen(Screen):
    pass
class vPerfilScreen(Screen):
    pass
class ListaScreen(Screen):
    pass
class PacActScreen(Screen):
    pass
class PacPesoScreen(Screen):
    pass
class PacPerfilScreen(Screen):
    pass

GUI= Builder.load_file("main.kv")

class MainApp(App):


    def build(self):
        self.firedata = MyFire()
        return(GUI)


    def on_start(self):
        self.empieza()

    def empieza(self):
        #Get database data
        # Populate avatar grid
        avatar_grid = self.root.ids['ChangeScreen'].ids['avatar_grid']
        for root_dir, folders, files in walk("icon/avatar"):
            for f in files:
                img = ImageButton(source="icon/avatar/" + f, on_release=partial(self.change_avatar, f))
                avatar_grid.add_widget(img)


        try:
            #persistent sign in
                with open("refresh_token.txt",'r') as f:
                    refresh_token = f.read()
                    #use refresh token to get id
                id_token, local_id = self.firedata.exchange_refresh_token(refresh_token)

                self.local_id = local_id
                self.id_token = id_token
                result = requests.get("https://innpass-62327.firebaseio.com/" + local_id +".json?auth=" + id_token)
                print("was it ok?", result.ok)
                data = json.loads(result.content.decode())

                self.data = data
                self.Contactos = data['Contactos']
                print("Contactos todo bien")
                #Cargo Perfil
                verperfil = self.root.ids['vPerfilScreen']

                vnombre = verperfil.ids['Nombre']
                vapellido = verperfil.ids['Apellido']
                vtel = verperfil.ids['Telefono']
                vdir = verperfil.ids['Direccion']
                vnombre.text = data['Nombre']
                vapellido.text = data['Apellido']
                vtel.text = str(data['Tel'])
                vdir.text = data['Dir']
                #populate info
                avatar_image=self.root.ids['HomeScreen'].ids['avatar_image']
                avatar_image.source = "icon/avatar/" + data['avatar']
                print("Avatar todo bien")
                #Friend Id label

                my_id_label = self.root.ids['SettingScreen'].ids['my_id_label']
                my_id_label.text = "Mi ID es " + str(data['ID'])
                #Pesos
                pesos = data['Pesos']
                print("Peso todo bien")
                if pesos != "":

                    peso_grid_banner = self.root.ids['PesoScreen'].ids['peso_grid_banner']
                    pesos_keys = pesos.keys()
                    for peso_key in pesos_keys:
                        peso = pesos[peso_key]
                        W= PesoBanner(PesoKG = peso['PesoKg'], Fecha = peso['Fecha'] )
                        print("Peso banner")
                        peso_grid_banner.add_widget(W)
                #Actividades

                actividades = data['Actividades']
                print("Actividades todo bien")
                if actividades != "":
                    act_keys = actividades.keys()
                    act_grid_banner = self.root.ids['ActScreen'].ids['act_grid_banner']

                    for act_key in act_keys:
                            actividad = actividades[act_key]
                            W = ActBanner(Fecha=actividad['Fecha'],Acti=actividad['Acti'],Comentarios=actividad['Comentarios'],Persona=actividad['Persona'])
                            print("Actividad banner")
                            act_grid_banner.add_widget(W)
                print("Actividad cargada bien")
                # Populate Friend List
                if self.Contactos != {}:
                    print("1")
                    contactos_array = self.Contactos.split(",")
                    for contacto in contactos_array:
                        contacto = contacto.replace(" ","")
                        contacto_banner = ContactoBanner(ContactoID = contacto)
                        self.root.ids["ListaScreen"].ids["pac_banner"].add_widget(contacto_banner)

                print("2")

                print("start up ok")

                self.change_screen("HomeScreen")

        except Exception as e:
            print(e)





    def change_avatar(self,image,widget_id):
        #change avatar in app

        avatar_image=self.root.ids['HomeScreen'].ids['avatar_image']
        avatar_image.source = "icon/avatar/" + image

        my_data = '{"avatar": "%s"}' % image
        requests.patch(
            "https://innpass-62327.firebaseio.com/" + self.local_id + ".json?auth=" + self.id_token,
            data=my_data)
        self.change_screen("HomeScreen")
        pass

    def change_screen(self,screen_name):
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name

    def add_peso(self):
        peso_nuevo = self.root.ids['PesoScreen'].ids['peso_nuevo'].text
        try:
            peso_nuevo = int(peso_nuevo)
        except:
            self.root.ids['PesoScreen'].ids['peso_nuevo'].background_color = (1, 0, 0, 1)
            return

        today = date.today()
        d1 = today.strftime("%d/%m/%Y")


        peso_payload = {"PesoKg": peso_nuevo, "Fecha": d1}
        peso_req = requests.post("https://innpass-62327.firebaseio.com/%s/Pesos.json?auth=%s"
                              % (self.local_id, self.id_token), data=json.dumps(peso_payload))

        W = PesoBanner(PesoKG=peso_nuevo, Fecha=d1)
        peso_grid_banner = self.root.ids['PesoScreen'].ids['peso_grid_banner']
        peso_grid_banner.add_widget(W)

    def add_act(self):
        pantalla = self.root.ids['AddActividadScreen']

        #get data from all fields
        FechaAct = pantalla.ids['FechaAct'].text
        TipoAct = pantalla.ids['TipoAct'].text
        EncargadoAct = pantalla.ids['EncargadoAct'].text
        DescripcionAct = pantalla.ids['DescripcionAct'].text
        #Check fill are not trash

        if FechaAct == "":
            pantalla.ids["FechaAct"].background_color = (1, 0, 0, 1)
            return
        if TipoAct == "":
            pantalla.ids["TipoAct"].background_color = (1, 0, 0, 1)
            return
        if EncargadoAct == "":
            pantalla.ids["EncargadoAct"].background_color = (1, 0, 0, 1)
            return
        #all ok
        print("Todo OK")
        #send data to firebase
        actividad_payload = {"Acti": TipoAct,"Fecha": FechaAct,"Persona": EncargadoAct,"Comentarios": DescripcionAct}
        actividad_req = requests.post("https://innpass-62327.firebaseio.com/%s/Actividades.json?auth=%s"
                                      %(self.local_id, self.id_token), data=json.dumps(actividad_payload))
        print("todo salio bien")

        act_grid_banner = self.root.ids['ActScreen'].ids['act_grid_banner']

        W = ActBanner(Fecha=FechaAct, Acti=TipoAct, Comentarios=DescripcionAct,
                          Persona=EncargadoAct)

        act_grid_banner.add_widget(W)
        self.change_screen("ActScreen")
    def add_perfil(self):
        pantalla = self.root.ids['PerfilScreen']

        # get data from all fields
        Nombre = pantalla.ids['Nombre'].text
        Apellido = pantalla.ids['Apellido'].text
        Tel = pantalla.ids['Telefono'].text
        Dir = pantalla.ids['Direccion'].text
        # Check fill are not trash

        if Nombre == "":
            pantalla.ids["Nombre"].background_color = (1, 0, 0, 1)
            return
        if Apellido == "":
            pantalla.ids["Apellido"].background_color = (1, 0, 0, 1)
            return
        if Dir == "":
            pantalla.ids["Direccion"].background_color = (1, 0, 0, 1)
            return
        try:
            Tel = int(Tel)
        except:
            self.root.ids['PerfilScreen'].ids['Telefono'].background_color = (1, 0, 0, 1)
            return
        # all ok
        print("Todo OK")
        # send data to firebase
        perfil_payload = {"Nombre": Nombre, "Apellido": Apellido, "Dir": Dir, "Tel": Tel}
        perfil_req = requests.patch("https://innpass-62327.firebaseio.com/%s.json?auth=%s"
                                      % (self.local_id, self.id_token), data=json.dumps(perfil_payload))
        print("todo salio bien")
        verperfil = self.root.ids['vPerfilScreen']

        vnombre = verperfil.ids['Nombre']
        vapellido = verperfil.ids['Apellido']
        vtel = verperfil.ids['Telefono']
        vdir = verperfil.ids['Direccion']
        vnombre.text = Nombre
        vapellido.text = Apellido
        vtel.text = str(Tel)
        vdir.text = Dir
        self.change_screen("SettingScreen")

    def add_ID(self,IDs):
        #check if ID exists
        check_rqe = requests.get('https://innpass-62327.firebaseio.com/.json?orderBy="ID"&equalTo=' + IDs)
        print(check_rqe.ok)
        if check_rqe.json() == {}:
            self.root.ids['AddScreen'].ids['add_label'].text = "ID invalido"
        else:
            data = check_rqe.json()
            print(data)
            key = (data.keys())
            temp=list(key)
            print(temp[0])
            pat_ID = data[temp[0]]['ID']
            self.root.ids['AddScreen'].ids['add_label'].text = "Todo Piola"
        #Say success or error
        #Add to friend list
            self.Contactos += ", %s" %pat_ID
            patch_data = '{"Contactos": "%s"}' %self.Contactos
            patch_req = requests.patch("https://innpass-62327.firebaseio.com/" + self.local_id + ".json?auth=" + self.id_token,
                                       data=patch_data)
    def load_pac_screen(self,contact_ID,widget):
        #Get Actividades from paciente ID
        fdata_rqe = requests.get('https://innpass-62327.firebaseio.com/.json?orderBy="ID"&equalTo=' + contact_ID)
        datap = fdata_rqe.json()
        temp = list(datap.values())
        print(temp)
        act_data = temp[0]['Actividades']
        avt_data = temp[0]['avatar']
        pac_act_grid_banner = self.root.ids['PacActScreen'].ids['pac_act_grid_banner']
        #Clean Banner
        for w in pac_act_grid_banner.walk():
            if w.__class__ == ActBanner:
                pac_act_grid_banner.remove_widget(w)

        avatar_image = self.root.ids['PacActScreen'].ids['pac_avatar']
        avatar_image.source = "icon/avatar/" + avt_data
        pactividades = act_data
        print("Actividades todo bien")
        if pactividades != "":
            act_keys = pactividades.keys()


            for act_key in act_keys:
                actividad = pactividades[act_key]
                W = ActBanner(Fecha=actividad['Fecha'], Acti=actividad['Acti'], Comentarios=actividad['Comentarios'],
                              Persona=actividad['Persona'])
                print("Actividad banner")
                pac_act_grid_banner.add_widget(W)
        print("Actividad cargada bien")
        self.change_screen('PacActScreen')

    def load_pac_peso(self,contact_ID,widget):
        #Get Pesos from paciente ID
        fdata_rqe = requests.get('https://innpass-62327.firebaseio.com/.json?orderBy="ID"&equalTo=' + contact_ID)
        fdata_rqe = requests.get('https://innpass-62327.firebaseio.com/.json?orderBy="ID"&equalTo=' + contact_ID)
        datap = fdata_rqe.json()
        temp = list(datap.values())
        print(temp)
        pes_data = temp[0]['Pesos']
        avt_data = temp[0]['avatar']
        pac_peso_grid_banner = self.root.ids['PacPesoScreen'].ids['pac_peso_grid_banner']
        avatar_image = self.root.ids['PacPesoScreen'].ids['pac_peso']
        avatar_image.source = "icon/avatar/" + avt_data
        for w in pac_peso_grid_banner.walk():
            if w.__class__ == PesoBanner:
                pac_peso_grid_banner.remove_widget(w)
        pesos = pes_data
        if pesos != "":


            pesos_keys = pesos.keys()
            for peso_key in pesos_keys:
                peso = pesos[peso_key]
                W = PesoBanner(PesoKG=peso['PesoKg'], Fecha=peso['Fecha'])
                print("Peso banner")
                pac_peso_grid_banner.add_widget(W)
        #Populate screens
        #Change to screen
        self.change_screen('PacPesoScreen')
    def load_pac_perfil(self, contact_ID, widget):
        # Get profile from paciente ID
        fdata_rqe = requests.get('https://innpass-62327.firebaseio.com/.json?orderBy="ID"&equalTo=' + contact_ID)
        datap = fdata_rqe.json()
        temp = list(datap.values())
        print(temp)
        nom_data = temp[0]['Nombre']
        ape_data = temp[0]['Apellido']
        dir_data = temp[0]['Dir']
        tel_data = temp[0]['Tel']
        verperfil = self.root.ids['PacPerfilScreen']

        vnombre = verperfil.ids['Nombre']
        vapellido = verperfil.ids['Apellido']
        vtel = verperfil.ids['Telefono']
        vdir = verperfil.ids['Direccion']
        vnombre.text = str(nom_data)
        vapellido.text = str(ape_data)
        vtel.text = str(dir_data)
        vdir.text = str(tel_data)
        # Populate screens
        # Change to screen
        self.change_screen('PacPerfilScreen')

MainApp().run()
