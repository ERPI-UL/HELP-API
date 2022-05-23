import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import Register from "./views/Register.vue";
import Scenarios from "./views/Scenarios.vue";
import Machines from "./views/Machines.vue";
import Statistics from "./views/Statistics.vue";
import Easyconnect from "./views/Easyconnect.vue";
import Admin from "./views/Admin.vue";
import Profile from "./views/Profile.vue";
import CreateScenario from "./views/CreateScenario.vue";
import CreateMachine from "./views/CreateMachine.vue";
import Reset from "./views/Reset.vue";

import './index.css'
import "flowbite"

// https redirection (should be done in NGINX, but it not we do it here)
// if (window.location.protocol !== 'https:' && window.location.hostname !== 'localhost') {
//     window.location.protocol = 'https:';
// }

const router = createRouter({
    mode: "history",
    history: createWebHistory(),
    routes: [
        { path: '/', name: 'Home', component: Home },
        { path: '/login', name: 'Login', component: Login },
        { path: '/register', name: 'Register', component: Register },
        { path: '/scenarios', name: 'Scenarios', component: Scenarios },
        { path: '/machines', name: 'Machines', component: Machines },
        { path: '/statistics', name: 'Statistics', component: Statistics },
        { path: '/easyconnect', name: 'Easyconnect', component: Easyconnect },
        { path: '/profile', name: 'Profile', component: Profile },
        { path: '/admin', name: 'Admin', component: Admin },
        { path: '/scenarios/create', name: 'CreateScenario', component: CreateScenario },
        { path: '/scenarios/edit', name: 'EditScenario', component: CreateScenario },
        { path: '/machines/create', name: 'CreateMachine', component: CreateMachine },
        { path: '/machines/edit', name: 'EditMachine', component: CreateMachine },
        { path: '/reset', name: 'Reset', component: Reset }
    ]
});

createApp(App).use(router).mount('#app')