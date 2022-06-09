<template>
    <!-- Home page, with topbar and a little window with some basic introduction text -->
    <div class="flex flex-col h-screen">
        <div class="p-2">
            <Topbar></Topbar>
        </div>
        <div v-if="User.currentUser.isVisitor()" class="flex flex-col grow m-2">
            <div class="flex md:flex-row flex-col m-auto 300 p-4 rounded-lg shadow-lg bg-white">
                <div class="mx-auto">
                    <img class="max-h-[50vw] md:max-h-[30vh] w-auto" src="../assets/images/icons/icon_full.png" alt="" />
                </div>
                <div class="w-full md:w-[30vw] md:p-4 p-2">
                    <h1 class="text-gray-600 text-2xl font-bold text-center">Indico - Interface Web</h1>
                    <br>
                    <p class="text-gray-500 text-lg text-center">Bienvenue sur l'interface web de l'application <span class="font-bold">Indico</span> !</p>
                    <p class="text-gray-500 text-lg text-center">
                        Pour accéder à toutes les fonctionnalités,
                        <a class="text-indigo-600 hover:underline cursor-pointer" href="/login">connectez-vous</a>
                        à l'application, ou
                        <a class="text-indigo-600 hover:underline cursor-pointer" href="/register">créez un compte</a>
                        .
                    </p>
                </div>
            </div>
            <div class="bottom-2 w-full md:block hidden">
                <div class="flex flex-col m-4 p-2 bg-white rounded-lg shadow-lg border border-gray-200 m-auto w-fit">
                    <img class="w-full mx-auto w-80" src="../assets/images/logos/grand_est.png" alt="" />
                    <p class="font-semibold text-gray-600 my-auto mt-2 text-center">Avec le soutien fiancier de la Région Grand Est</p>
                </div>
            </div>
        </div>
        <div v-if="User.currentUser.canLearner()" class="flex md:flex-row flex-col md:m-4 m-2 grow min-h-0">
            <div class="md:mr-2 m-0 min-w-min max-w-full md:flex flex-col hidden w-min justify-between">
                <!-- Left panel containing the different scenario view modes -->
                <div class="bg-white rounded min-w-[12vw] divide-y min-w-0 w-fit" ref="menu">
                    <h2 class="text-2xl font-extrabold text-indigo-600 px-6 py-2 whitespace-nowrap min-w-fit">Accès rapide</h2>
                    <div class="flex md:flex-col md:overflow-x-visible overflow-x-scroll justify-between py-2">
                        <p class="whitespace-nowrap py-1 px-2 mx-4 my-1 rounded-lg text-base font-semibold text-left text-indigo-800 cursor-pointer"
                           :class="menu.selectedOption == 'recent'? 'bg-indigo-600 text-indigo-50 shadow-md shadow-indigo-600': ''"
                           v-on:click="menu.selectedOption = 'recent'; selectOption()">
                            Fréquemment utilisé
                        </p>
                        <p class="whitespace-nowrap py-1 px-2 mx-4 my-1 rounded-lg text-base font-semibold text-left text-indigo-800 cursor-pointer"
                           :class="menu.selectedOption == 'account'? 'bg-indigo-600 text-indigo-50 shadow-md shadow-indigo-600': ''"
                           v-on:click="menu.selectedOption = 'account'; selectOption()">
                            Compte
                        </p>
                        <p class="whitespace-nowrap py-1 px-2 mx-4 my-1 rounded-lg text-base font-semibold text-left text-indigo-800 cursor-pointer"
                           :class="menu.selectedOption == 'statistics'? 'bg-indigo-600 text-indigo-50 shadow-md shadow-indigo-600': ''"
                           v-on:click="menu.selectedOption = 'statistics'; selectOption()">
                            Statistiques
                        </p>
                        <p class="whitespace-nowrap py-1 px-2 mx-4 my-1 rounded-lg text-base font-semibold text-left text-indigo-800 cursor-pointer"
                           :class="menu.selectedOption == 'scenarios'? 'bg-indigo-600 text-indigo-50 shadow-md shadow-indigo-600': ''"
                           v-on:click="menu.selectedOption = 'scenarios'; selectOption()">
                            Scénarios
                        </p>
                        <p class="whitespace-nowrap py-1 px-2 mx-4 my-1 rounded-lg text-base font-semibold text-left text-indigo-800 cursor-pointer"
                           :class="menu.selectedOption == 'machines'? 'bg-indigo-600 text-indigo-50 shadow-md shadow-indigo-600': ''"
                           v-on:click="menu.selectedOption = 'machines'; selectOption()">
                            Machines
                        </p>
                    </div>
                </div>
                <div class="flex grow"></div>
                <div class="flex flex-col m-4 p-2 bg-white rounded-lg shadow-lg border border-gray-200 m-auto max-w-full">
                    <img class="w-full mx-auto" src="../assets/images/logos/grand_est.png" alt="" />
                    <p class="font-semibold text-gray-600 my-auto mt-2 text-center">Avec le soutien fiancier de la Région Grand Est</p>
                </div>
            </div>
            <div class="flex flex-col grow min-h-0 min-w-0">
                <div id="overview" class="flex grow min-h-0 min-w-fit max-w-[full] w-[50%] m-auto">
                    <div class="flex grow flex-col bg-white rounded-lg border border-gray-200">
                        <div class="flex flex-col mx-4 my-2">
                            <h2 class="md:text-2xl text-xl font-extrabold text-indigo-600">Dernière session</h2>
                            <div id="stat-zone" class="flex flex-col space-y-2"></div>
                        </div>
                        <div class="md:flex hidden grow m-4 min-h-0 max-h-full max-w-full min-w-0">
                            <div id="loading-zone" class="flex grow">
                                <div class="flex m-auto">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="rotate h-6 w-6 text-indigo-600 my-1 md:block hidden" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                        <path style="stroke:#4f46e5;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;" d="M 21.8,11.8 A 10,10 0 0 1 11.8,21.8 10,10 0 0 1 1.8,11.8 10,10 Z" />
                                    </svg>
                                    <p class="ml-4 text-xl font-semibold text-indigo-600">Chargement ...</p>
                                </div>
                            </div>
                            <canvas id="chart-canvas" class="flex my-auto min-w-0 min-h-0 max-h-full max-w-full hidden"></canvas>
                        </div>
                    </div>
                </div>
                <div id="shortcuts" class="flex flex-wrap justify-center">
                    <MenuDiv v-for="categ in shortcuts" :title="categ.title" v-show="menu.selectedOption == categ.name">
                        <MenuCard v-for="el in categ.data">
                            <CardTitle :icon="el.icon">
                                <template v-slot:title>{{ el.title }}</template>
                            </CardTitle>
                            <p class="whitespace-wrap text-gray-600">{{ el.description }}</p>
                            <div class="flex grow-0 md:justify-end justify-center">
                                <RedirectButton :href="el.redirect.href">{{ el.redirect.label }}</RedirectButton>
                            </div>
                        </MenuCard>
                    </MenuDiv>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import API from "../script/API";
