import datetime
from datetime import date, timedelta
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, ActionExecuted, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.events import Restarted
from rasa_sdk.events import AllSlotsReset
import mysql.connector
import pymysql

import requests
import json
#url = "http://172.16.1.72/webservice-php-json/index.php"

url = "http://45.228.211.133:8080/webservice-php-json/index.php"

global SiPaga
global NoPaga
global motivo
global tipo_contacto
global compromiso_p
global derivacion
global fecha_com
global entrega_info
SiPaga=None
NoPaga=None
motivo=None
tipo_contacto=0
compromiso_p=0
derivacion=None
fecha_com=None
entrega_info=None
"""
(host='10.3.0.5',
                             user='root',
                             password='T3c4dmin1234.',
                             database='asterisk',
                             )

"""
"""
class DataBase:
    def __init__(self):
        self.connection=pymysql.connect(host='10.3.0.5',
                             user='root',
                             password='T3c4dmin1234.',
                             database='asterisk',
                             )
        self.cursor = self.connection.cursor()
        print("Conexion exitosa!")

    def select_user(self, uniqueid):
        sql = "select T0.vendor_lead_code, T0.first_name,T0.address1,T0.lead_id,T0.address2,T0.city,T0.owner,T1.list_name,T0.email,T2.campaign_name from vicidial_list T0 inner join vicidial_lists T1 on T0.list_id=T1.list_id inner join vicidial_campaigns T2 on T1.campaign_id=T2.campaign_id where T0.lead_id ='{}'".format(uniqueid,uniqueid)
        
        try:
            self.cursor.execute(sql)
            user = self.cursor.fetchone()
            global monto
            global nombre
            global fechaVencimiento
            global Campania
            global oferta
            global primernombre
            print("user:",user)
            primernombre = user[1]
            monto = user[4]
            nombre = user[2]
            fechaVencimiento = user[5]
            Campania = user[9]
            oferta = user[8]
            print("user: ", user)
            print("Nombre:" , nombre)
            print("Deuda monto:" , monto)
            print("Campaña: " , Campania)
            print("oferta: " , oferta)
           
              
        except Exception as e:
            raise
    def close(self):
        try:
            self.connection.close()
            print("Sesion cerrada exitosamente!")
            #agi.verbose("Database cerrada exitosamente!")
        except Exception as e:
            raise


class DataBase2:
    def __init__(self):
        self.connection=pymysql.connect(host='45.228.211.131',
                             user='root',
                             password='T3c4dmin1234.',
                             database='asterisk',
                             )
        self.cursor = self.connection.cursor()
        print("Conexion exitosa database2!")


    def tipo_contacto(self,uniqueid):
        sql = "SELECT tipo_contacto, max(fecha_llamada) from bot_movatec where lead_id='{}'".format(uniqueid)
     
        try:
            self.cursor.execute(sql)
            user = self.cursor.fetchone()
            global tipo_contact
            tipo_contact = user[0]
          
        except Exception as e:
            raise 
    def update_user(self,tipo_contacto,motivo,compromiso_p,derivacion,fecha_com,entrega_info,uniqueid):
        sql = "UPDATE bot_movatec SET tipo_contacto='{}',motivo='{}',compromiso_p='{}',derivacion='{}',fecha_com='{}',entrega_info='{}' WHERE lead_id='{}'".format(tipo_contacto,motivo,compromiso_p,derivacion,fecha_com,entrega_info,uniqueid)
      
        
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            raise 
    def close(self):
        try:
            self.connection.close()
            print("Sesion cerrada exitosamente!")
            #agi.verbose("Database cerrada exitosamente!")
        except Exception as e:
            raise

database = DataBase()
database2 = DataBase2()

"""

"""
def variables():
     global fechaVencimiento
     global nombre
     global monto
     fechaVencimiento = "14/01/2021"
     nombre = "Ignacio"
     monto="100000"

variables()
""" 





#ConverterDate()


"""
def llamarDB(uniqueid):
    #database = DataBase()
    database.select_user(uniqueid)

def progreso(tipo_contacto,motivo,compromiso_p,derivacion,fecha_com,entrega_info,uniqueid):
    #database = DataBase()
    database2.update_user(tipo_contacto,motivo,compromiso_p,derivacion,fecha_com,entrega_info,uniqueid)

def TipoContacto(uniqueid):
    #database = DataBase()
    database2.tipo_contacto(uniqueid)
"""

def Querys(uniqueid):
        payload={'action': 'get','id': f'{uniqueid}'}
        files=[
        ]
        headers = {}
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        my_bytes_value = response.content
        my_new_string = my_bytes_value.decode("utf-8").replace("'", '"')
        data = json.loads(my_new_string)
        s = json.dumps(data, indent=4, sort_keys=True)
        print(s)
        global nombre
        global monto
        global fechaVencimiento
        global primernombre
        global rut
        global campania
        nombre=data["data"][0]["address1"]
        monto=data["data"][0]["address2"]
        fechaVencimiento=data["data"][0]["city"]
        primernombre=data["data"][0]["first_name"]
        rut=data["data"][0]["vendor_lead_code"]
        campania=data["data"][0]["campaign_name"]

"""
            "address1": "DANIELA HERNANDEZ",
            "address2": "26799",
            "campaign_name": "CLICK RECORDATORIO",
            "city": "28-02-21",
            "email": "",
            "first_name": "DANIELA",
            "lead_id": "134",
            "list_name": "CLICK RECORDATORIO",
            "owner": "78574270",
            "vendor_lead_code": "170099999"
"""

