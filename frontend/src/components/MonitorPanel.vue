<template>
  <div class="py-8">
    <div class="text-center mb-6">
      <v-icon size="80" color="blue">mdi-chip</v-icon>
      <v-card-title class="text-h4 mb-4">Monitoreo ESP32</v-card-title>
      <p class="text-body-1">Estado y configuración del dispositivo</p>
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
          <v-card-subtitle class="text-body-2 mb-2">{{ device.ubicacion }}</v-card-subtitle>
          <div class="d-flex align-center justify-space-between mt-2">
            <span class="text-caption">Última señal:</span>
            <span class="text-caption">{{ device.localTimestamp }}</span>
          </div>
          <div class="d-flex align-center justify-space-between mt-2">
            <span class="text-caption">Estado:</span>
            <v-chip :color="device.status === 'activo' ? 'green' : 'red'" text-color="white">
              {{ device.status }}
            </v-chip>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'

// URL del blob con SAS Token (lectura + escritura)
const sasURL = 'https://ovitrampa.blob.core.windows.net/imagenes-ovitrampa/gestion.json?sp=rw&st=2025-06-22T19:54:58Z&se=2025-07-26T03:54:58Z&sv=2024-11-04&sr=b&sig=4hbWLUnd8eE9IRFV2GqblzUm69K6hN8Mr0ViQu6xQM0%3D'

const dispositivos = ref({})

const fetchAndOverwrite = async () => {
  try {
    const response = await axios.get(sasURL)
    const rawData = response.data
    const now = new Date()
    const updatedData = {}

    for (const [id, info] of Object.entries(rawData)) {
      const utcDate = new Date(info.timestamp)
      const gmt6Date = new Date(utcDate.getTime() - 6 * 60 * 60 * 1000)
      const diffMin = (now.getTime() - gmt6Date.getTime()) / (1000 * 60)

      const status = diffMin > 1 ? 'inactivo' : 'activo'

      updatedData[id] = {
        ...info,
        status,
        localTimestamp: gmt6Date.toLocaleString()
      }
    }

    dispositivos.value = updatedData

    const saveData = {}
    for (const [id, info] of Object.entries(updatedData)) {
      const { localTimestamp, ...rest } = info
      saveData[id] = rest
    }

    const jsonString = JSON.stringify(saveData, null, 2)

    await axios.put(sasURL, jsonString, {
      headers: {
        'x-ms-blob-type': 'BlockBlob',
        'Content-Type': 'application/json'
      }
    })

    console.log('Archivo gestion.json actualizado exitosamente en Azure Blob Storage')
  } catch (error) {
    console.error('Error al obtener o sobrescribir datos:', error)
  }
}

onMounted(fetchAndOverwrite)
</script>