import User from "../script/User";
import Topbar from "../components/Topbar.vue";
import RedirectButton from "../components/RedirectButton.vue";
import MenuCard from "../components/MenuCard.vue";
import CardTitle from "../components/CardTitle.vue";
import MenuDiv from "../components/MenuDiv.vue";
import Chart from "chart.js/auto";
import { stringTime } from "../script/common";

let menu = {
    selectedOption: "recent"
};
function selectOption(option) {
    if (option) menu.selectedOption = option;
}

function setup() {
    let data = [];
    let labels = [];
    API.execute_logged(API.ROUTE.STATS.USERS + User.currentUser.id + API.ROUTE.STATS.__SESSIONS, API.METHOD_GET, User.currentUser.getCredentials()).then(sessions => {
        if (sessions.data.length > 0)
            API.execute_logged(API.ROUTE.STATS.SESSIONS+sessions.data[0].id, API.METHOD_GET, User.currentUser.getCredentials()).then(session => {
                API.execute_logged(API.ROUTE.SCENARIOS+session.scenario.id, API.METHOD_GET, User.currentUser.getCredentials()).then(scenario => {
                    document.getElementById("chart-canvas").classList.remove("hidden");
                    document.getElementById("loading-zone").classList.add("hidden");
                    labels = scenario.steps.map(step => step.name);
                    data = scenario.steps.map(step => session.playedSteps.filter(playedSteps => playedSteps.step_id === step.id).map(playedStep => playedStep.time).reduce((a, b) => a+b, 0));
                    generateChart(data, labels);
                    addStat("- Scénario :", scenario.name);
                    addStat("- Date :", new Date(Date.parse(session.date)).toLocaleString());
                    addStat("- Temps :", stringTime(session.playedSteps.map(playedStep => playedStep.time).reduce((a, b) => a+b, 0)));
                });
            });
        else document.getElementById("overview").classList.add("hidden");
    });
}

function addStat(title, data) {
    const container = document.getElementById("stat-zone");
    const card = document.createElement("div");
    card.classList.add("flex", "md:flex-row", "flex-col", "grow-0", "space-x-4", "justify-between");
    const titleElement = document.createElement("p");
    titleElement.classList.add("font-semibold", "whitespace-nowrap", "text-lg", "text-gray-600");
    const dataElement = document.createElement("p");
    dataElement.classList.add("font-semibold", "whitespace-nowrap", "text-lg", "text-indigo-600");
    titleElement.innerText = title;
    dataElement.innerText = data;
    card.appendChild(titleElement);
    card.appendChild(dataElement);
    container.appendChild(card);
}

