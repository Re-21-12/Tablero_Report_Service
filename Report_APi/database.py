from pymongo import MongoClient
from flask import jsonify, request, send_file
import io
import os

MONGO_URI = "mongodb://root:apple123@mongo:27017/"
DB_NAME = "Reporteria"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def get_mongo_connection():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://root:apple123@mongo:27017/")
    client = MongoClient(mongo_uri)
    db = client["Reporteria"]
    return db

def Descargar_Reporte(nombre_reporte):
    db = get_mongo_connection()
    reporte = db.Reporteria.find_one({"nombre_reporte": nombre_reporte})
    if not reporte:
        return jsonify({"error": "Reporte no encontrado"}), 404

    buffer = io.BytesIO(reporte["archivo_pdf"])
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{nombre_reporte}.pdf",
        mimetype="application/pdf"
    )

