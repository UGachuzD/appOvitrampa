<template>
  <v-container class="py-8 px-4">
    <!-- Hero -->
    <div class="text-center mb-8">
      <v-icon size="80" color="primary" class="mb-4 neon-icon"
        >mdi-cog-sync</v-icon
      >
      <h2 class="text-h3 my-4 font-weight-bold gradient-text">
        Panel de Control
      </h2>
      <p class="text-body-1 text-medium-emphasis">
        Personaliza el comportamiento del sistema
      </p>
    </div>

    <!-- Formulario -->
    <v-card v-if="cargado" class="glass-card pa-6 mb-6" elevation="0">
      <v-form @submit.prevent="actualizarConfiguracion">
        <v-row dense>
          <v-col cols="12" class="mt-2">
  <v-checkbox
    v-model="editarAzure"
    label="Editar configuración avanzada de Azure"
    color="primary"
  />
</v-col>

<v-col cols="12" md="4">
  <v-text-field
    v-model="ajustes.blobBase"
    label="Blob Base"
    :disabled="!editarAzure"
    variant="outlined"
    color="deep-purple"
    prepend-inner-icon="mdi-link"
  />
</v-col>

<v-col cols="12" md="4">
  <v-text-field
    v-model="ajustes.sasTokenEscritura"
    label="SAS Token Escritura"
    :disabled="!editarAzure"
    variant="outlined"
    color="deep-purple"
    prepend-inner-icon="mdi-key"
  />
</v-col>

<v-col cols="12" md="4">
  <v-text-field
    v-model="ajustes.urlGestion"
    label="URL Gestión"
    :disabled="!editarAzure"
    variant="outlined"
    color="deep-purple"
    prepend-inner-icon="mdi-file-document-edit"
  />
</v-col>

          <v-col cols="12" md="6">
            <v-text-field
              v-model="ajustes.horasTomaFoto"
              label="Horas entre capturas"
              type="number"
              min="0"
              required
              variant="outlined"
              color="primary"
              prepend-inner-icon="mdi-clock-outline"
              class="animated-field"
            />
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field
              v-model="ajustes.intervaloRevision"
              label="Intervalo de revisión (segundos)"
              type="number"
              min="0"
              required
              variant="outlined"
              color="primary"
              prepend-inner-icon="mdi-timer-sand"
              class="animated-field"
            />
          </v-col>

          <!-- Activar botón Modo Instantáneo -->
          <!-- Botones alineados -->
          <v-col cols="12">
            <v-row justify="center" align="center" class="mt-4" dense>
              <v-col cols="12" md="6" class="d-flex justify-center">
                <v-btn
                  :disabled="modoActivo"
                  color="success"
                  variant="tonal"
                  rounded="lg"
                  class="ma-2"
                  @click="activarModoInstantaneo"
                  prepend-icon="mdi-flash"
                >
                  {{
                    modoActivo
                      ? `Modo activo (${contador}s)`
                      : "Activar Modo Instantáneo"
                  }}
                </v-btn>
              </v-col>

              <v-col cols="12" md="6" class="d-flex justify-center">
                <v-btn
                  color="primary"
                  type="submit"
                  :loading="cargando"
                  size="large"
                  rounded="lg"
                  class="ma-2"
                  prepend-icon="mdi-cloud-upload"
                >
                  <template v-slot:loader>
                    <v-progress-circular
                      indeterminate
                      color="white"
                      size="24"
                    />
                  </template>
                  {{ cargando ? "Actualizando..." : "Guardar Configuración" }}
                </v-btn>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-form>
    </v-card>

    <!-- Alerta -->
    <transition name="slide-fade">
      <v-alert
        v-if="mensaje"
        :type="exito ? 'success' : 'error'"
        class="floating-alert"
        elevation="8"
        :icon="exito ? 'mdi-check-circle' : 'mdi-alert-circle'"
        closable
        @click:close="mensaje = ''"
      >
        <strong>{{ mensaje }}</strong>
      </v-alert>
    </transition>
  </v-container>
</template>
<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const ajustes = ref({
  horasTomaFoto: null,
  intervaloRevision: null,
  tomaInstanteanea: false,
  blobBase: "",
  sasTokenEscritura: "",
  urlGestion: ""
});

const jsonOriginal = ref({});
const cargando = ref(false);
const cargado = ref(false);
const mensaje = ref("");
const exito = ref(true);

const modoActivo = ref(false);
const contador = ref(10);
let intervalo;

const editarAzure = ref(false);

const obtenerConfiguracion = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:5000/api/control");
    jsonOriginal.value = res.data;

    ajustes.value.horasTomaFoto = res.data.horasTomaFoto;
    ajustes.value.intervaloRevision = res.data.intervaloRevision;
    ajustes.value.tomaInstanteanea = res.data.tomaInstanteanea === "Activado";

    ajustes.value.blobBase = res.data.blobBase;
    ajustes.value.sasTokenEscritura = res.data.sasTokenEscritura;
    ajustes.value.urlGestion = res.data.urlGestion;

    cargado.value = true;
  } catch (error) {
    mensaje.value = "Error al cargar configuración.";
    exito.value = false;
  }
};

const actualizarCampoInstantaneo = async (estado) => {
  try {
    const nuevoJson = {
      ...jsonOriginal.value,
      tomaInstanteanea: estado,
    };

    const res = await axios.put("http://127.0.0.1:5000/api/control", nuevoJson);
    jsonOriginal.value = res.data;

    mensaje.value = `Modo Instantáneo ${estado === "Activado" ? "activado" : "desactivado"} correctamente.`;
    exito.value = true;
  } catch (err) {
    mensaje.value = "Error al actualizar Modo Instantáneo.";
    exito.value = false;
  }
};

const activarModoInstantaneo = async () => {
  modoActivo.value = true;
  contador.value = 10;

  await actualizarCampoInstantaneo("Activado");

  intervalo = setInterval(async () => {
    contador.value--;

    if (contador.value <= 0) {
      clearInterval(intervalo);
      modoActivo.value = false;

      await actualizarCampoInstantaneo("Desactivado");
    }
  }, 1000);
};

const actualizarConfiguracion = async () => {
  cargando.value = true;
  mensaje.value = "";

  try {
    const nuevoJson = {
      ...jsonOriginal.value,
      horasTomaFoto: parseInt(ajustes.value.horasTomaFoto, 10),
      intervaloRevision: parseInt(ajustes.value.intervaloRevision, 10),
      tomaInstanteanea: ajustes.value.tomaInstanteanea ? "Activado" : "Desactivado",
    };

    if (editarAzure.value) {
      nuevoJson.blobBase = ajustes.value.blobBase;
      nuevoJson.sasTokenEscritura = ajustes.value.sasTokenEscritura;
      nuevoJson.urlGestion = ajustes.value.urlGestion;
    }

    const res = await axios.put("http://127.0.0.1:5000/api/control", nuevoJson);
    jsonOriginal.value = res.data;

    mensaje.value = "Configuración actualizada exitosamente.";
    exito.value = true;
  } catch (err) {
    mensaje.value = "Error al actualizar configuración.";
    exito.value = false;
  } finally {
    cargando.value = false;
  }
};

onMounted(obtenerConfiguracion);
</script>