function generateChart(data, labels) {
    let colors = ["#6366F1"];

    let counter = 0;
    let a = Array.from(Array(colors.length), () => colors[Math.floor((counter += Math.max(1, colors.length/labels.length)) % colors.length)]);

    /**@type {HTMLCanvasElement} */
    let canvas = document.getElementById("chart-canvas");
    const chart = new Chart(canvas, {
        title: "last session stats",
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Temps absolu",
                backgroundColor: a,
                borderColor: a,
                data: data,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

const shortcuts = [
    {
        name: "recent",
        title: "Fréquemment utilisé",
        data: [
            /*
            {
                icon: `<path stroke-linecap="round" stroke-linejoin="round" d="M8 .01M12 .01M16 .01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />`,
                title: "- - - - - - - -",
                description: "- - - - - - - -",
                redirect: {
                    label: "- - - - - - - -",
                    href: "/"
                }
            }
            */
        ]
    },
    {
        name: "account",
        title: "Compte",
        data: [
            {
                icon: `<path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />`,
                title: "Mon profil",
                description: "Voir et modifier mon profil",
                redirect: {
                    label: "Mon profil",
                    href: "/profile"
                }
            },
            {
                icon: `<path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />`,
                title: "Easy Connect",
                description: "Connecter un appareil",
                redirect: {
                    label: "Connecter",
                    href: "/easyconnect"
                }
            },
            {
                icon: `<path stroke-linecap="round" stroke-linejoin="round" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />`,
                title: "Administration",
                description: "Voir le panneau d'administration",
                redirect: {
                    label: "Afficher le panneau",
                    href: "/admin"
                }
            }
        ]
    },
    {
        name: "statistics",
        title: "Statistiques",
        data: [
            {
                icon: `<path stroke-linecap="round" stroke-linejoin="round" d="M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z" />`,
                title: "Mode apprentissage",
                description: "Voir mes statistiques en mode apprentissage",
                redirect: {
                    href: "/statistics#learning",
                    label: "Mode apprentissage"
                }
            },
            {
                icon: `<path d="M12 14l9-5-9-5-9 5 9 5z" />
                       <path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                       <path stroke-linecap="round" stroke-linejoin="round" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222" />`,
                title: "Mode Évaluation",
                description: "Voir mes statistiques en mode évaluation",
                redirect: {
                    href: "/statistics#testing",
                    label: "Mode évaluation"
                }
            }
        ]
    },
    {
        name: "scenarios",
        title: "Scénarios",
        data: [
            {
                icon: `<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                       <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />`,
                title: "Voir les scénarios",
                description: "Voir les scénarios disponibles",
                redirect: {
                    href: "/scenarios#all",
                    label: "Voir les scénarios"
                }
            },
            {
                icon: `<path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />`,
                title: "Modifier un scénario",
                description: "Modifier ou supprimer un scénario",
                redirect: {
                    href: "/scenarios#editing",
                    label: "Modifier un scénarios"
                }
            },
            {
                icon: `<path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />`,
                title: "Créer un scénario",
                description: "Créer un nouveau scénario",
                redirect: {
                    href: "/scenarios/create",
                    label: "Créer un scénarios"
                }
            }
        ]
    },
    {
        name: "machines",
        title: "Machines",
        data: [
            {
                icon: `<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                       <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />`,
                title: "Voir les machines",
                description: "Voir les machines disponibles",
                redirect: {
                    href: "/machines#all",
                    label: "Voir les machines"
                }
            },
            {
                icon: `<path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />`,
                title: "Modifier une machine",
                description: "Modifier ou supprimer une machine",
                redirect: {
                    href: "/machines#editing",
                    label: "Modifier une machine"
                }
            },
            {
                icon: `<path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />`,
                title: "Créer une machine",
                description: "Créer une nouvelle machine",
                redirect: {
                    href: "/machines/create",
                    label: "Créer une machine"
                }
            }
        ]
    }
]

export default {
    name: "Home",
    components: {
        Topbar,
        RedirectButton,
        MenuCard,
        CardTitle,
        MenuDiv
    },
    data() {
        return {User, menu, selectOption, shortcuts}
    },
    setup() {
        let recent = shortcuts.find(sc => sc.name == "recent");
        recent.data.push(shortcuts.find(sc => sc.name == "account").data.find(el => el.redirect.href == "/easyconnect"));
        recent.data.push(shortcuts.find(sc => sc.name == "statistics").data.find(el => el.redirect.href == "/statistics#learning"));
        recent.data.push(shortcuts.find(sc => sc.name == "scenarios").data.find(el => el.redirect.href == "/scenarios#all"));
    },
    mounted() {
        setup();
    }
};
</script>


<style>
@keyframes rotate {
    0% {transform: rotate(0deg);}
    40% {transform: rotate(-20deg);}
    90% {transform: rotate(750deg);}
    100% {transform: rotate(720deg);}
}

.rotate {
    animation: rotate 1s ease infinite;
}
</style>