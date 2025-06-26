<template>
  <v-container class="fill-height" fluid style="background-color: #f5f5f5">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card elevation="12" class="pa-8 rounded-lg" color="surface">
          <div class="text-center mb-6">
            <v-avatar size="72" color="primary" class="mb-4">
              <v-icon size="40" color="white">mdi-account-circle</v-icon>
            </v-avatar>
            <v-card-title class="text-h4 font-weight-bold text-primary">
              Iniciar sesión
            </v-card-title>
            <v-card-subtitle class="text-body-1">
              Ingresa tus credenciales para continuar
            </v-card-subtitle>
          </div>

          <v-form v-model="formValid" @submit.prevent="handleLogin">
            <v-text-field
              v-model="email"
              label="Correo electrónico"
              prepend-inner-icon="mdi-email-outline"
              type="email"
              :rules="emailRules"
              required
              variant="outlined"
              color="primary"
              class="mb-4"
              clearable
            />

            <v-text-field
              v-model="password"
              label="Contraseña"
              prepend-inner-icon="mdi-lock-outline"
              :type="showPassword ? 'text' : 'password'"
              :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append-inner="showPassword = !showPassword"
              :rules="passwordRules"
              required
              variant="outlined"
              color="primary"
              class="mb-2"
            />

            <div class="d-flex justify-end mb-4">
              <a
                href="#"
                class="text-caption text-primary text-decoration-none"
              >
                ¿Olvidaste tu contraseña?
              </a>
            </div>

            <v-btn
              :disabled="!formValid"
              :loading="loading"
              type="submit"
              color="primary"
              class="mt-2"
              block
              size="large"
              rounded="pill"
              append-icon="mdi-arrow-right"
            >
              Entrar
            </v-btn>
          </v-form>

          <v-divider class="my-6" />

          <div class="text-center">
            <span class="text-caption text-disabled"
              >¿No tienes una cuenta?</span
            >
            <a
              href="#"
              class="text-caption text-primary text-decoration-none ml-2"
            >
              Regístrate ahora
            </a>
          </div>
        </v-card>

        <!-- Snackbar mejorado -->
        <v-snackbar
          v-model="snackbar"
          :color="snackbarColor"
          timeout="3000"
          location="bottom center"
          rounded="pill"
          elevation="12"
        >
          <div class="d-flex align-center">
            <v-icon class="mr-2">
              {{
                snackbarColor === "success"
                  ? "mdi-check-circle"
                  : "mdi-alert-circle"
              }}
            </v-icon>
            {{ snackbarText }}
          </div>

          <template v-slot:actions>
            <v-btn
              variant="text"
              :color="snackbarColor === 'success' ? 'white' : 'white'"
              @click="snackbar = false"
              icon="mdi-close"
            />
          </template>
        </v-snackbar>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();
const email = ref("");
const password = ref("");
const formValid = ref(false);
const showPassword = ref(false);
const loading = ref(false);

const snackbar = ref(false);
const snackbarColor = ref("success");
const snackbarText = ref("");

const emailRules = [
  (v) => !!v || "El correo es requerido",
  (v) => /.+@.+\..+/.test(v) || "Correo no válido",
];

const passwordRules = [
  (v) => !!v || "La contraseña es requerida",
  (v) => v.length >= 6 || "Mínimo 6 caracteres",
];

const handleLogin = async () => {
  try {
    loading.value = true;
    const response = await axios.post("http://127.0.0.1:5000/login", {
      email: email.value,
      password: password.value,
    });

    const token = response.data.access_token;
    localStorage.setItem("token", token);

    snackbarText.value = "Login exitoso";
    snackbarColor.value = "success";
    snackbar.value = true;

    // Pequeño delay para permitir ver el mensaje antes de redirigir
    setTimeout(() => {
      router.push("/home");
    }, 1000);
  } catch (error) {
    const msg =
      error.response?.data?.msg || error.message || "Error desconocido";
    snackbarText.value = "Login fallido: " + msg;
    snackbarColor.value = "error";
    snackbar.value = true;
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.v-card {
  transition: transform 0.3s ease;
}

.v-card:hover {
  transform: translateY(-5px);
}

.v-btn {
  text-transform: none;
  letter-spacing: normal;
}

.v-text-field :deep(.v-input__details) {
  padding-left: 8px;
}
</style>
