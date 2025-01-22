#!/usr/bin/env python3
from flask import Flask, request, jsonify
import csv
from datetime import datetime
import os

app = Flask(__name__)

# Archivo donde se guardan los datos
CSV_FILE = "data.csv"

# Si quieres, creas la cabecera una sola vez:
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "imei", "temperature", "latitude", "longitude"])

@app.route("/", methods=["GET"])
def index():
    return "Servidor Flask en Render: envía POST a /data", 200

@app.route("/data", methods=["POST"])
def receive_data():
    """
    Endpoint para recibir datos JSON del T-Call A7670E.
    Espera un JSON como:
    {
        "imei": "string",
        "temperature": 25.4,
        "latitude": 10.123456,
        "longitude": -66.123456
    }
    """
    data = request.get_json(force=True)
    imei = data.get("imei", "N/A")
    temperature = data.get("temperature", 0.0)
    latitude = data.get("latitude", 0.0)
    longitude = data.get("longitude", 0.0)

    # Guarda en CSV con fecha/hora
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([now_str, imei, temperature, latitude, longitude])

    return jsonify({"status": "ok", "message": "Datos recibidos correctamente"}), 200

@app.route("/csv", methods=["GET"])
def get_csv():
    """
    Permite descargar/visualizar el contenido de data.csv
    """
    if not os.path.exists(CSV_FILE):
        return "No hay datos aún.", 200

    with open(CSV_FILE, "r") as f:
        content = f.read()
    # Envía el CSV como texto plano
    return f"<pre>{content}</pre>", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
