# importar o App,
# importar Builder (GUI), interface
# criar o app
# criar a função build

from kivy.app import App

from kivy.lang import Builder

GUI = Builder.load_file("tela.kv")



class MeuAplicativo(App):
      def build(self):
            return GUI
