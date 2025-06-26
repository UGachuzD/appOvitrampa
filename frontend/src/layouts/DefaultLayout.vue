<template>
    <v-app>
      <AppBar @navigate="navigateTo" @logout="emit('logout')" @toggle-drawer="toggleDrawer" />
      <NavigationDrawer :activeTab="activeTab" :drawer="drawer" @navigate="navigateTo" @update:drawer="val => drawer = val" />
      <v-main>
        <slot />
      </v-main>
      <v-footer app color="surface" class="py-2">
        <v-spacer />
        <span class="text-caption text-disabled">Sistema de monitoreo &copy; {{ new Date().getFullYear() }}</span>
        <v-spacer />
      </v-footer>
    </v-app>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import AppBar from '@/components/AppBar.vue'
  import NavigationDrawer from '@/components/NavigationDrawer.vue'
  
  defineProps(['activeTab'])
  const emit = defineEmits(['navigate', 'logout'])
  
  const drawer = ref(false)
  
  const navigateTo = (tab) => {
    emit('navigate', tab)
  }
  const toggleDrawer = () => {
    drawer.value = !drawer.value
  }
  </script>
  