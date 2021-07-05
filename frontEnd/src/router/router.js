import Vue from "vue";
import Router from "vue-router";

//컴포넌트 Import
import MainLayout from "/src/components/layout/MainLayout";
import Login from "/src/components/auth/Login";

Vue.use(Router);

const routes = [
  {
    path: "/",
    name: "Login",
    component: Login,
  },
  {
    path: "/Home",
    name: "Home",
    component: MainLayout,
  },
];

const router = new Router({
  mode: "history",
  routes,
});

export default router;
