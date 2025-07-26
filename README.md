# 📦 Software Ovitrampa

Este repositorio cuenta con el código fuente del frontend y backend empleado en el desarrollo del software del Sistema de ayuda a la decisión para controlar la densidad poblacional del mosquito transmisor del dengue en Acapulco, desarrollado durante la estancia de investigación Verano Delfín 2025.

---

## 🧠 Índice

- [Tecnologías utilizadas](#tecnologias-utilizadas)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Autores](#autores)
- [Licencia](#licencia)

---

## ⚙️ Tecnologías utilizadas

### Frontend
- [ ] Vue
- [ ] Framework UI: Vuetify
- [ ] Otros: axios, leaflet, turf 

### Backend
- [ ] Python (Flask)
- [ ] Librerias utilizadas se encuentran dentro del archivo `requirements.txt`

### Nube
- [ ] Microsoft Azure
- [ ] Medio de almacenamiento: Blob Storqge
- [ ] Manejo de SAS token

---

## 🧱 Estructura del proyecto

```bash
/
├── frontend/
│   ├── src/
│   ├── public/
│   └── ...
├── backend/
│   ├── .venv/
|   ├── auth/
|   ├── data/
|   │   └── users.json
│   ├── app.py
|   ├── .env
│   └── ...
└── README.md
```

## 🖥️ Leventar proyecto

Para poder ejecutar el proyecto de manera local, es necesario seguir los siguientes pasos:

1. Clonar el respositorio por medio del comando desde terminal:
```bash
git clone [text](https://github.com/UGachuzD/appOvitrampa.git)
```
2. Acceder a la ruta en donde se guardo el archivo y dirigirse a la ruta en donde se encuentra el frontend, una vez dentro ejecutar el siguiente comando:
```bash
npm install
```
3. Cuando se haya terminado de instalar lo necesario para el frontend, ejecutar el comando que mostrara en terminal la dirección localhost en la cual al presionarla aparecerá desde navegador el frontend:
```bash
npm run dev
```
4. Antes de interactuar con el frontend, dirigirse a la ruta del backend y crear un entorno virtual con el siguiente comando:
```bash
python -m venv nombreEntornoVirtual
```
5. Cuando el entorno se haya creado, debemos de activarlo (Depende el sistema operativo donde se cree el comando con el cual activarlo) e instalar las librerias dentro del entorno virtual con el siguiente comando:
```bash
pip install -r requirements.txt
```
6. Cuando este haya terminado de completarse, es necesario que dentro de backend exista el archivo `.env` que contiene las variables de entorno usadas en el proyecto que corresponden a los SAS Token de Azure para los archivos de imagenes, gestion.json, control.json y datos.json. El archivo debe de quedar como sigue:
```bash
SAS_TOKEN_IMAGENES = "https://<account>.blob.core.windows.net/<container>/<blob>?<SAS_TOKEN>"
SAS_TOKEN_GESTION = "https://<account>.blob.core.windows.net/<container>/<blob>?<SAS_TOKEN>"
SAS_TOKEN_CONTROL = "https://<account>.blob.core.windows.net/<container>/<blob>?<SAS_TOKEN>"
SAS_TOKEN_DATOS = "https://<account>.blob.core.windows.net/<container>/<blob>?<SAS_TOKEN>"
```
7. De igual forma dentro de la carpeta `data/` del backend debe de existir el archivo `user.json` que debe de contener el correo y el hash de la contraseña, para eso se incluye el archivo `generatePass.py` que genera la contraseña con base una cadena, es el archivo donde se autentifica el usuario y contraseña. El archivo debe de tener el siguiente formato:
```json
[
  {
    "email": "user@dominio.com",
    "password_hash": "cadenaHash" 
  }
]
```
8. Posterior a añadir los archivos faltantes, se puede ejecutar el siguiente comando dentro de la raiz del backend que inicializará el backend y asi poder ahora si interactuar con el sistema:
```bash
python app.py
```

## 👥 Autores
- [text](https://github.com/UGachuzD)
- [text](https://github.com/AuthenticAsp)

## 📋 Licencia
© 2025 Ulises Gachuz. Todos los derechos reservados.

Este proyecto fue desarrollado como parte de una estancia de investigación en la Facultad de Matemáticas de la Universidad Autónoma de Guerrero.

**No se permite copiar, distribuir, modificar ni utilizar el contenido de este repositorio, total ni parcialmente, sin el permiso explícito y por escrito de los autores.**

El uso del material está estrictamente limitado a fines de revisión personal o académica sin redistribución.