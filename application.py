from crypt import methods
from distutils.log import debug
from os import abort
import string
from flask import Flask, render_template, request, jsonify, redirect
from flask_restful import Api, Resource
import pandas as pd
import requests
from mixpanel import Mixpanel

# Mixpanel Project Token DEV
mp = Mixpanel('5ea691d11e2276f51ab859aa948fc87c')

# Mixpanel Project Token PROD
# mp = Mixpanel('603e3712797aada25b4b89647598af80')

# Credenciales Sheets de Usuarios
sheet_id = '1Jd6H3m13cWzyhJLlNYkCmyMebrVEpjeGhWeT837hucA'


#Constantes
# URL_BASE = 'http://localhost/'
# URL_API = 'http://localhost/api/rut/'
URL_BASE = 'http://localhost:5000/'
URL_API = 'http://localhost:5000/api/rut/'
VIMEO_URL = 'https://vimeo.com/event/2090053/embed'
ZOOM_URL = 'https://us02web.zoom.us/j/87375674909?pwd=YmdKNk8rYThJb3hzLzkyU1Awejc0dz09'
WSP_URL = 'https://wa.me/56942989805'
CHAT_VIMEO = 'https://vimeo.com/event/2090053/chat/'


# static_folder: indica la nueva carpeta de statics y con 
# static_url_path puedo especificar cual es la raiz de static 
# o sea podría no tener prefico static, util para cuando trabajamos con plantillas webflow o brizi


application = Flask(__name__, static_folder='templates', static_url_path='')

#application = Flask(__name__)



#Api

class All(Resource):

    def get(self):
        df = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv')
        records = df.to_dict(orient='records')
        return records

class Rut(Resource):
    def get(self, value):
        df = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv')
        records = df.to_dict(orient='records')
        for obj in records:
            try:
                if obj['PEGAR RUT'].lower().startswith( value.lower() ):
                    return obj
            except:
                return 'Rut no encontrado'       


#rutas
api = Api(application)
api.add_resource(All, '/api/')
api.add_resource(Rut, '/api/rut/<string:value>')

# data = []
#Rutas Frontend

@application.route("/")
def index():
    return render_template('login.html', wspurl=WSP_URL)

@application.route("/evento")
def evento():
    formRut = request.args.get('rut')
    req = requests.get(url=URL_API+'{}'.format(formRut))
    resp = req.json()
    if resp == 'Rut no encontrado':
        mp.track(formRut.lower(), 'Login Fallido',{
        'Ingreso': 'Login Oficial'
        })
        return render_template('error.html')
    else:
        # traking mixpanel set datos usuario
        mp.people_set(resp['PEGAR RUT'].lower(), {
        '$first_name'    : resp['NOMBRE COMPLETO'].upper(),
        '$rut'     : resp['PEGAR RUT'].lower(),
        'Afiliado'  : resp['Tipo de afiliado'].upper()
        })
        # trak mp set evento
        mp.track(resp['PEGAR RUT'].lower(), 'Login Exitoso',{
        'Carton 1': resp['CARTON 1'],
        'Carton 2': resp['CARTON 2']
        })
        return render_template('evento.html', data=resp, zoomurl=ZOOM_URL, wspurl=WSP_URL, vimeourl=VIMEO_URL, chatvimeo=CHAT_VIMEO)
        
    

@application.route("/cartones")
def cartones():
    rut = request.args.get('rut')
    c1 = request.args.get('c1')
    c2 = request.args.get('c2')

    mp.track(rut.lower(), 'Entrada vía Zoom',{
        'Carton 1': c1,
        'Carton 2': c2
    })
    return render_template('cartones.html',rut=rut, c1=c1, c2=c2, zoomurl=ZOOM_URL, wspurl=WSP_URL, vimeourl=VIMEO_URL, chatvimeo=CHAT_VIMEO)

@application.route("/error")
def error():
    return render_template('error.html')

@application.errorhandler(404)
def notfound(error):
    return render_template('404.html'), 404

@application.route("/login2")
def testLogin():
    return render_template('login2.html')

@application.route("/vivo")
def vivo():
    rut = request.args.get('rut')
    c1 = request.args.get('c1')
    c2 = request.args.get('c2')

    mp.track(rut.lower(), 'Entrada vía Vimeo',{
        'Carton 1': c1,
        'Carton 2': c2
    })
    return render_template('vivo.html', rut=rut, c1=c1, c2=c2, zoomurl=ZOOM_URL, wspurl=WSP_URL, vimeourl=VIMEO_URL, chatvimeo=CHAT_VIMEO)
 
# Esta ruta hace la consulta al WS para entrar directo al envivo, para pruebas de admin ya que no deja estadisticas en mixpanel
@application.route("/directo")
def directo():
    formRut = request.args.get('rut')
    req = requests.get(url=URL_API+'{}'.format(formRut))
    return render_template('directo.html', data=req.json(), zoomurl=ZOOM_URL, wspurl=WSP_URL, vimeourl=VIMEO_URL, chatvimeo=CHAT_VIMEO)

#Ruta para que los monitores obtengan datos de cartones y URL directo para los usuarios
@application.route("/rut/<string:rut>")
def consultaRut(rut):
    req = requests.get(url=URL_API+'{}'.format(rut))
    resp = req.json()
    if resp == 'Rut no encontrado':
        mp.track(rut.lower(), 'Login Fallido',{
        'Ingreso': 'Login Asistido'
        })
        return resp
    else:
        mp.people_set(resp['PEGAR RUT'].lower(), {
        '$first_name'    : resp['NOMBRE COMPLETO'].upper(),
        '$rut'     : resp['PEGAR RUT'].lower(),
        'Afiliado'  : resp['Tipo de afiliado'].upper()
        })
        mp.track(resp['PEGAR RUT'].lower(), 'Login Asistido',{
        'Carton 1': resp['CARTON 1'],
        'Carton 2': resp['CARTON 2']
        })
        return render_template('rut.html', data=resp, url=URL_BASE)

# URL con codigo para pruebas de carga con loader.io
@application.route("/loaderio-ec989db5a8c05ed7e625e7e8e94982c7/")
def loadTest():
    return 'loaderio-ec989db5a8c05ed7e625e7e8e94982c7'

''' 
@application.route("/<path:path>")
def publicFiles(path):
    return render_template(path)
'''






if __name__ == '__main__':
    # application.run(debug = True, ssl_context = 'adhoc', port = 5000)
    application.run(debug = True, port = 5000)
    # application.run()

