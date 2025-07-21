<template>
  <v-app>
    <v-main>
      <v-container class="pa-0 fill-container" fluid>
        <iframe src="/heatmap.html" class="full-frame"></iframe>
      </v-container>
    </v-main>
  </v-app>
</template>

<style scoped>
.fill-container {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.full-frame {
  border: none;
  width: 100%;
  height: 100%;
}
</style>
