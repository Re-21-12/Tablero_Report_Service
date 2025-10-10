import requests
from flask import Flask, jsonify, request
from database import db
import data as dt
import ReportGenerator as RG

app = Flask(__name__)
token = ""

@app.route("/")
def default():
    """
    global token
    r = request.get_json()
    usuario = {
        "nombre": r["nombre"],
        "contrasena": r["contrasena"]
    }
    token = obtener_token(usuario)
    """
    return jsonify({"mensaje": "API Flask funcionando correctamente"})
    

@app.route("/auth", methods=["GET"])
def raiz():
    global token
    """r = request.get_json()
    usuario = {
        "nombre": r["nombre"],
        "contrasena": r["contrasena"]
    }
    """
    usuario = {
        "nombre": "Macario",
        "contrasena": "apple123"
    }
    dt.set_user(usuario)
    token = dt.obtener_token()


    return jsonify({"mensaje": "API Flask funcionando correctamente"})


@app.route("/Reporte/Equipos")
def Reporte_Equipos():
    global token
    return RG.Generar_Equipos(token)
@app.route("/Reporte/Jugadores")
def Reporte_Equipo_Jugadores():
    global token
    id_equipo = request.args.get('id')
    return RG.Generar_Jugadores(token, id_equipo)
@app.route("/Reporte/Partidos")
def Reporte_Partidos_Marcador():
    global token
    return RG.Generar_Historial_Partidos(token)
@app.route("/Reporte/Partido/Roster")
def Reporte_Jugadores_Equipo_Partido():
    global token
    id_partido = request.args.get('id')
    return RG.Generar_Roster_Partido(token, id_partido)


@app.route("/usuarios")
def obtener_usuarios():
    usuarios = list(db.usuarios.find({}, {"_id": 0}))
    return jsonify({"usuarios": usuarios})

@app.route("/externa")
def consumir_externa():
    token = dt.obtener_token()
    data = dt.Obtener_Jugadores(token)
    return jsonify({"datos": data})

if __name__ == "__main__":
    app.run(debug=True, port=8000)
