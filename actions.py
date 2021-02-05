# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message("Hello World!")
#
#         return []

# *********************************************************************************



# https://legacy-docs.rasa.com/docs/core/_modules/rasa_core/actions/action/
# https://rasa.com/docs/action-server/next/actions#tracker
# https://blog.rasa.com/how-to-migrate-your-assistant-to-rasa-x-the-easy-way/
# https://rasa.com/docs/rasa/next/forms
# https://www.youtube.com/watch?v=9POI7LiKH_8
# https://blog.rasa.com/how-to-build-your-first-rasa-form/


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

#import zeep
from typing import Text, List, Any, Dict
import requests
from rasa_sdk import Action, Tracker # Esto está definico en el archivo interfaces.py
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import formAction
#from rasa.core.actions.action actions

#import pandas as pd
import sys

import requests
from requests.auth import HTTPDigestAuth
import json
#import jwt
from datetime import timezone
import time
import datetime
from calendar import timegm

import pandas as pd


class AliadosComerciales(formAction):
    """ Accesa DB de Aliados Comerciales.
        Accion Forma personalizada que llena todos los slots para encontrar un aliado comercial
    """
    
    def name(self) -> Text:
        # Identificador unico de la forma
        
        return "forma_aliados_comerciales" # nombre de accion definido en el archivo domain
    
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """ Una lista de Slots que la Forma tiene que completar.
            Este método es obligatorio.
            Si aun falta algun solot, la Policy de Forma continuara prediciendo la Accion Forma, y el assistente le seguira pidiendo al usuario estos datos
         """
        
        return ["ubicacion", "numero_cuenta"]
    
    def slot_mappings(self) -> Dict[Text, Any]:
        
        """Metodo opcional. 
        Algunos slots necesarios pueden venir desde entradas de usuario muy diferentes, las cuales naturalmente tendran diferentes intenciones o etiquetas de entidad. 
        Por defecto Form Actions llenará los slots requeridos usando los valores de los slots con exactamente los mismos nombres.
        Slot_mappings me permite definir como los valores desde otras intenciones o entidades pueden ser mapeados a los slots requeridos especificos.
        En nuestro caso los nombres de los slots requeridos coinciden los nombres de las correspondientes entidades, pero tambien podemos especificar desde cuales intenciones aquellos valores vienen.
        
        """
        
        return{ "ubicacion" : self.from_entity(entity: "ubicacion",
                                              intent: ["informacion_aliados_comerciales",
                                                       "explicacion_financiaciones"]),
               "numero_cuenta" : self.from_entity(entity: "numero_cuenta",
                                                 intente: ["informacion_aliados_comerciales",
                                                       "explicacion_financiaciones"])         
                      
        }
    
    
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        
        """
        Finalmente, debemos definir que pasa cuando todos los slots requeridos son proporcionados.
        """
        
        # rastreador de estado para el usuario actual. Accesamos los valores de los slot.
        numero_cuenta_usuario = tracker.get_slot('numero_cuenta') #pasamos el nombre del slot que estamos accesando
        ubicacion = tracker.get_slot('ubicacion')
        
        results = EncontrarAliadoComercial
        if len(results) == 0:
            dispatcher.utter_message(
            "Lo siento, no pudimos encontrar un Aliado Comercial en {} para la cuenta {}.".format(ubicacion.title(),
                                                                                                 numero_cuenta_usuario))
            return []
        
        # limita el numero de resultados a 3
        for r in results[:3]
    
    
    def run(self, dispatcher, tracker, domain):
        

        

        
        if not consulta["IsOk"]:
            respuesta = "La Cuenta {} no tiena datos asociados".format(numero_cuenta_usuario)
        
        if not ubicacion:
            conexion = WebService()
            conexion.autenticacion()
            consulta = conexion.solicitud(numero_cuenta_usuario, "Cliente")
            ubicacion = consulta['NombreMunicipio']
            
        
        
        
        db_aliado = pd.read_excel('Relacion_aliados_comerciales.xlsx', sheet_name='Hoja1')
        
        print(db_aliado.head())
        
        
        
        data = db_aliado[db_aliado['MUNICIPIO'] == ubicacion]
        
        
        
        respuesta = "Los Aliados Comerciales a la cuenta {} son:\n{}".format(numero_cuenta_usuario, data)
        dispatcher.utter_message(respuesta)
        
        return [SlotSet("numero_cuenta", numero_cuenta_usuario)]
        
    
    




    
    
