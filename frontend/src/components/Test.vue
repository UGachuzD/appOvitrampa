<template>
  <v-app>
    <v-main>
      <v-container class="pa-4 fill-container" fluid>
        <!-- Botón centrado arriba del iframe -->
        <v-row justify="center" class="mb-4">
          <v-col cols="auto">
            <v-btn color="primary" @click="actualizarConteo">
              Actualizar conteo
            </v-btn>
          </v-col>
        </v-row>

        <!-- Mapa de calor -->
        <iframe ref="heatmapFrame" src="/heatmap.html" class="full-frame"></iframe>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue';

const heatmapFrame = ref(null);

async function actualizarConteo() {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/huevos', {
      method: 'POST'
    });

    if (!response.ok) {
      throw new Error(`Error del servidor: ${response.statusText}`);
    }

    const jsonData = await response.json();

    // Forzar recarga del iframe
    if (heatmapFrame.value) {
      heatmapFrame.value.src = heatmapFrame.value.src;
    }
  } catch (error) {
    console.error('Error al obtener o procesar los datos:', error);
  }
}

</script>

<style scoped>
.fill-container {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.full-frame {
  border: none;
  width: 90%;
  height: 90%;
}
</style>
