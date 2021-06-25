import Vue from "vue";
import Router from "vue-router";

//컴포넌트 Import
import MainLayout from "/src/components/layout/MainLayout";
import Print from "/src/components/form/Print";

Vue.use(Router);

const routes = [
  {
    path: "/",
    name: "MainLayout",
    component: MainLayout,
  },
  {
    path: "/print/",
    name: "Print",
    component: Print,
  },
];

const router = new Router({
  mode: "history",
  routes,
});

export default router;