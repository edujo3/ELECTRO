from flask import Flask, request, jsonify
import csv
from datetime import datetime

app = Flask(__name__)

@app.route("/data", methods=["POST"])
def receive_data():
    # Leer datos enviados por el ESP32 en formato JSON
    data = request.get_json(force=True)
    print("Datos recibidos:", data)

    # Extraer campos (imei, temperature, latitude, longitude)
    imei = data.get("imei", "N/A")
    temperature = data.get("temperature", 0.0)
    latitude = data.get("latitude", 0.0)
    longitude = data.get("longitude", 0.0)

    # Guardar en un archivo CSV
    with open("data.csv", "a", newline="") as f:
        writer = csv.writer(f)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([now_str, imei, temperature, latitude, longitude])

    return jsonify({"status": "ok", "message": "Datos recibidos correctamente"}), 200

@app.route("/")
def index():
    return "Servidor Flask en Render: envía POST a /data", 200

if __name__ == "__main__":
    # Ejecuta en modo local en el puerto 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
