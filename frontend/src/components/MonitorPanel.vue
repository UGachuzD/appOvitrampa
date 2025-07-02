<template>
  <div class="py-8">
    <div class="text-center mb-6">
      <v-icon size="80" color="blue">mdi-chip</v-icon>
      <v-card-title class="text-h4 mb-4">Monitoreo ESP32</v-card-title>
      <p class="text-body-1">Estado y configuración de los dispositivos</p>
      <div class="text-center mt-4">
        <v-btn
          color="primary"
          @click="fetchAndOverwrite"
          prepend-icon="mdi-refresh"
        >
          Actualizar datos
        </v-btn>
      </div>
    </div>

    <v-row justify="center" align="center" class="px-4">
      <v-col
        v-for="(device, id) in dispositivos"
        :key="id"
        cols="12"
        md="6"
        lg="4"
      >
        <v-card elevation="2" class="pa-4">
          <v-card-title class="text-h6">{{ id }}</v-card-title>
          <v-card-subtitle class="text-body-2 mb-2">{{
            device.ubicacion
          }}</v-card-subtitle>
          <div class="d-flex align-center justify-space-between mt-2">
            <span class="text-caption">Última señal:</span>
            <span class="text-caption">{{ device.localTimestamp }}</span>
          </div>
          <div class="d-flex align-center justify-space-between mt-2">
            <span class="text-caption">Estado:</span>
            <v-chip
              :color="device.status === 'Activo' ? 'green' : 'red'"
              text-color="white"
            >
              {{ device.status }}
            </v-chip>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

const dispositivos = ref({});

const fetchAndOverwrite = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:5000/api/gestion");
    dispositivos.value = response.data;
    console.log("Datos actualizados desde el backend");
  } catch (error) {
    console.error("Error al obtener datos desde el servidor:", error);
  }
};

onMounted(fetchAndOverwrite);
</script>
