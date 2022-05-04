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

createApp(App).use(router).mount('#app')