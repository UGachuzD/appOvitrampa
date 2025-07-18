import json
import requests
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import csv

load_dotenv()

data_bp = Blueprint('data', __name__)

@data_bp.route('/api/ovitrampas', methods=['GET'])
def get_ovitrampa_data():
    data_file = 'data/dataOvitrampas.csv'
    points = []

    try:
        with open(data_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row['nombre']
                lat = float(row['latitud'])
                lng = float(row['longitud'])
                intensity = int(row['huevos'])  # Usado como peso en el heatmap
                points.append([name, lat, lng, intensity])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify(points)

@data_bp.route('/api/gestion', methods=['GET'])
def actualizar_gestion():
    try:
        sas_url = os.getenv('SAS_TOKEN_GESTION')
        if not sas_url:
            return jsonify({"error": "SAS_URL no está definido en el .env"}), 500

        # Obtener datos actuales
        res = requests.get(sas_url)
        if res.status_code != 200:
            return jsonify({"error": "Error al obtener el archivo JSON"}), 500

        raw_data = res.json()
        now = datetime.utcnow()
        updated_data = {}

        for device_id, info in raw_data.items():
            utc_timestamp = datetime.fromisoformat(info['timestamp'])
            gmt6_timestamp = utc_timestamp - timedelta(hours=6)
            diff_minutes = (now - utc_timestamp).total_seconds() / 60

            status = "Inactivo" if diff_minutes > 1 else "Activo"

            updated_data[device_id] = {
                "ubicacion": info.get("ubicacion"),
                "timestamp": info.get("timestamp"),
                "status": status,
                "localTimestamp": gmt6_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                "latitud": info.get("latitud"),
                "longitud": info.get("longitud")
            }

        # Guardar sin localTimestamp
        save_data = {
            dev_id: {
                "ubicacion": dev_info.get("ubicacion"),
                "timestamp": dev_info.get("timestamp"),
                "status": dev_info.get("status"),
                "latitud": dev_info.get("latitud"),
                "longitud": dev_info.get("longitud")
            }
            for dev_id, dev_info in updated_data.items()
        }


        response = requests.put(
            sas_url,
            data=json.dumps(save_data, indent=2),
            headers={
                "x-ms-blob-type": "BlockBlob",
                "Content-Type": "application/json"
            }
        )

        if response.status_code not in [200, 201]:
            return jsonify({"error": "Error al sobrescribir archivo JSON"}), 500

        return jsonify(updated_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@data_bp.route('/api/control', methods=['GET'])
def obtener_control_json():
    CONTROL_URL = os.getenv('SAS_TOKEN_CONTROL')
    try:
        if not CONTROL_URL:
            return jsonify({"error": "CONTROL_SAS_URL no definido"}), 500

        response = requests.get(CONTROL_URL)
        if response.status_code != 200:
            return jsonify({"error": "No se pudo obtener el archivo de configuración"}), 500

        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@data_bp.route('/api/control', methods=['PUT'])
def actualizar_control_json():
    CONTROL_URL = os.getenv('SAS_TOKEN_CONTROL')
    try:
        if not CONTROL_URL:
            return jsonify({"error": "CONTROL_SAS_URL no definido"}), 500

        nuevo_json = request.get_json()
        if not nuevo_json:
            return jsonify({"error": "JSON inválido o vacío"}), 400

        # Orden deseado
        orden_claves = [
            "horasTomaFoto",
            "intervaloRevision",
            "blobBase",
            "sasTokenEscritura",
            "urlGestion",
            "tomaInstanteanea"
        ]

        # Reordenar
        nuevo_json_ordenado = {clave: nuevo_json.get(clave) for clave in orden_claves}

        put_response = requests.put(
            CONTROL_URL,
            data=json.dumps(nuevo_json_ordenado, indent=2),
            headers={
                "x-ms-blob-type": "BlockBlob",
                "Content-Type": "application/json"
            }
        )

        if put_response.status_code not in [200, 201]:
            return jsonify({"error": "No se pudo guardar el archivo"}), 500

        return jsonify(nuevo_json_ordenado)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
