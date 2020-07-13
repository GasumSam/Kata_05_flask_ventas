from flask import Flask
from flask_testing import TestCase
import run    #La creación de la app me la he llevado a run, así que importo

class TestFlaskBase(TestCase):
    def create_app(self):
        self.app = run.app   #creo la aplicación y me la guardo para poder usarla en otros métodos
        return run.app

    def setUp(self):  #En el método setUp creábamos la pantalla, la empaquetñabamos y esperábamos para vsualizarla
        self.client = self.app.test_client()
        self.client.testing = True 




    def tearDown(self):   #Tras setUp, para salir del test se aplica tearDown
        pass