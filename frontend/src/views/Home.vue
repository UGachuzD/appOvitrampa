<template>
  <v-app>
    <v-app-bar app color="primary" prominent>
      <v-app-bar-nav-icon variant="text" @click.stop="drawer = !drawer" />
      <v-toolbar-title class="text-h5 font-weight-bold">Dashboard</v-toolbar-title>
      <v-spacer />
      <v-btn icon><v-icon>mdi-bell-outline</v-icon></v-btn>
      <v-menu location="bottom">
        <template v-slot:activator="{ props }">
          <v-btn icon v-bind="props">
            <v-avatar size="40" color="secondary"><v-icon>mdi-account</v-icon></v-avatar>
          </v-btn>
        </template>
        <v-list>
          <v-list-item prepend-icon="mdi-cog" title="Configuración" @click="navigateTo('settings')" />
          <v-list-item prepend-icon="mdi-logout" title="Cerrar sesión" @click="handleLogout" />
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" temporary>
      <v-list nav dense>
        <v-list-item prepend-icon="mdi-chip" title="Monitorear ESP32" @click="navigateTo('monitor')" :active="activeTab === 'monitor'" />
        <v-list-item prepend-icon="mdi-map-marker" title="Ubicación Ovitrampas" @click="navigateTo('mapa')" :active="activeTab === 'mapa'" />
        <v-list-item prepend-icon="mdi-cog" title="Ajustes" @click="navigateTo('settings')" :active="activeTab === 'settings'" />
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container fluid class="fill-height">
        <v-row class="fill-height">
          <v-col cols="12">
            <v-card class="pa-6 rounded-lg" elevation="4">
              <v-card-title class="text-h4 mb-4">Bienvenido al sistema</v-card-title>
              <v-card-text>
                <v-window v-model="activeTab">
                  <v-window-item value="monitor">
                    <div class="text-center py-8">
                      <v-icon size="80" color="blue">mdi-chip</v-icon>
                      <h2 class="text-h3 my-4">Monitoreo ESP32</h2>
                      <p class="text-body-1">Estado y configuración del dispositivo</p>
                    </div>
                  </v-window-item>

                  <v-window-item value="mapa">
                    <div class="text-center py-8">
                      <div ref="mapContainer" class="map-container" />
                    </div>
                  </v-window-item>

                  <v-window-item value="settings">
                    <div class="text-center py-8">
                      <v-icon size="80" color="grey">mdi-cog</v-icon>
                      <h2 class="text-h3 my-4">Ajustes</h2>
                      <p class="text-body-1">Configuración del sistema</p>
                    </div>
                  </v-window-item>
                </v-window>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>

    <v-footer app color="surface" class="py-2">
      <v-spacer />
      <span class="text-caption text-disabled">Sistema de monitoreo &copy; {{ new Date().getFullYear() }}</span>
      <v-spacer />
    </v-footer>
  </v-app>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import maplibregl from 'maplibre-gl';

const drawer = ref(false);
const activeTab = ref('monitor');
const router = useRouter();
const mapContainer = ref(null);
let map = null;
let geojsonData = null;

const waitForContainer = (attempts = 10) =>
  new Promise((resolve, reject) => {
    const check = () => {
      if (mapContainer.value) resolve();
      else if (attempts <= 0) reject(new Error('mapContainer no disponible'));
      else setTimeout(() => check(--attempts), 200);
    };
    check();
  });

const fetchOvitrampas = async () => {
  const response = await axios.get('http://127.0.0.1:5000/api/ovitrampas');
  const raw = response.data;

  // Convertir a GeoJSON FeatureCollection
  return {
    type: 'FeatureCollection',
    features: raw.map(([lat, lng, huevos]) => ({
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [lng, lat],
      },
      properties: {
        weight: huevos,
        description: `Huevos: ${huevos}`
      }
    }))
  };
};

const addMarkers = (features) => {
  features.forEach((feature) => {
    const [lng, lat] = feature.geometry.coordinates;
    const { description } = feature.properties;

    new maplibregl.Marker({ color: 'red' })
      .setLngLat([lng, lat])
      .setPopup(new maplibregl.Popup().setHTML(`<strong>${description}</strong>`))
      .addTo(map);
  });
};

const initMapLibre = async () => {
  try {
    await nextTick();
    await waitForContainer();

    if (map) {
      map.remove();
      map = null;
    }

    // Recuperar datos del backend
    geojsonData = await fetchOvitrampas();

    map = new maplibregl.Map({
      container: mapContainer.value,
      style: 'https://tiles.stadiamaps.com/styles/alidade_smooth.json',
      center: [-99.880066, 16.865588],
      zoom: 14,
    });

    map.on('load', () => {
      // Fuente GeoJSON desde backend
      map.addSource('ovitrampas', {
        type: 'geojson',
        data: geojsonData,
      });

      // Capa de calor
      map.addLayer({
        id: 'ovitrampas-heat',
        type: 'heatmap',
        source: 'ovitrampas',
        maxzoom: 18,
        paint: {
          // Este parametro realza la intensidad del calor en el mapa
          'heatmap-intensity': ['interpolate', ['linear'], ['zoom'], 10, 2, 18, 4],
          'heatmap-weight': ['interpolate', ['linear'], ['get', 'weight'], 0, 0, 100, 1],
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
          ],
          // Este parametro de radius especifica el radio de influencia de cada punto
          'heatmap-radius': ['interpolate', ['linear'], ['zoom'], 10, 30, 18, 60],
          'heatmap-opacity': 0.7,
        }
      });

      // Marcadores individuales
      addMarkers(geojsonData.features);
    });
  } catch (e) {
    console.error('Error inicializando el mapa:', e);
  }
};

watch(activeTab, (tab) => {
  if (tab === 'mapa') initMapLibre();
});

const navigateTo = (tab) => {
  activeTab.value = tab;
  drawer.value = false;
};

const handleLogout = () => {
  localStorage.removeItem('token');
  router.push('/');
};
</script>



<style scoped>
.v-list-item--active {
  background-color: rgba(98, 0, 238, 0.08);
}
.v-main {
  background-color: #f5f5f5;
}
.v-card {
  transition: all 0.3s ease;
}
.v-card:hover {
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1) !important;
}
.map-container {
  width: 100%;
  height: 500px;
  border-radius: 10px;
  overflow: hidden;
}

</style>
