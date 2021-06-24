import Vue from 'vue'
import Router from 'vue-router'

//컴포넌트 Import
import MainLayout from "/src/components/layout/MainLayout";


Vue.use(Router)

const routes = [
    {
        path: "/",
        name: "MainLayout",
        component: MainLayout,
    },
];

const router = new Router({
    mode: 'history',
    routes,

});

export default router;