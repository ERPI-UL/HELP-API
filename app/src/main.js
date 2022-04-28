import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from './views/Home.vue'
import Explore from './views/Explore.vue'
import ExploreItem from './views/explore/Item.vue'
import ExploreGraph from './views/explore/Graph.vue'
import ExploreSelection from './views/explore/Selection.vue'
import './index.css'
import FloatingVue from 'floating-vue'
import 'floating-vue/dist/style.css'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', name: 'Home', component: Home },
        { path: '/explore', name: 'Explore', component: Explore },
        { path: '/explore/:type/:id', name: 'ExploreItem', component: ExploreItem },
        { path: '/explore/graph/:type', name: 'ExploreGraph', component: ExploreGraph },
        { path: '/explore/selection/:type', name: 'ExploreSelection', component: ExploreSelection },
    ]
})

// Init Local Storage
if (!localStorage.getItem("formultool.emollients")) localStorage.setItem("formultool.emollients", "?")
if (!localStorage.getItem("formultool.surfactants")) localStorage.setItem("formultool.surfactants", "?")

createApp(App)
.use(router)
.use(FloatingVue)
.mount('#app')
