<template>
    <div class="min-h-screen flex flex-col">
        <div class="p-2">
            <Topbar></Topbar>
        </div>
        <div class="block md:flex" style="flex-grow: 1">
            <div class="m-2" style="flex-grow: 1 0">
                <div class="bg-white rounded min-w-[12vw] divide-y" style="flex-grow: 1">
                    <h2 class="text-2xl leading-9 font-extrabold text-indigo-600 px-6 py-2 whitespace-nowrap">Scénarios</h2>
                    <div class="md:pt-8 flex md:flex-col md:overflow-x-visible overflow-x-scroll justify-between">
                        <a class="whitespace-nowrap md:min-w-full md:p-4 md:m-4 p-2 m-2 rounded-lg text-base font-semibold text-left text-indigo-800 outline-none hover:border-indigo-300" 
                            :class="(window.location.href.split('#')[1] == 'all')?'bg-indigo-600 text-indigo-50 shadow-lg shadow-indigo-600': ''"
                            href="#all">
                            Tous les scénarios
                        </a>
                        <a class="whitespace-nowrap md:min-w-full md:p-4 md:m-4 p-2 m-2 rounded-lg text-base font-semibold text-left text-indigo-800 outline-none hover:border-indigo-300"
                            :class="(window.location.href.split('#')[1] == 'pending')?'bg-indigo-600 text-indigo-50 shadow-lg shadow-indigo-600': ''"
                            href="#pending">
                            Scénarios en cours
                        </a>
                        <a class="whitespace-nowrap md:min-w-full md:p-4 md:m-4 p-2 m-2 rounded-lg text-base font-semibold text-left text-indigo-800 outline-none hover:border-indigo-300"
                            :class="(window.location.href.split('#')[1] == 'completed')?'bg-indigo-600 text-indigo-50 shadow-lg shadow-indigo-600': ''"
                            href="#completed">
                            Scénarios complétés
                        </a>
                    </div>
                </div>
            </div>
            <div class="m-2 ml-4 flex flex-wrap justify-evenly" style="flex-grow: 1"> <!-- Scenario -->
                <Scenario v-if="window.location.href.split('#')[1] == 'all'" v-for="item in scenarios.all">
                    <template v-slot:title>{{item.title}}</template>
                    <template v-slot:machine>{{item.machine}}</template>
                    <template v-slot:description>{{item.description}}</template>
                    <template v-slot:href href="login"><Redirectbutton :href="item.href">Démarrer</Redirectbutton></template>
                </Scenario>
                <Scenario v-if="window.location.href.split('#')[1] == 'pending'" v-for="item in scenarios.pending">
                    <template v-slot:title>{{item.title}}</template>
                    <template v-slot:machine>{{item.machine}}</template>
                    <template v-slot:description>{{item.description}}</template>
                    <template v-slot:progress>{{item.progress}}</template>
                    <template v-slot:href href="login"><Redirectbutton :href="item.href">Continuer</Redirectbutton></template>
                </Scenario>
                <Scenario v-if="window.location.href.split('#')[1] == 'completed'" v-for="item in scenarios.completed">
                    <template v-slot:title>{{item.title}}</template>
                    <template v-slot:machine>{{item.machine}}</template>
                    <template v-slot:description>{{item.description}}</template>
                    <template v-slot:href href="login"></template>
                </Scenario>
            </div>
        </div>
    </div>
</template>

<script>
import Topbar from "../components/Topbar.vue";
import Scenario from "../components/Scenario.vue";
import Redirectbutton from "../components/RedirectButton.vue";

let dom = null;

const scenarios = {
    all: [
        {title: "Scénario démo", machine: "WP-960", description: "Scénario de démonstration du fonctionnement d'Indico AR", href: ""},
        {title: "Classique", machine: "WP-960", description: "Scénario par défaut sur le fonctionnement de la découpeuse laser WP-960", href: ""}
    ],
    pending: [
        {title: "Scénario test", machine: "WP-960", description: "Scénario de test avec 15 étapes faciles", progress: "12/15", href: ""}
    ],
    completed: [
        {title: "Scénario inutile", machine: "WP-960", description: "Scénario sans vrai description", href: "login"},
    ]
}

setTimeout(() => {
    scenarios.all.push(
        {title: "Problème", machine: "WP-960", description: "Scénario de sécurité en cas de problème sur la découpeuse laser WP-960", href: ""}
    );
    if (dom != null) dom.$forceUpdate();
}, 1000);
setTimeout(() => {
    scenarios.pending.push(
        {title: "Scénario en cours", machine: "WP-960", description: "Scénario en cours pour voir", progress: "4/9", href: ""}
    );
    if (dom != null) dom.$forceUpdate();
}, 1500);

export default {
    name: "Scenarios",
    components: {
        Topbar,
        Scenario,
        Redirectbutton
    },
    setup() {
        return {window, scenarios}
    },
    mounted() {
        dom = this;
    }
};
</script>