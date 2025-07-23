import json
import requests
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import csv

from flask import request, jsonify
import os
import cv2
import numpy as np
from PIL import Image
import json
from azure.storage.blob import ContainerClient, BlobClient, ContentSettings 
import shutil


load_dotenv()

data_bp = Blueprint('data', __name__)

# ======================
# FUNCIONES PARA CONTEO DE HUEVOS
# ======================

def obtenerInfoUbicacion(sasUrlJson):
    blobClient = BlobClient.from_blob_url(sasUrlJson)
    datosJson = blobClient.download_blob().readall()
    infoUbicaciones = json.loads(datosJson)

    resultado = {}
    for identificador, info in infoUbicaciones.items():
        lat = info.get("latitud")
        lon = info.get("longitud")
        resultado[identificador] = {"latitud": lat, "longitud": lon}

    return resultado


def descargarImgs(sasUrl, identificador, directorioSalida):
    os.makedirs(directorioSalida, exist_ok=True)
    containerClient = ContainerClient.from_container_url(sasUrl)

    for blob in containerClient.list_blobs():
        if identificador in blob.name:
            rutaLocal = os.path.join(directorioSalida, os.path.basename(blob.name))
            with open(rutaLocal, "wb") as file:
                datos = containerClient.download_blob(blob)
                file.write(datos.readall())


def procesarImagen(rutaImagen, areaMin=300, areaMax=450):
    pilImage = Image.open(rutaImagen).convert("RGB")
    imagen = np.array(pilImage)
    imagen = cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR)
    imagenRedimensionada = cv2.resize(imagen, (400, 400))
    gris = cv2.cvtColor(imagenRedimensionada, cv2.COLOR_BGR2GRAY)
    filtrada = cv2.medianBlur(gris, 5)

    binTemp = cv2.adaptiveThreshold(
        filtrada, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )

    contornos, _ = cv2.findContours(binTemp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    huevosValidos = [cnt for cnt in contornos if areaMin < cv2.contourArea(cnt) < areaMax]

    return len(huevosValidos)


def contarHuevosEnCarpeta(carpetaImagenes, identificador):
    totalHuevos = 0
    for nombreArchivo in os.listdir(carpetaImagenes):
        if nombreArchivo.lower().endswith((".jpg", ".png", ".jpeg")):
            rutaImagen = os.path.join(carpetaImagenes, nombreArchivo)
            cantidad = procesarImagen(rutaImagen)
            totalHuevos += cantidad
    return totalHuevos



data_bp = Blueprint('data', __name__)

@data_bp.route('/api/huevos', methods=['POST'])
def obtenerNumeroHuevos():
    try:
        sasUrlImgs = os.getenv('SAS_TOKEN_IMAGENES')
        sasUrlJson = os.getenv('SAS_TOKEN_GESTION')
        sasUrlDatos = os.getenv('SAS_TOKEN_DATOS') 

        identificadores = ["OVI-AEAA6C", "OVI-FIBONA"]

        if not sasUrlImgs or not sasUrlJson or not sasUrlDatos:
            return jsonify({"error": "Faltan parámetros obligatorios"}), 400

        carpetaRaizImgs = "imgs"

        if os.path.exists(carpetaRaizImgs):
            shutil.rmtree(carpetaRaizImgs)
        os.makedirs(carpetaRaizImgs, exist_ok=True)

        infoUbicaciones = obtenerInfoUbicacion(sasUrlJson)
        resultados = []

        for identificador in identificadores:
            subcarpeta = os.path.join(carpetaRaizImgs, identificador)
            descargarImgs(sasUrlImgs, identificador, subcarpeta)
            totalHuevos = contarHuevosEnCarpeta(subcarpeta, identificador)

            datosUbicacion = infoUbicaciones.get(identificador, {})
            latitud = datosUbicacion.get("latitud", "")
            longitud = datosUbicacion.get("longitud", "")

            resultados.append({
                "latitud": latitud,
                "longitud": longitud,
                "gid": identificador,
                "cantidad_huevos": totalHuevos
            })

        # Guardar el JSON en Azure Blob Storage (sobrescribir)
        blob_client = BlobClient.from_blob_url(sasUrlDatos)
        blob_client.upload_blob(
            json.dumps(resultados, ensure_ascii=False, indent=4),
            overwrite=True,
            content_settings=ContentSettings(content_type="application/json") 
        )

        return jsonify(resultados), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@data_bp.route('/api/datosJSON', methods=['GET'])
def obtener_datos():
    sas_url_datosJson = os.getenv("SAS_TOKEN_DATOS")

    try:
        response = requests.get(sas_url_datosJson)
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'No se pudieron obtener los datos', 'detalle': str(e)}), 500


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

            status = "Inactivo" if diff_minutes > 180 else "Activo"

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
