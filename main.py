from crypt import methods
from distutils.log import debug
import string
from flask import Flask, render_template, request, jsonify, redirect
from flask_restful import Api, Resource
import pandas as pd
import requests

# Credenciales Sheets de Usuarios
sheet_id = '1Jd6H3m13cWzyhJLlNYkCmyMebrVEpjeGhWeT837hucA'

#Constantes
URL_API = 'http://localhost:8000/api/rut/'
VIMEO_URL = 'https://vimeo.com/event/2090053/embed'
ZOOM_URL = 'https://us02web.zoom.us/j/87375674909?pwd=YmdKNk8rYThJb3hzLzkyU1Awejc0dz09'
WSP_URL = 'https://wa.me/56942989805'
CHAT_VIMEO = 'https://vimeo.com/event/2090053/chat/'


# static_folder: indica la nueva carpeta de statics y con 
# static_url_path puedo especificar cual es la raiz de static 
# o sea podría no tener prefico static, util para cuando trabajamos con plantillas webflow o brizi


app = Flask(__name__, static_folder='templates', static_url_path='')

#app = Flask(__name__)



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
            if obj['PEGAR RUT'].lower().startswith( value.lower() ):
                return obj
        


#rutas
api = Api(app)
api.add_resource(All, '/api/')
api.add_resource(Rut, '/api/rut/<string:value>')

data = []
#Rutas Frontend

@app.route("/")
def index():
    return render_template('login.html', wspurl=WSP_URL)

@app.route("/evento")
def evento():
    formRut = request.args.get('rut')
    req = requests.get(url=URL_API+'{}'.format(formRut))
    return render_template('evento.html', data=req.json(), zoomurl=ZOOM_URL, wspurl=WSP_URL, vimeourl=VIMEO_URL, chatvimeo=CHAT_VIMEO)
    

@app.route("/cartones")
def cartones():
    rut = request.args.get('rut')
    c1 = request.args.get('c1')
    c2 = request.args.get('c2')
    return render_template('cartones.html',rut=rut, c1=c1, c2=c2, zoomurl=ZOOM_URL, wspurl=WSP_URL, vimeourl=VIMEO_URL, chatvimeo=CHAT_VIMEO)

@app.route("/error")
def error():
    return render_template('error.html')

@app.errorhandler(404)
def notfound(error):
    return render_template('404.html'), 404

@app.route("/login2")
def testLogin():
    return render_template('login2.html')

 
@app.route("/directo")
def directo():
    
    formRut = request.args.get('rut')
    req = requests.get(url=URL_API+'{}'.format(formRut))
    return render_template('home-evento.html', data=req.json(), zoomurl=ZOOM_URL, wspurl=WSP_URL, vimeourl=VIMEO_URL, chatvimeo=CHAT_VIMEO)

'''
@app.route("/test-vimeo/<string:rut>")
def vimeo(rut):
    req = requests.get(url='http://localhost:8000/api/rut/{}'.format(rut))
    return render_template('vimeo.html', data=req.json())
'''



@app.route("/<path:path>")
def publicFiles(path):
    return render_template(path)

# api entretencion
# @app.route("/api/rut/<id>")
# def searchRut(id):
#    return "<h1>el rut es: {}</h1>".format(id)





if __name__ == '__main__':
    app.run(debug = True, port=8000)
