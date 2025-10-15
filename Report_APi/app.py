import requests
from flask import Flask, jsonify, request
from database import db
import data as dt
import ReportGenerator as RG

app = Flask(__name__)
token = ''

@app.route('/')
def default():
    '''
    global token
    r = request.get_json()
    usuario = {
        'nombre': r['nombre'],
        'contrasena': r['contrasena']
    }
    token = obtener_token(usuario)
    '''
    return jsonify({'mensaje': 'API Flask funcionando correctamente'})
    

@app.route('/auth', methods=['GET'])
def raiz():
    global token
    '''r = request.get_json()
    usuario = {
        'nombre': r['nombre'],
        'contrasena': r['contrasena']
    }
    '''
    usuario = {
        'nombre': 'Macario',
        'contrasena': 'apple123'
    }
    dt.set_user(usuario)
    token = dt.obtener_token()


    return jsonify({'mensaje': 'API Flask funcionando correctamente'})


@app.route('/Reporte/Equipos', methods=['POST'])
def Reporte_Equipos():
    global token
    data = request.get_json()
    print(data)
    return RG.Generar_Equipos(data)
@app.route('/Reporte/Jugadores', methods=['POST'])
def Reporte_Equipo_Jugadores():
    global token
    equipo = str(request.args.get('equipo'))
    jugadores = request.get_json()
    return RG.Generar_Jugadores(jugadores, equipo)
@app.route('/Reporte/Partidos', methods=['POST'])
def Reporte_Partidos_Marcador():
    global token
    datos = request.get_json()
    return RG.Generar_Historial_Partidos(datos)
@app.route('/Reporte/Partido/Roster', methods=['POST'])
def Reporte_Jugadores_Equipo_Partido():
    global token
    datos = request.get_json()
    return RG.Generar_Roster_Partido(datos)
@app.route('/Reporte/Estadistica/Jugador', methods=['POST'])
def Reporte_Estadistica_Jugador():
    global token
    
    data = request.get_json()
    return RG.Generar_Reporte_Estadisticas_Jugador(data)

@app.route('/usuarios')
def obtener_usuarios():
    usuarios = list(db.usuarios.find({}, {'_id': 0}))
    return jsonify({'usuarios': usuarios})

@app.route('/externa')
def consumir_externa():
    token = dt.obtener_token()
    data = dt.Obtener_Jugadores(token)
    return jsonify({'datos': data})

if __name__ == '__main__':
    pass
