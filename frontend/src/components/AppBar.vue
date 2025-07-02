<template>
    <v-app-bar app color="primary" prominent>
      <v-app-bar-nav-icon variant="text" @click.stop="toggleDrawer" />
      <v-toolbar-title class="text-h5 font-weight-bold">Dashboard</v-toolbar-title>
      <v-spacer />
      <!-- <v-btn icon><v-icon>mdi-bell-outline</v-icon></v-btn> -->
      <v-menu location="bottom">
        <template #activator="{ props }">
          <v-btn icon v-bind="props">
            <v-avatar size="40" color="secondary"><v-icon>mdi-account</v-icon></v-avatar>
          </v-btn>
        </template>
        <v-list>
          <!-- <v-list-item prepend-icon="mdi-cog" title="Configuración" @click="emit('navigate', 'settings')" /> -->
          <v-list-item prepend-icon="mdi-logout" title="Cerrar sesión" @click="emit('logout')" />
        </v-list>
      </v-menu>
    </v-app-bar>
  </template>
  
  <script setup>
  const emit = defineEmits(['navigate', 'logout', 'toggle-drawer'])
  
  const toggleDrawer = () => {
    emit('toggle-drawer')
  }
  </script>
  