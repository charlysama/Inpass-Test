import requests
import json
from kivy.app import App
from json import dumps
import sys
from kivy.network.urlrequest import UrlRequest
class MyFire():
    wak = "AIzaSyBlQmAG-mSVueERGgVPWasOaJEOUVjyfPM" #Api de my database
    debug = True
    def sign_up(self,email,password):
        app = App.get_running_app()
        print("sign up")
        #send email and password
        #Recibo localID, authToken and refreshToken
        signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + self.wak
        sign_up_payload = {"email": email, "password":password, "returnSecureToken": True}
        sign_up_request = requests.post(signup_url,data=sign_up_payload)
        print("ok")
        sign_up_data=json.loads(sign_up_request.content.decode())

        if sign_up_request.ok == False:
            error_data = json.loads(sign_up_request.content.decode())
            error_message = error_data["error"]["message"]
            print(error_message)
            app.root.ids['LoginScreen'].ids['login_message'].text = error_message.replace("_", " ")

        if sign_up_request.ok == True:
            refresh_token=sign_up_data['refreshToken']
            localID = sign_up_data['localId']
            idToken = sign_up_data['idToken']

            #Save refreshtoken to a file
            with open("refresh_token.txt","w") as f:
                f.write(refresh_token)
            #Save localID to variable in mainapp class
            app.local_id=localID
            #Save idtoken in main app classv
            app.id_token=idToken
            #Create new key in database from localID
            #get friend id
            next_ID_req=requests.get("https://innpass-62327.firebaseio.com/next_ID.json?auth=" + idToken)
            ID = next_ID_req.json()
            print(ID)
            id_patch_data = '{"next_ID": %s}' % str(ID+1)

            Id_patch = requests.patch("https://innpass-62327.firebaseio.com/.json?auth=" + idToken,
                                      data=id_patch_data)

            my_data = '{"avatar": "man.png","Contactos":"","Pesos":"","Actividades":"","Nombre":"","Apellido":"","Tel":"","Dir":"","ID":%s}'%ID
            requests.patch("https://innpass-62327.firebaseio.com/" + localID + ".json?auth" + idToken,
                       data=my_data)
            app.change_screen("HomeScreen")
            
        pass

    def exchange_refresh_token(self,refresh_token):
        refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.wak
        refresh_payload = '{"grant_type": "refresh_token", "refresh_token": "%s"}' % refresh_token
        refresh_req = requests.post(refresh_url, data=refresh_payload)
        print("Refresh A-Ok",refresh_req.ok)
        print(refresh_req.json())

        local_id = refresh_req.json()['user_id']
        id_token = refresh_req.json()['id_token']
        return id_token, local_id

    def sign_in(self,email,password):
        """Called when the "Log in" button is pressed.
        app = App.get_running_app()
        Sends the user's email and password in an HTTP request to the Firebase
        Authentication service.
        """
        app = App.get_running_app()
        if self.debug:
            print("Attempting to sign user in: ", email, password)
        sign_in_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + self.wak
        sign_in_payload = dumps(
            {"email": email, "password": password, "returnSecureToken": True})

        UrlRequest(sign_in_url, req_body=sign_in_payload,
                   on_success=self.successful_login,
                   on_failure=self.sign_in_failure,
                   on_error=self.sign_in_error)
    def sign_in_failure(self, urlrequest, failure_data):
        """Displays an error message to the user if their attempt to create an
        account was invalid.
        """
        app = App.get_running_app()
        print(failure_data)
        # Check if the error msg is the same as the last one

        if self.debug:
            print("Couldn't sign the user in: ", failure_data)

        error_message = failure_data["error"]["message"]
        print(error_message)
        app.root.ids['LoginScreen'].ids['login_message'].text = error_message.replace("_", " ")
        return
    def sign_in_error(self, *args):
        app = App.get_running_app()
        if self.debug:
            print("Sign in error", args)

        error_message = "error"
        print(error_message)
        app.root.ids['LoginScreen'].ids['login_message'].text = error_message
        return
    def successful_login(self, urlrequest, log_in_data):
        """Collects info from Firebase upon successfully registering a new user.
        """
        app = App.get_running_app()
        app.refresh_token = log_in_data['refreshToken']
        app.local_id = log_in_data['localId']
        app.id_token = log_in_data['idToken']
        # Save refreshtoken to a file
        with open("refresh_token.txt", "w") as f:
            f.write(app.refresh_token)
        if self.debug:
            print("Successfully logged in a user: ", log_in_data)
        app.empieza()