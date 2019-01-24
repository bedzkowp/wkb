from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from soib import beta
from kivy.clock import Clock
import matplotlib.pyplot as plt
from numpy import linspace as linspace
import math

class Display(BoxLayout):
    pass

class LoginScreen(GridLayout):

    def n(self,r,a,g,delta,n1):
        if r >=0 and r <= a:
          return n1 * math.sqrt(1 - 2 * delta * ((r / a)**g))
        else:
          return n1 * math.sqrt(1 - 2 * delta)

    def popUp(self, _text, _width=300):
        layout = GridLayout(cols=1)
        layout.add_widget(Label(text=_text))
        btnClose = Button(text="Zamknij")
        layout.add_widget(btnClose)
        
        popup = Popup(title="UWAGA!", content=layout,size_hint=(None,None), size=(_width,200),auto_dismiss=False)
        btnClose.bind(on_press=popup.dismiss)
        popup.open()

    def isFilled(self,instance):
        is_filled_good = True
        if(len(self.m.text) == 0 or len(self.p.text) == 0 or len(self.g.text) == 0 or len(self.n1.text)==0 or len(self.NA.text)==0 or len(self.clad_d.text)==0 or len(self.core_d.text)==0 or len(self.l.text)==0):

            self.popUp("Prosze podać wszystkie parametry!")
            
        else:
            m = int(self.m.text)
            p = int(self.p.text)
            g = float(self.g.text)
            n1 = float(self.n1.text)
            NA = float(self.NA.text)
            core_d = float(self.core_d.text)/10**6
            clad_d = float(self.clad_d.text)/10**6
            l = float(self.l.text)/10**9

            if not(m >= 0):
                self.popUp("Zła wartość m!")
                is_filled_good = False
            if not(p >= 1):
                self.popUp("Zła wartość p!")
                is_filled_good = False 
            if not(NA >= 0):
                self.popUp("Proszę podać aperture numeryczną > 0",400)
                is_filled_good = False 
            if (core_d > clad_d):
                self.popUp("Średnica rdzenia nie może być większa niż średnica płaszcza!",500)
                is_filled_good = False

            if is_filled_good == True:
                try:
                    B = beta(NA, g, n1, l, core_d, clad_d, m, p)
                    self.B.text = str(round(B['b']/10**6,3))				
                except ValueError:
                    self.popUp("Złe parametry!")
                    self.B.text = "Proszę podać odpowiednie parametry!"
			

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        
        self.cols = 2
        
        self.add_widget(Label(text="m:"))
        self.m = TextInput(multiline=False)
        self.add_widget(self.m)
        
        self.add_widget(Label(text="p:"))
        self.p = TextInput(multiline=False)
        self.add_widget(self.p)

        self.add_widget(Label(text="g - wykładnik profilu wspołczynnika załamania:"))
        self.g = TextInput(multiline=False)
        self.add_widget(self.g)

        self.add_widget(Label(text="n1 - współczynnik załamania rdzenia:"))
        self.n1 = TextInput(multiline=False)
        self.add_widget(self.n1)

        self.add_widget(Label(text="NA - apertura numeryczna:"))
        self.NA = TextInput(multiline=False)
        self.add_widget(self.NA)

        self.add_widget(Label(text="srednica rdzenia [um]:"))
        self.core_d = TextInput(multiline=False)
        self.add_widget(self.core_d)

        self.add_widget(Label(text="srednica płaszcza [um]:"))
        self.clad_d = TextInput(multiline=False)
        self.add_widget(self.clad_d)

        self.add_widget(Label(text="długość fali [nm]:"))
        self.l = TextInput(multiline=False)
        self.add_widget(self.l)

        self.add_widget(Button(text="Oblicz wartość stałej propagacji B [rad/um]", on_press=self.isFilled))
        self.B = TextInput(readonly=True)
        self.add_widget(self.B)

class Screen_One(Screen):
    def __init__(self, **kwargs):
        super(Screen_One, self).__init__(**kwargs)
        LoginLayout = LoginScreen()
        self.add_widget(LoginLayout)

class SOIBApp(App):
    def build(self):
        return Display()

if __name__ == '__main__':
    SOIBApp().run()
		


