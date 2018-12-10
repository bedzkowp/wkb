from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from soib import beta
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

    def plotN(self, instance):
        if(len(self.m.text) == 0 or len(self.p.text) == 0 or len(self.g.text) == 0 or len(self.n1.text)==0 or len(self.NA.text)==0 or len(self.clad_d.text)==0 or len(self.core_d.text)==0 or len(self.l.text)==0):
            layout = GridLayout(cols=1)
            layout.add_widget(Label(text="Proszę podać wszystkie parametry!"))
            btnClose = Button(text="Zamknij")
            layout.add_widget(btnClose)

            popup = Popup(title="UWAGA!", content=layout,size_hint=(None,None), size=(300,200),auto_dismiss=False)
            btnClose.bind(on_press=popup.dismiss)
            popup.open()
        else:
            m = int(self.m.text)
            p = int(self.p.text)
            g = int(self.g.text)
            n1 = float(self.n1.text)
            NA = float(self.NA.text)
            core_d = float(self.core_d.text)
            clad_d = float(self.clad_d.text)
            l = float(self.l.text)
            delta = (NA**2)/(2*(n1**2))
            clad_r = clad_d/2
            a = core_d/2
            r_vec = linspace(0,clad_r)
            n_vec = []
            
            for r in r_vec:
                n_vec.append(self.n(r,a, g, delta, n1))

            plt.plot(r_vec,n_vec)
            plt.xlabel("odległość od środka światłowodu - r [m]")
            plt.ylabel("wartość współczynnika załamania - n")
            plt.title("Wykres współczynnika załamania od odległości od środka światłowodu")
            plt.grid(True)
            plt.show()
    
    def plotB(self, instance):
        if(len(self.m.text) == 0 or len(self.p.text) == 0 or len(self.g.text) == 0 or len(self.n1.text)==0 or len(self.NA.text)==0 or len(self.clad_d.text)==0 or len(self.core_d.text)==0):
            layout = GridLayout(cols=1)
            layout.add_widget(Label(text="Proszę podać wszystkie parametry!"))
            btnClose = Button(text="Zamknij")
            layout.add_widget(btnClose)
            
            popup = Popup(title="UWAGA!", content=layout,size_hint=(None,None), size=(300,200),auto_dismiss=False)
            btnClose.bind(on_press=popup.dismiss)
            popup.open()
        else:
            m = int(self.m.text)
            p = int(self.p.text)
            g = int(self.g.text)
            n1 = float(self.n1.text)
            NA = float(self.NA.text)
            core_d = float(self.core_d.text)
            clad_d = float(self.clad_d.text)
            
            delta = (NA**2)/(2*(n1**2))
            clad_r = clad_d/2
            a = core_d/2
            l_vec = linspace(600e-9,1200e-9, 20)
            l_vec2 = linspace(600,1200,20)
            b_vec = []
            for l in l_vec:
                ko = (2 * math.pi) / l 
                b_vec.append(beta(NA,g, n1,l, core_d, clad_d,m,p)['b']/ko)
                
            plt.plot(l_vec2,b_vec)
            plt.xlabel("długość fali - [nm]")
            plt.ylabel("B/ko")
            plt.title("Wykres B/ko w zależności od długości fali")
            plt.grid(True)
            plt.show()
	
	
    def isFilled(self,instance):
        
        if(len(self.m.text) == 0 or len(self.p.text) == 0 or len(self.g.text) == 0 or len(self.n1.text)==0 or len(self.NA.text)==0 or len(self.clad_d.text)==0 or len(self.core_d.text)==0 or len(self.l.text)==0):
            layout = GridLayout(cols=1)
            layout.add_widget(Label(text="Proszę podać wszystkie parametry!"))
            btnClose = Button(text="Zamknij")
            layout.add_widget(btnClose)

            popup = Popup(title="UWAGA!", content=layout,size_hint=(None,None), size=(300,200),auto_dismiss=False)
            btnClose.bind(on_press=popup.dismiss)
            popup.open()
        else:
            m = int(self.m.text)
            p = int(self.p.text)
            g = int(self.g.text)
            n1 = float(self.n1.text)
            NA = float(self.NA.text)
            core_d = float(self.core_d.text)
            clad_d = float(self.clad_d.text)
            l = float(self.l.text)
            
            B = beta(NA, g, n1, l, core_d, clad_d, m, p) 
            self.B.text = str(B['b'])
        
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

        self.add_widget(Label(text="srednica rdzenia:"))
        self.core_d = TextInput(multiline=False)
        self.add_widget(self.core_d)

        self.add_widget(Label(text="srednica płaszcza:"))
        self.clad_d = TextInput(multiline=False)
        self.add_widget(self.clad_d)

        self.add_widget(Label(text="długość fali:"))
        self.l = TextInput(multiline=False)
        self.add_widget(self.l)

        self.add_widget(Button(text="Oblicz wartość stałej propagacji B", on_press=self.isFilled))
        self.B = TextInput(readonly=True)
        self.add_widget(self.B)

        self.add_widget(Button(text="Wykres współczynnika zał.", on_press= self.plotN))
        #self.B = TextInput(readonly=True)
        #self.add_widget(self.B)
        self.add_widget(Button(text="Wykres stałej propagacji B", on_press= self.plotB))
        
            
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
		


