import requests
from flask import Flask, jsonify, request
from database import db
from data import obtener_token, Obtener_Jugadores
import ReportGenerator as RG

app = Flask(__name__)
token = ""

@app.route("/")
def default():
    return jsonify({"Mensaje": "Esta ruta es la principal, no hay nada aqui"})

@app.route("/auth", methods=["GET"])
def raiz():
    global token
    r = request.get_json()
    usuario = {
        "nombre": r["nombre"],
        "contrasena": r["contrasena"]
    }
    token = obtener_token(usuario)
    return jsonify({"mensaje": "API Flask funcionando correctamente"})
@app.route("/Reporte/Jugadores")
def prueba():
    return obtener_token()

@app.route("/Reporte/Equipos")
def Reporte_Equipos():
    return RG.Generar_Equipos()

@app.route("/usuarios")
def obtener_usuarios():
    usuarios = list(db.usuarios.find({}, {"_id": 0}))
    return jsonify({"usuarios": usuarios})

@app.route("/externa")
def consumir_externa():
    token = obtener_token()
    data = Obtener_Jugadores(token)
    return jsonify({"datos": data})

if __name__ == "__main__":
    app.run(debug=True, port=8000)
