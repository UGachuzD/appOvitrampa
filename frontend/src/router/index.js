import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import Home from "../views/Home.vue";

const routes = [
  {
    path: "/",
    component: Login,
    name: "Login",
  },
  {
    path: "/home",
    component: Home,
    name: "Home",
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// Guard global para autenticación
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");

  if (to.meta.requiresAuth && !token) {
    next({ name: "Login" });
  } else if (to.name === "Login" && token) {
    next({ name: "Home" });
  } else {
    next();
  }
});


export default router;
