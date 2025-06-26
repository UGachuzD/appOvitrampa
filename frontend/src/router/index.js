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
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
