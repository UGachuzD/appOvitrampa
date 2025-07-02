<template>
  <div class="text-center mb-6">
    <v-icon size="80" color="blue">mdi-map-marker</v-icon>
    <v-card-title class="text-h4 mb-4">Mapa de calor Ovitrampas</v-card-title>
    <p class="text-body-1">Ubicación y cantidad de huevos</p>

    <!-- Botón para actualizar -->
    <div class="text-center mt-4">
      <v-btn color="primary" @click="cargarMapa" prepend-icon="mdi-refresh">
        Actualizar mapa
      </v-btn>
    </div>
  </div>
  <div ref="mapContainer" class="map-container" />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import maplibregl from 'maplibre-gl'

const mapContainer = ref(null)
let map = null
let markers = [] // ← para controlar los marcadores existentes

// 1. Obtener datos
const fetchOvitrampas = async () => {
  const response = await axios.get('http://127.0.0.1:5000/api/ovitrampas')
  const raw = response.data
  return {
    type: 'FeatureCollection',
    features: raw.map(([lat, lng, huevos]) => ({
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [lng, lat] },
      properties: { weight: huevos, description: `Huevos: ${huevos}` }
    }))
  }
}

// 2. Limpiar y agregar marcadores
const addMarkers = (features) => {
  // Limpiar marcadores anteriores
  markers.forEach(marker => marker.remove())
  markers = []

  features.forEach(feature => {
    const [lng, lat] = feature.geometry.coordinates
    const { description } = feature.properties
    const marker = new maplibregl.Marker({ color: 'red' })
      .setLngLat([lng, lat])
      .setPopup(new maplibregl.Popup().setHTML(`<strong>${description}</strong>`))
      .addTo(map)

    markers.push(marker)
  })
}

// 3. Cargar/actualizar datos en el mapa
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
          1, 'darkred'
        ]
      }
    })
  } else {
    map.getSource('ovitrampas').setData(geojsonData)
  }

  addMarkers(geojsonData.features)
  map.resize() // ← Soluciona distorsión
}

// 4. Inicializar mapa
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
