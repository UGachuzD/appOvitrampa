<template>
  <div class="text-center mb-6">
    <v-icon size="80" color="blue">mdi-map-marker</v-icon>
    <v-card-title class="text-h4 mb-4">Mapa de calor Ovitrampas</v-card-title>
    <p class="text-body-1">Ubicación y cantidad de huevos</p>

    <div class="text-center mt-4">
      <v-btn color="primary" @click="cargarMapa" prepend-icon="mdi-refresh">
        Actualizar mapa
      </v-btn>
    </div>
  </div>

  <!-- Mapa -->
  <div ref="mapContainer" class="map-container" />

  <!-- Tabla -->
  <v-card class="mt-8">
    <v-card-title>Tabla de Ovitrampas</v-card-title>
    <v-data-table
      :headers="headers"
      :items="ovitrampasData"
      class="elevation-1"
      :items-per-page="5"
    >
      <template #item="{ item, index }">
        <!-- Fila descriptiva -->
        <tr v-if="index === 0" style="font-weight: bold; background-color: #f0f0f0">
          <td>—</td>
          <td>{{ item.name }}</td>
          <td>{{ item.lat }}</td>
          <td>{{ item.lng }}</td>
          <td>{{ item.huevos }}</td>
        </tr>
        <!-- Filas normales -->
        <tr v-else>
          <td>{{ index }}</td>
          <td>{{ item.name }}</td>
          <td>{{ item.lat }}</td>
          <td>{{ item.lng }}</td>
          <td>{{ item.huevos }}</td>
        </tr>
      </template>
    </v-data-table>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import maplibregl from 'maplibre-gl'

const mapContainer = ref(null)
let map = null
let markers = []

// Tabla
const ovitrampasData = ref([])
const headers = [
  { text: '#', value: 'index' },
  { text: 'Nombre', value: 'name' },
  { text: 'Latitud', value: 'lat' },
  { text: 'Longitud', value: 'lng' },
  { text: 'Huevos', value: 'huevos' },
]

// Obtener datos del backend
const fetchOvitrampas = async () => {
  const response = await axios.get('http://127.0.0.1:5000/api/ovitrampas')
  const raw = response.data

  // Agrega una fila descriptiva al inicio
  ovitrampasData.value = [
    {
      name: 'Nombre de la ovitrampa',
      lat: 'Latitud (coordenada Y)',
      lng: 'Longitud (coordenada X)',
      huevos: 'Número de huevos detectados',
    },
    ...raw.map(([name, lat, lng, huevos]) => ({ name, lat, lng, huevos })),
  ]

  // Devuelve datos para el mapa
  return {
    type: 'FeatureCollection',
    features: raw.map(([name, lat, lng, huevos]) => ({
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [lng, lat] },
      properties: {
        name,
        weight: huevos,
        description: `<strong>${name}</strong><br>Huevos: ${huevos}`,
      },
    })),
  }
}

// Agregar marcadores
const addMarkers = (features) => {
  markers.forEach(marker => marker.remove())
  markers = []

  features.forEach(feature => {
    const [lng, lat] = feature.geometry.coordinates
    const { description } = feature.properties
    const marker = new maplibregl.Marker({ color: 'red' })
      .setLngLat([lng, lat])
      .setPopup(new maplibregl.Popup().setHTML(description))
      .addTo(map)

    markers.push(marker)
  })
}

// Cargar mapa
const cargarMapa = async () => {
  const geojsonData = await fetchOvitrampas()

  if (!map.getSource('ovitrampas')) {
    map.addSource('ovitrampas', { type: 'geojson', data: geojsonData })

    map.addLayer({
      id: 'heatmap',
      type: 'heatmap',
      source: 'ovitrampas',
      maxzoom: 18,
      paint: {
        'heatmap-intensity': ['interpolate', ['linear'], ['zoom'], 10, 2, 18, 4],
        'heatmap-weight': ['interpolate', ['linear'], ['get', 'weight'], 0, 0, 100, 1],
        'heatmap-radius': ['interpolate', ['linear'], ['zoom'], 10, 30, 18, 60],
        'heatmap-opacity': 0.7,
        'heatmap-color': [
          'interpolate',
          ['linear'],
          ['heatmap-density'],
          0, 'rgba(0,255,0,0)',
          0.2, 'lime',
          0.4, 'yellow',
          0.6, 'orange',
          0.8, 'red',
          1, 'darkred',
        ],
      },
    })
  } else {
    map.getSource('ovitrampas').setData(geojsonData)
  }

  addMarkers(geojsonData.features)
  map.resize()
}

// Inicializar mapa
onMounted(() => {
  map = new maplibregl.Map({
    container: mapContainer.value,
    style: 'https://tiles.stadiamaps.com/styles/alidade_smooth.json',
    center: [-99.880066, 16.865588],
    zoom: 14,
  })

  map.on('load', cargarMapa)
})
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 500px;
  border-radius: 10px;
  overflow: hidden;
}
</style>