def Updates(tipo_contacto,motivo,compromiso_p,derivacion,fecha_com,entrega_info,lead_id,rut):
          payload={'action': 'update',
          'tipo_contacto': f'{tipo_contacto}',
          'motivo': f'{motivo}',
          'compromiso_p': f'{compromiso_p}',
          'derivacion': f'{derivacion}',
          'fecha_com': f'{fecha_com}',
          'entrega_info': f'{entrega_info}',
          'lead_id': f'{lead_id}',
          'rut': f'{rut}'}
          files=[
          ]
          headers = {}
          response = requests.request("POST", url, headers=headers, data=payload, files=files)
          print(response.text)

def month_converter(i):
       month = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
       return month[i-1]


def ConverterDate():
     global mes
     global dia
     global anio
     global nombreMes 
     dia=int(fechaVencimiento[0:2])
     mes=int(fechaVencimiento[3:5])
     anio=int(fechaVencimiento[6:10])
     nombreMes=month_converter(mes)
     print("dia: ",dia)
     print("mes: ",nombreMes)
     print("año: ",anio)


class ActionHello(Action):
    def name(self):
        return "action_hello"

    def run(self, dispatcher, tracker, domain):
        #global database
        #global database2
        #database = DataBase()
        #database2 = DataBase2()
        global uniqueid
        uniqueid = tracker.sender_id
        Querys(uniqueid)
        #llamarDB(uniqueid)
        #progreso(7,motivo,compromiso_p,derivacion,fecha_com,"No",uniqueid)
        Updates(7,motivo,compromiso_p,derivacion,fecha_com,"No",uniqueid,rut)
        t = datetime.datetime.now()
        if 23 >= int(t.hour) >= 12:
             dispatcher.utter_message(f'Buenas tardes, ¿Hablo con {nombre}?')
        else:
             dispatcher.utter_message(f'Buenos días, ¿Hablo con {nombre}?')
           
           
        return []
           

class ActionHello2(Action):
    def name(self):
        return "action_hello2"

    def run(self, dispatcher, tracker, domain):
        global uniqueid
        uniqueid = tracker.sender_id
        #print("uniqueid: ", tracker.sender_id)
        #llamarDB(uniqueid)
        Querys(uniqueid)
        #progreso(7,motivo,compromiso_p,derivacion,fecha_com,"No",uniqueid)
        Updates(7,motivo,compromiso_p,derivacion,fecha_com,"No",uniqueid,rut)
        dispatcher.utter_message(f'Disculpe, Me comunico con {primernombre}?')
        return []


###########################################################
################### Pregunta Principal ####################
###########################################################

class ActionQuestion(Action):
    def name(self):
        return "action_ask_question"

    def run(self, dispatcher, tracker, domain):
        #database = DataBase()
        global uniqueid
        uniqueid = tracker.sender_id
        Querys(uniqueid)
        #llamarDB(uniqueid)
        #progreso(1,motivo,compromiso_p,derivacion,fecha_com,"No",uniqueid)
        Updates(1,motivo,compromiso_p,derivacion,fecha_com,"No",uniqueid,rut)
        ConverterDate()
        dispatcher.utter_message(f'{primernombre}, Le recordamos que se encuentra disponible el pago de su cuota que vence el {fechaVencimiento} en nuestro sitio web, triple doble b .tarjetacencosud punto cl. Para mayor información, llamar al fono 223637830, entre 8  45 horas a 18  45 horas, de lunes a viernes, y sábados desde 9:00  a 14:00 horas. Le informamos que esta conversación fue grabada por su seguridad, muchas gracias. | EXIT') 
        #progreso(2,motivo,compromiso_p,derivacion,fecha_com,"Si",uniqueid)
        Updates(2,motivo,compromiso_p,derivacion,fecha_com,"Si",uniqueid,rut)
        return []

#{dia} de {nombreMes} del  dosmil {anio}       
################################################
################### Si paga ####################
################################################

class ActionSiPaga(Action):
    def name(self):
        return "action_no_paga"

    def run(self, dispatcher, tracker, domain):
        global uniqueid
        uniqueid = tracker.sender_id
        #llamarDB(uniqueid)
        Querys(uniqueid)
        #progreso(4,motivo,4,derivacion,fecha_com,"Si",uniqueid)
        Updates(4,motivo,4,derivacion,fecha_com,"Si",uniqueid,rut)
        dispatcher.utter_message(f"Disculpe las molestias. Muchas gracias | EXIT")
        
        return []



###############################################
################### Restart ###################
###############################################

class ActionRestart2(Action):
    """Resets the tracker to its initial state.
    Utters the restart template if available."""

    def name(self) -> Text:
        return "action_restart2"

    async def run(self, dispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [Restarted()]

class ActionSlotReset(Action):  
    def name(self):         
        return 'action_slot_reset'  
    def run(self, dispatcher, tracker, domain):
        return[AllSlotsReset()]


class ActionQuestion2(Action):
    def name(self):
        return "action_ask_question2"

    def run(self, dispatcher, tracker, domain):
     
       dispatcher.utter_message(f'Disculpe le haré la pregunta nuevamente')
       return []

class ActionConoce(Action):
    def name(self):
        return "action_quien"

    def run(self, dispatcher, tracker, domain):
        database = DataBase()
        global uniqueid
        uniqueid = tracker.sender_id
        Querys(uniqueid)
        #llamarDB(uniqueid)
        dispatcher.utter_message(f'{nombre}?')
        return []
