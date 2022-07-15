#Se importa flask como framework
from flask import Flask, jsonify
#Se como libreria https
import requests
#Se importa para manipular horas y fechas
from datetime import date
from datetime import datetime
#Se importa para usar comandos de sistema
import os
#Se cargar el .env file
from dotenv import load_dotenv

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

#Funcion con distintos mensajes de respuesta segun la situacion
def resposestatus(type):
    response = ""
    match type:
        case 1:
            response ={
                "message": "Solo valores entre 1 y 500"
                }
            return response
        case 2:
            response ={
            "message": "Solo datos numericos"
            }
            return response
        case 3:
            response ={
            "message": "Internal server error"
            }
            return response
        case _:
            response ={
            "message": "Internal server error"
            }
            return response

#Funcion para consumir una api de tipo get
def callrestget(url):
    try:
        Callresponse = requests.get(url, timeout=500000)
        if Callresponse.status_code == 200:
                return Callresponse
        elif  Callresponse.status_code == 500:
            return resposestatus(3)
    except Exception as err:
        print(str(err))
        
#Se declara el end-point
@app.route('/cat-facts/<number>', methods = ['GET'])
def getdatacats(number):
    CallresponseArray = []
    current_year = date.today().year
    try:
        #Se valida si el tipo de dato es numerico
        if (number.isnumeric()):
            #Se valida si el dato se encuentra entre 1 y 500
            if (int(number) >= 1 and int(number) <= 500):
                #Se consume la api cat-fact
                catFactUrl = os.getenv('CAT-FACTURL')
                Callresponse = callrestget(catFactUrl + str(number))
                #Se valida el codigo de respuesta
                if (Callresponse.status_code == 200):
                    #Se convierte a json
                    data = Callresponse.json()
                    #Se recorre el json de respuesta
                    for position in data:
                        #Se convierte cada fecha dentro de cada position al formato de solo el año
                        date_time_obj = datetime.strptime(position['updatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        #print("El año es " + str(date_time_obj.year))
                        #Se valida si el año corresponde al actual de ser así se hace push al nuevo json de respuesta, si no, se omite.
                        if (date_time_obj.year == current_year):
                            CallresponseArray.append(position)
                    return jsonify(CallresponseArray), 200
            else:
                #Si no se encuentra en el rango se retorna json
                return jsonify(resposestatus(1)), 406
        else:
            #Si el valor no es numerico se retorna json
            return jsonify(resposestatus(2)), 406
        
    except Exception as err:
        print(str(err))
        return jsonify(resposestatus(3)), 500
if __name__ == '__main__':
    #Carga las variables de entorno
    load_dotenv()
    app.run(debug=False, host='0.0.0.0', port=os.getenv('PORT'),threaded=True)
        
        
