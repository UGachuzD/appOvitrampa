<template>
    <div class="text-center mb-6">
      <v-icon size="80" color="blue">mdi-map-marker</v-icon>
      <v-card-title class="text-h4 mb-4">Mapa de calor Ovitrampas</v-card-title>
      <p class="text-body-1">Ubicación y cantidad de huevos</p>
    </div>
    <div ref="mapContainer" class="map-container" />
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  import maplibregl from 'maplibre-gl'
  
  const mapContainer = ref(null)
  let map = null
  
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
  
  const addMarkers = (features) => {
    features.forEach(feature => {
      const [lng, lat] = feature.geometry.coordinates
      const { description } = feature.properties
      new maplibregl.Marker({ color: 'red' })
        .setLngLat([lng, lat])
        .setPopup(new maplibregl.Popup().setHTML(`<strong>${description}</strong>`))
        .addTo(map)
    })
  }
  
  onMounted(async () => {
    const geojsonData = await fetchOvitrampas()
  
    map = new maplibregl.Map({
      container: mapContainer.value,
      style: 'https://tiles.stadiamaps.com/styles/alidade_smooth.json',
      center: [-99.880066, 16.865588],
      zoom: 14,
    })
  
    map.on('load', () => {
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
  
      addMarkers(geojsonData.features)
    })
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
  