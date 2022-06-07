<template>
    <!-- Home page, with topbar and a little window with some basic introduction text -->
    <div class="flex flex-col h-screen">
        <div class="p-2">
            <Topbar></Topbar>
        </div>
        <div v-if="User.currentUser.isVisitor()" class="flex grow m-2">
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
        </div>
        <div v-if="User.currentUser.canLearner()" class="flex md:flex-row flex-col md:m-4 m-2 grow min-h-0">
            <div class="md:mr-2 m-0 min-w-0 max-w-full">
                <!-- Left panel containing the different scenario view modes -->
                <div class="bg-white rounded min-w-[12vw] divide-y grow min-w-0 w-fit" ref="menu">
                    <h2 class="text-2xl font-extrabold text-indigo-600 px-6 py-2 whitespace-nowrap min-w-fit">Accès rapide</h2>
                    <div class="flex md:flex-col md:overflow-x-visible overflow-x-scroll justify-between py-2">
                        <p class="whitespace-nowrap py-1 px-2 mx-4 my-1 rounded-lg text-base font-semibold text-left text-indigo-800 cursor-pointer"
                           :class="menu.selectedOption == 'recent'? 'bg-indigo-600 text-indigo-50 shadow-md shadow-indigo-600': ''"
                           v-on:click="menu.selectedOption = 'recent'; selectOption()">
                            Fréquement utilisé
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
            </div>
            <div class="flex flex-col grow min-h-0">
                <div id="overview" class="flex grow min-h-0">
                    <div class="flex grow bg-white rounded-lg border border-gray-200 mx-4">
                        <div class="flex flex-col mx-4 my-2 px-4">
                            <CardTitle class="py-2">
                                <template v-slot:title>Dernière session</template>
                            </CardTitle>
                            <div id="stat-zone" class="flex flex-col space-y-2"></div>
                        </div>
                        <div class="flex grow m-4 min-h-0 max-h-full">
                            <canvas id="chart-canvas" class="flex m-auto min-w-0 min-h-0 h-80"></canvas>
                        </div>
                    </div>
                </div>
                <div id="shortcuts" class="flex flex-wrap justify-center">
                    <MenuDiv title="Fréquement utilisé" v-show="menu.selectedOption == 'recent'">
                        <MenuCard>
                            <CardTitle>
                                <template v-slot:path>
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M8 .01M12 .01M16 .01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </template>
                                <template v-slot:title>- - - - - - - -</template>
                            </CardTitle>
                            <p class="whitespace-wrap text-gray-600">- - - - - - - - - - - - - - - -</p>
                            <div class="flex grow-0 md:justify-end justify-center">
                                <RedirectButton href="/statistics#learning">- - - - - - - -</RedirectButton>
                            </div>
                        </MenuCard>
                    </MenuDiv>
                    <MenuDiv title="Compte" v-show="menu.selectedOption == 'account'">
                        <MenuCard>
                            <CardTitle>
                                <template v-slot:path>
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                </template>
                                <template v-slot:title>Mon profil</template>
                            </CardTitle>
                            <p class="whitespace-wrap text-gray-600">Voir et modifier mon profil</p>
                            <div class="flex grow-0 md:justify-end justify-center">
                                <RedirectButton href="/profile">Mon profil</RedirectButton>
                            </div>
                        </MenuCard>
                        <MenuCard>
                            <CardTitle>
                                <template v-slot:path>
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                                </template>
                                <template v-slot:title>Easy Connect</template>
                            </CardTitle>
                            <p class="whitespace-wrap text-gray-600">Connecter un appareil</p>
                            <div class="flex grow-0 md:justify-end justify-center">
                                <RedirectButton href="/easyconnect">Connecter</RedirectButton>
                            </div>
                        </MenuCard>
                        <MenuCard v-if="User.currentUser.canAdmin()">
                            <CardTitle>
                                <template v-slot:path>
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                </template>
                                <template v-slot:title>Administration</template>
                            </CardTitle>
                            <p class="whitespace-wrap text-gray-600">Voir le panneau d'administration</p>
                            <div class="flex grow-0 md:justify-end justify-center">
                                <RedirectButton href="/admin">Afficher le panneau</RedirectButton>
                            </div>
                        </MenuCard>
                    </MenuDiv>
                    <MenuDiv title="Statistiques" v-show="menu.selectedOption == 'statistics'">
                        <MenuCard>
                            <CardTitle>
                                <template v-slot:path>
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z" />
                                </template>
                                <template v-slot:title>Mode apprentissage</template>
                            </CardTitle>
                            <p class="whitespace-wrap text-gray-600">Voir mes statistiques en mode apprentissage</p>
                            <div class="flex grow-0 md:justify-end justify-center">
                                <RedirectButton href="/statistics#learning">Mode apprentissage</RedirectButton>
                            </div>
                        </MenuCard>
                        <MenuCard>
                            <CardTitle>
                                <template v-slot:path>
                                    <path d="M12 14l9-5-9-5-9 5 9 5z" />
                                    <path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222" />
                                </template>
                                <template v-slot:title>Mode Évaluation</template>
                            </CardTitle>
                            <p class="whitespace-wrap text-gray-600">Voir mes statistiques en mode évaluation</p>
                            <div class="flex grow-0 md:justify-end justify-center">
                                <RedirectButton href="/statistics#testing">Mode évaluation</RedirectButton>
                            </div>
                        </MenuCard>
                    </MenuDiv>
                    <MenuDiv title="Scénarios" v-show="menu.selectedOption == 'scenarios'">
                        <MenuCard>
                            <CardTitle>
                                <template v-slot:path>
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                </template>
                                <template v-slot:title>Voir les scénarios</template>
                            </CardTitle>
                            <p class="whitespace-wrap text-gray-600">Voir les scénarios disponibles</p>
                            <div class="flex grow-0 md:justify-end justify-center">
                                <RedirectButton href="/scenarios">Voir les scénarios</RedirectButton>
                            </div>
                        </MenuCard>
                        <MenuCard v-if="User.currentUser.canTeacher()">
                            <CardTitle>
                                <template v-slot:path>
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                                </template>
                                <template v-slot:title>Modifier un scénario</template>
                            </CardTitle>
                            <p class="whitespace-wrap text-gray-600">Modifier ou supprimer un scénario</p>
                            <div class="flex grow-0 md:justify-end justify-center">
                                <RedirectButton href="/scenarios#editing">Modifier un scénarios</RedirectButton>
                            </div>
                        </MenuCard>
                        <MenuCard v-if="User.currentUser.canTeacher()">
                            <CardTitle>
                                <template v-slot:path>
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
                                </template>
                                <template v-slot:title>Créer un scénario</template>
                            </CardTitle>
                            <p class="whitespace-wrap text-gray-600">Créer un nouveau scénario</p>
                            <div class="flex grow-0 md:justify-end justify-center">
                                <RedirectButton href="/scenarios/create">Créer un scénarios</RedirectButton>
                            </div>
                        </MenuCard>
                    </MenuDiv>
                    <MenuDiv title="Machines" v-show="menu.selectedOption == 'machines'">
                        <MenuCard>
                            <CardTitle>
                                <template v-slot:path>
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                </template>
                                <template v-slot:title>Voir les machines</template>
                            </CardTitle>
                            <p class="whitespace-wrap text-gray-600">Voir les machines disponibles</p>
                            <div class="flex grow-0 md:justify-end justify-center">
                                <RedirectButton href="/machines#all">Voir les machines</RedirectButton>
                            </div>
                        </MenuCard>
                        <MenuCard v-if="User.currentUser.canTeacher()">
                            <CardTitle>
                                <template v-slot:path>
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                                </template>
                                <template v-slot:title>Modifier une machine</template>
                            </CardTitle>
                            <p class="whitespace-wrap text-gray-600">Modifier ou supprimer une machine</p>
                            <div class="flex grow-0 md:justify-end justify-center">
                                <RedirectButton href="/machines#editing">Modifier une machine</RedirectButton>
                            </div>
                        </MenuCard>
                        <MenuCard v-if="User.currentUser.canTeacher()">
                            <CardTitle>
                                <template v-slot:path>
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
                                </template>
                                <template v-slot:title>Créer une machine</template>
                            </CardTitle>
                            <p class="whitespace-wrap text-gray-600">Créer une nouvelle machine</p>
                            <div class="flex grow-0 md:justify-end justify-center">
                                <RedirectButton href="/machines/create">Créer une machine</RedirectButton>
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
    card.classList.add("flex", "grow-0", "space-x-4", "justify-between");
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
        title: "cocou",
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
            responsive: false,
            maintainAspectRatio: false
        }
    });

}

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
        return {User, menu, selectOption}
    },
    mounted() {
        setup();
    }
};
</script>


<style>
</style>