<template>
    <v-navigation-drawer v-model="localDrawer" temporary>
      <v-list nav dense>
        <v-list-item prepend-icon="mdi-chip" title="Monitorear ESP32" @click="select('monitor')" :active="activeTab === 'monitor'" />
        <v-list-item prepend-icon="mdi-map-marker" title="Ubicación Ovitrampas" @click="select('mapa')" :active="activeTab === 'mapa'" />
        <v-list-item prepend-icon="mdi-cog" title="Ajustes" @click="select('settings')" :active="activeTab === 'settings'" />
      </v-list>
    </v-navigation-drawer>
  </template>
  
  <script setup>
  import { ref, watch } from 'vue'
  
  const props = defineProps(['activeTab', 'drawer'])
  const emit = defineEmits(['navigate', 'update:drawer'])
  
  const localDrawer = ref(props.drawer)
  
  watch(localDrawer, val => emit('update:drawer', val))
  watch(() => props.drawer, val => localDrawer.value = val)
  
  const select = (tab) => {
    emit('navigate', tab)
    localDrawer.value = false
  }
  </script>
  