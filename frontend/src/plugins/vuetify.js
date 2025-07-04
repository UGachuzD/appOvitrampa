/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'

// Tema personalizado
const customTheme = {
  dark: false,
  colors: {
    background: "#FDF9F6",    // fondo crema claro
    surface: "#FFFFFF",
    primary: "#5C1234",       // guinda principal
    secondary: "#AE8730",     // dorado mostaza como acento
    accent: "#C29A57",        // tono dorado más suave para botones u hover
    error: "#D32F2F",
    info: "#1976D2",
    success: "#388E3C",
    warning: "#FBC02D",
  },
};



// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    defaultTheme: 'customTheme',
    // defaultTheme: "light",
    // defaultTheme: "dark",
    themes: {
      customTheme: customTheme,
    }
  },
});
