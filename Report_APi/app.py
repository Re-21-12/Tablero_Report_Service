from flask import Flask, jsonify
from database import db
from data import obtener_token, Obtener_Jugadores

app = Flask(__name__)

@app.route("/")
def raiz():
    return jsonify({"mensaje": "API Flask funcionando correctamente"})
@app.route("/token")
def prueba():
    return obtener_token()

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
