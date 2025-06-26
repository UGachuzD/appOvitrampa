/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

import { registerPlugins } from '@/plugins'
import App from './App.vue'
import { createApp } from 'vue'
import 'unfonts.css'
import Router from "./router/index";

const app = createApp(App);
registerPlugins(app);
app.use(Router);
app.mount("#app");
