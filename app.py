{\rtf1\ansi\ansicpg1252\cocoartf2639
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from flask import Flask, request, jsonify\
import csv\
from datetime import datetime\
\
app = Flask(__name__)\
\
@app.route("/data", methods=["POST"])\
def receive_data():\
    data = request.get_json(force=True)  # Datos en JSON del ESP32\
    print("Datos recibidos:", data)\
\
    # Extraer campos\
    imei = data.get("imei", "N/A")\
    temperature = data.get("temperature", 0.0)\
    latitude = data.get("latitude", 0.0)\
    longitude = data.get("longitude", 0.0)\
\
    # Guardar en CSV\
    with open("data.csv", "a", newline="") as f:\
        writer = csv.writer(f)\
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")\
        writer.writerow([now_str, imei, temperature, latitude, longitude])\
\
    return jsonify(\{"status": "ok", "message": "Datos recibidos correctamente"\}), 200\
\
\
@app.route("/")\
def index():\
    return "Servidor Flask en Railway: Enviar POST a /data", 200\
\
\
if __name__ == "__main__":\
    # En local usamos el puerto 5000\
    app.run(host="0.0.0.0", port=5000, debug=True)\
}