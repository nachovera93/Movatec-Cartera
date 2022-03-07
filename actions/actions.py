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

class DataBase:
    def __init__(self):
        self.connection=pymysql.connect(host='45.225.92.195',
                             user='cron',
                             password='T3c4dmin1234.',
                             database='asterisk',
                             )
        self.cursor = self.connection.cursor()
        print("Conexion exitosa!")

    def select_user(self, uniqueid):
        sql = "select T0.vendor_lead_code, T0.first_name,T0.address1,T0.lead_id,T0.address2,T0.city,T0.owner,T1.list_name,T0.email,T2.campaign_name from vicidial_list_archive T0 inner join vicidial_lists T1 on T0.list_id=T1.list_id inner join vicidial_campaigns T2 on T1.campaign_id=T2.campaign_id where T0.lead_id ='{}' union ALL select T0.vendor_lead_code, T0.first_name,T0.address1,T0.lead_id,T0.address2,T0.city,T0.owner,T1.list_name,T0.email,T2.campaign_name  from vicidial_list T0 inner join vicidial_lists T1 on T0.list_id=T1.list_id inner join vicidial_campaigns T2 on T1.campaign_id=T2.campaign_id where T0.lead_id ='{}'".format(uniqueid,uniqueid)
        
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
            """
            global mes
            global dia
            global anio
            global nombreMes 
            dia=int(fechaVencimiento[0:2])
            mes=int(fechaVencimiento[3:5])
            anio=int(fechaVencimiento[6:10])
            nombreMes=month_converter(mes-1)
            print("dia: ",dia)
            print("mes: ",nombreMes)
            print("año: ",anio)
            """
              
        except Exception as e:
            raise
    def tipo_contacto(self,uniqueid):
        sql = "SELECT tipo_contacto, max(fecha_llamada) from bot_movatec where lead_id='{}'".format(uniqueid)
       # sql = "UPDATE usuarios SET name='{}' WHERE id = {}".format(name,id)
        try:
            self.cursor.execute(sql)
            user = self.cursor.fetchone()
            global tipo_contact
            tipo_contact = user[0]
          
        except Exception as e:
            raise 
    def update_user(self,tipo_contacto,razon,compromiso_p,derivacion,fecha_com,entrega_info,uniqueid):
        sql = "UPDATE bot_movatec SET tipo_contacto='{}',motivo='{}',compromiso_p='{}',derivacion='{}',fecha_com='{}',entrega_info='{}' WHERE lead_id='{}'".format(tipo_contacto,razon,compromiso_p,derivacion,fecha_com,entrega_info,uniqueid)
       # sql = "UPDATE usuarios SET name='{}' WHERE id = {}".format(name,id)
        
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
     nombreMes=month_converter(mes-1)
     print("dia: ",dia)
     print("mes: ",nombreMes)
     print("año: ",anio)


#ConverterDate()



def llamarDB(uniqueid):
    #database = DataBase()
    database.select_user(uniqueid)

def progreso(tipo_contacto,razon,compromiso_p,derivacion,fecha_com,entrega_info,uniqueid):
    #database = DataBase()
    database.update_user(tipo_contacto,razon,compromiso_p,derivacion,fecha_com,entrega_info,uniqueid)

def TipoContacto(uniqueid):
    #database = DataBase()
    database.tipo_contacto(uniqueid)

class ActionHello(Action):
    def name(self):
        return "action_hello"

    def run(self, dispatcher, tracker, domain):
      
        global uniqueid
        uniqueid = tracker.sender_id
        llamarDB(uniqueid)
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
        #database = DataBase()
        global uniqueid
        uniqueid = tracker.sender_id
        #print("uniqueid: ", tracker.sender_id)
        llamarDB(uniqueid)
        progreso(7,razon,compromiso_p,derivacion,fecha_com,"No",uniqueid)
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
        llamarDB(uniqueid)
        ConverterDate()
        dispatcher.utter_message(f'{primernombre}, Le recordamos que se encuentra disponible el pago de su cuota que vence el {dia} de {nombreMes} del {anio} en nuestro sitio web, triple doble b .tarjetacencosud punto cl. Para mayor información, llamar al fono 223637830 entre: 8 y 45 horas a 18 y 45 horas, de Lunes a Viernes, y Sábados desde 9:00  a 14:00 horas. Le informamos que esta conversación fue grabada por su seguridad, muchas gracias. | EXIT') 
           
        return []

       
################################################
################### Si paga ####################
################################################

class ActionSiPaga(Action):
    def name(self):
        return "action_no_paga"

    def run(self, dispatcher, tracker, domain):
        
        dispatcher.utter_message(f"Disculpe las molestias. Muchas Gracias | EXIT")
        
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
        llamarDB(uniqueid)
        dispatcher.utter_message(f'{nombre}?')
        return []
