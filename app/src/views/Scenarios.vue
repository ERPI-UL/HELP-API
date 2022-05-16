<template>
    <div class="min-h-screen flex flex-col">
        <div class="p-2">
            <Topbar></Topbar>
        </div>
        <div class="block md:flex grow">
            <div class="m-2 grow-0">
                <div class="bg-white rounded min-w-[12vw] divide-y grow">
                    <h2 class="text-2xl leading-9 font-extrabold text-indigo-600 px-6 py-2 whitespace-nowrap">Scénarios</h2>
                    <div class="md:pt-8 flex md:flex-col md:overflow-x-visible overflow-x-scroll justify-between">
                        <a class="whitespace-nowrap md:min-w-full md:p-4 md:m-4 p-2 m-2 rounded-lg text-base font-semibold text-left text-indigo-800 outline-none hover:border-indigo-300" 
                            :class="(window.location.href.split('#')[1] == 'all')?'bg-indigo-600 text-indigo-50 shadow-lg shadow-indigo-600': ''"
                            href="#all">
                            Tous les scénarios
                        </a>
                        <a v-if="user.canLearner()" class="whitespace-nowrap md:min-w-full md:p-4 md:m-4 p-2 m-2 rounded-lg text-base font-semibold text-left text-indigo-800 outline-none hover:border-indigo-300"
                            :class="(window.location.href.split('#')[1] == 'pending')?'bg-indigo-600 text-indigo-50 shadow-lg shadow-indigo-600': ''"
                            href="#pending">
                            Scénarios en cours
                        </a>
                        <a v-if="user.canLearner()" class="whitespace-nowrap md:min-w-full md:p-4 md:m-4 p-2 m-2 rounded-lg text-base font-semibold text-left text-indigo-800 outline-none hover:border-indigo-300"
                            :class="(window.location.href.split('#')[1] == 'completed')?'bg-indigo-600 text-indigo-50 shadow-lg shadow-indigo-600': ''"
                            href="#completed">
                            Scénarios complétés
                        </a>
                        <a v-if="user.canTeacher()" class="whitespace-nowrap md:min-w-full md:p-4 md:m-4 p-2 m-2 rounded-lg text-base font-semibold text-left text-indigo-800 outline-none hover:border-indigo-300"
                            :class="(window.location.href.split('#')[1] == 'editing')?'bg-indigo-600 text-indigo-50 shadow-lg shadow-indigo-600': ''"
                            href="#editing">
                            Créer / Modifier
                        </a>
                    </div>
                </div>
            </div>
            <div class="flex flex-col">
                <div v-if="window.location.href.split('#')[1] == 'editing'" class="m-4 w-fit h-fit">
                    <RedirectButton href="/scenarios/create">
                        <component :is="icon.plus" class="flex-shrink-0 h-5 text-white mr-2" aria-hidden="true" />
                        Nouveau scénario
                    </RedirectButton>
                </div>
                <div class="m-2 ml-4 flex grow flex-wrap justify-evenly"> <!-- Scenario -->
                    <Scenario v-if="window.location.href.split('#')[1] == 'all'" v-for="item in scenarios.all">
                        <template v-slot:title>{{item.title}}</template>
                        <template v-slot:machine>{{item.machine}}</template>
                        <template v-slot:description>{{item.description}}</template>
                        <template v-if="!user.isVisitor()" v-slot:href><RedirectButton :href="item.href">Démarrer</RedirectButton></template>
                    </Scenario>
                    <Scenario v-if="window.location.href.split('#')[1] == 'editing'" v-for="item in scenarios.editing">
                        <template v-slot:title>{{item.title}}</template>
                        <template v-slot:machine>{{item.machine}}</template>
                        <template v-slot:description>{{item.description}}</template>
                        <template v-slot:progress>{{item.progress}}</template>
                        <template v-slot:href><RedirectButton :href="item.href">Editer</RedirectButton></template>
                    </Scenario>
                    <Scenario v-if="window.location.href.split('#')[1] == 'pending'" v-for="item in scenarios.pending">
                        <template v-slot:title>{{item.title}}</template>
                        <template v-slot:machine>{{item.machine}}</template>
                        <template v-slot:description>{{item.description}}</template>
                        <template v-slot:progress>{{item.progress}}</template>
                        <template v-slot:href><RedirectButton :href="item.href">Continuer</RedirectButton></template>
                    </Scenario>
                    <Scenario v-if="window.location.href.split('#')[1] == 'completed'" v-for="item in scenarios.completed">
                        <template v-slot:title>{{item.title}}</template>
                        <template v-slot:machine>{{item.machine}}</template>
                        <template v-slot:description>{{item.description}}</template>
                        <template v-slot:href></template>
                    </Scenario>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Topbar from "../components/Topbar.vue";
import Scenario from "../components/Scenario.vue";
import RedirectButton from "../components/RedirectButton.vue";
import User from "../script/User";

import {
    PlusIcon
} from "@heroicons/vue/solid";

let dom = null;

const scenarios = {
    all: [
        {title: "Scénario démo", machine: "ML-W960", description: "Scénario de démonstration du fonctionnement d'Indico AR", href: ""},
        {title: "Classique", machine: "ML-W960", description: "Scénario par défaut sur le fonctionnement de la découpeuse laser ML-W960", href: ""}
    ],
    editing: [
        {title: "Scénario démo", machine: "ML-W960", description: "Scénario de démonstration du fonctionnement d'Indico AR", href: "/scenarios/edit?idScenario=1"}
    ],
    pending: [
        {title: "Scénario test", machine: "ML-W960", description: "Scénario de test avec 15 étapes faciles", progress: "12/15", href: ""}
    ],
    completed: [
        {title: "Scénario inutile", machine: "ML-W960", description: "Scénario sans vrai description", href: "/login"},
    ]
}

setTimeout(() => {
    scenarios.all.push(
        {title: "Problème", machine: "ML-W960", description: "Scénario de sécurité en cas de problème sur la découpeuse laser ML-W960", href: ""}
    );
    if (dom != null) dom.$forceUpdate();
}, 1000);
setTimeout(() => {
    scenarios.pending.push(
        {title: "Scénario en cours", machine: "ML-W960", description: "Scénario en cours pour voir", progress: "4/9", href: ""}
    );
    if (dom != null) dom.$forceUpdate();
}, 1500);

export default {
    name: "Scenarios",
    components: {
        Topbar,
        Scenario,
        RedirectButton
    },
    setup() {
        return {window, scenarios, user: User.currentUser, icon: {plus: PlusIcon}}
    },
    mounted() {
        dom = this;
    }
};
</script>