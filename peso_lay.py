from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.app import App
import kivy.utils

class PesoBanner(GridLayout):
	
	def __init__(self, **kwargs):
		self.rows = 1
		super(PesoBanner, self).__init__()
		
		#Need Left Float
		left = FloatLayout()
		left_label = Label(text=str(kwargs['PesoKG'])+" KG",size_hint=(1,1), pos_hint={"top": 1, "right": 1})
		left.add_widget(left_label)
		
		#Need Left Float
		right = FloatLayout()
		right_label = Label(text=str(kwargs['Fecha']),size_hint=(1,1),pos_hint={"top": 1, "right": 1})
		right.add_widget(right_label)
		
		self.add_widget(left)
		self.add_widget(right)