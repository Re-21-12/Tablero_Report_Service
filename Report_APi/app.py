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
@app.route("/Reporte/Jugadores")
def prueba():
    return dt.obtener_token()

@app.route("/Reporte/Equipos")
def Reporte_Equipos():
    global token
    return RG.Generar_Equipos(token)

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
