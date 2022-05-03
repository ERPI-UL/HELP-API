import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import Register from "./views/Register.vue";
import Scenarios from "./views/Scenarios.vue";
import Statistics from "./views/Statistics.vue";
import Easyconnect from "./views/Easyconnect.vue";

import './index.css'
import "flowbite"
import FloatingVue from "floating-vue"

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', name: 'Home', component: Home },
        { path: '/login', name: 'Login', component: Login },
        { path: '/register', name: 'Register', component: Register },
        { path: '/scenarios', name: 'Scenarios', component: Scenarios },
        { path: '/statistics', name: 'Statistics', component: Statistics },
        { path: '/easyconnect', name: 'Easyconnect', component: Easyconnect }
    ]
});

// Init Local Storage
if (!localStorage.getItem("formultool.emollients")) localStorage.setItem("formultool.emollients", "?")
if (!localStorage.getItem("formultool.surfactants")) localStorage.setItem("formultool.surfactants", "?")

createApp(App)
.use(router)
.use(FloatingVue)
.mount('#app')
