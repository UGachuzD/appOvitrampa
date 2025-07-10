<template>
  <DefaultLayout :activeTab="activeTab" @navigate="navigateTo" @logout="handleLogout">
    <v-container fluid class="fill-height">
      <v-row class="fill-height">
        <v-col cols="12">
          <v-card class="pa-6 rounded-lg" elevation="4">
            <v-card-text>
              <v-window v-model="activeTab">
                <v-window-item value="monitor">
                  <MonitorPanel />
                </v-window-item>

                <v-window-item value="mapa">
                  <MapaOvitrampas />
                </v-window-item>

                <v-window-item value="settings">
                  <SettingsPanel />
                </v-window-item>
              </v-window>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </DefaultLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import DefaultLayout from '@/layouts/DefaultLayout.vue'
import MonitorPanel from '@/components/MonitorPanel.vue'
import MapaOvitrampas from '@/components/MapaOvitrampas.vue'
import SettingsPanel from '@/components/SettingsPanel.vue'

const activeTab = ref('monitor')
const router = useRouter()

const navigateTo = (tab) => {
  activeTab.value = tab
}

const handleLogout = () => {
  localStorage.removeItem('token')
  router.push({ name: 'Login' }) // ← más robusto que usar '/'
}

</script>

<style scoped>
.v-card {
  transition: all 0.3s ease;
}
.v-card:hover {
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1) !important;
}
</style>
