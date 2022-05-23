<template>
    <div class="min-h-screen flex flex-col">
        <div class="p-2">
            <Topbar></Topbar>
        </div>
        <div class="block md:flex grow">
            <div class="m-2 grow-0">
                <div class="bg-white rounded min-w-[12vw] divide-y grow">
                    <h2 class="text-2xl leading-9 font-extrabold text-indigo-600 px-6 py-2 whitespace-nowrap">Statistiques</h2>
                    <div class="md:pt-8 flex md:flex-col md:overflow-x-visible overflow-x-scroll justify-between">
                        <a class="whitespace-nowrap md:min-w-full md:p-4 md:m-4 p-2 m-2 rounded-lg text-base font-semibold text-left text-indigo-800 outline-none hover:border-indigo-300" 
                            :class="(window.location.href.split('#')[1] == 'learning')?'bg-indigo-600 text-indigo-50 shadow-lg shadow-indigo-600': ''"
                            href="#learning">
                            Apprentissage
                        </a>
                        <a class="whitespace-nowrap md:min-w-full md:p-4 md:m-4 p-2 m-2 rounded-lg text-base font-semibold text-left text-indigo-800 outline-none hover:border-indigo-300"
                            :class="(window.location.href.split('#')[1] == 'testing')?'bg-indigo-600 text-indigo-50 shadow-lg shadow-indigo-600': ''"
                            href="#testing">
                            Évaluations
                        </a>
                    </div>
                </div>
            </div>
            <div class="m-4 grow">
                <div class="bg-white shadow-lg p-2 rounded-lg w-full h-fit flex md:flex-row flex-col grow">
                    <div class="flex md:justify-left justify-between md:mr-6" v-if="user.canTeacher()">
                        <h2 class="m-1 p-1">Utilisateurs: </h2>
                        <select id="user-select" class="min-w-0 border-none rounded bg-indigo-50 p-1 m-1 pr-8">
                            <option value="<loading>">Chargement ...</option>
                        </select>
                    </div>
                    <div class="flex md:justify-left justify-between md:mr-6">
                        <h2 class="m-1 p-1">Scénarios: </h2>
                        <select id="scenario-select" class="min-w-0 border-none rounded bg-indigo-50 p-1 m-1 pr-8">
                            <option value="<loading>">Chargement ...</option>
                        </select>
                    </div>
                    <div class="flex grow justify-between">
                        <span></span>
                        <ValidateButton v-on:click="search">Chercher</ValidateButton>
                    </div>
                </div>
                <div class="m-2 ml-4 flex flex-col flex-wrap justify-evenly grow"> <!-- Statistiques -->
                    <div class="mt-10 overflow-hidden" id="loadzone" style="display: none;">
                        <p class="text-center md:text-4xl text-2xl text-gray-500">Chargement ...</p>
                        <p class="text-center md:text-2xl text-xl text-gray-400">Chargement des données</p>
                    </div>
                    <div class="mt-10 overflow-hidden" id="nodatazone" style="display: none;">
                        <p class="text-center md:text-4xl text-2xl text-gray-500">Aucune donnée :/</p>
                        <p class="text-center md:text-2xl text-xl text-gray-400">Aucune donnée disponible pour les filtres sélectionnés</p>
                    </div>
                    <div class="mt-10 overflow-hidden" id="errorzone" style="display: none;">
                        <p class="text-center md:text-4xl text-2xl text-gray-500">Houston, on a un problème !</p>
                        <p class="text-center md:text-2xl text-xl text-gray-400">Impossible de récupérer les statistiques</p>
                    </div>
                    <div class="flex flex-col grow max-w-full">
                        <div class="flex flex-wrap grow-0 justify-evenly max-h-full">
                            <InfoBox v-for="box in infoBoxes" :boxTitle="box.title" :boxInfos="box.infos"></InfoBox>
                        </div>
                        <div class="flex flex-wrap grow justify-evenly">
                            <Chart v-for="chart in charts" :title="chart.title" :chartInfos="chart.data"></Chart>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <PaginationChoice
            ref="userPagination" :title="'Sélection utilisateurs'"
            :selectID="'#user-select'" :callback="addUserSelection" :route="API.ROUTE.USERS"
            :displayAttribute="el => el.firstname+' '+el.lastname" :identifier="el => el.id" :selectedValues="availableUsers.map(el => el.id)">
        </PaginationChoice>
        <PaginationChoice
            ref="scenarioPagination" :title="'Sélection scénarios'"
            :selectID="'#scenario-select'" :callback="addScenarioSelection" :route="API.ROUTE.SCENARIOS"
            :displayAttribute="el => el.name" :identifier="el => el.id" :selectedValues="availableScenarios.map(el => el.id)">
        </PaginationChoice>
    </div>
</template>

<script>
import Topbar from "../components/Topbar.vue";
import Chart from "../components/Chart.vue";
import ValidateButton from "../components/ValidateButton.vue";
import User from "../script/User";
import API from '../script/API';
import Statistics from "../script/Statistics";
import InfoBox from "../components/InfoBox.vue";
import PaginationChoice from "../components/PaginationChoice.vue";

let availableUsers = [];
let availableScenarios = [];

const charts = [];
const infoBoxes = [];
var dom = null;

function updateUserSelect(selectValue) {
    const userSelect = document.getElementById("user-select");
    let val = userSelect.value;
    userSelect.innerHTML = "";
    const userOptions = [{value: "<all>", text: "Tous"}];
    availableUsers.forEach(user => userOptions.push(user));
    userOptions.push({value: "<select>", text: "Selectionner ..."});

    userOptions.forEach(option => {
        let optionElement = document.createElement("option");
        optionElement.value = option.value;
        optionElement.text = option.text;
        userSelect.appendChild(optionElement);
    });
    userSelect.value = (val == "" || val == "<loading>" || val == "<select>") ? '<all>': val;
    setTimeout(() => {
        if (selectValue != undefined)
            userSelect.value = selectValue;
    }, 10);
}

function updateScenarioSelect(selectValue) {
    const scenarioSelect = document.getElementById("scenario-select");
    let val = scenarioSelect.value;
    scenarioSelect.innerHTML = "";
    const scenarioOptions = [{value: "<all>", text: "Tous"}];
    availableScenarios.forEach(scenario => scenarioOptions.push(scenario));
    scenarioOptions.push({value: "<select>", text: "Selectionner ..."});

    scenarioOptions.forEach(option => {
        let optionElement = document.createElement("option");
        optionElement.value = option.value;
        optionElement.text = option.text;
        scenarioSelect.appendChild(optionElement);
    });
    scenarioSelect.value = (val == "" || val == "<loading>" || val == "<select>") ? '<all>': val;
    setTimeout(() => {
        if (selectValue != undefined)
            scenarioSelect.value = selectValue;
    }, 10);
}

function setup() {
    let userSelect = document.getElementById("user-select");
    let scenarioSelect = document.getElementById("scenario-select");

    // fill the user select with all the available users and attach listener
    updateUserSelect();
    userSelect.addEventListener("change", ev => {
        if (ev.target.value == "<select>") {
            displayUserPagination();
        }
    });

    // fill the scenario select with all the available scenarios for the current user
    updateScenarioSelect();
    scenarioSelect.addEventListener("change", ev => {
        if (ev.target.value == "<select>") {
            displayScenarioPagination();
        }
    });

    search();
}

function addUserSelection(content) {
    availableUsers = availableUsers.filter(el => el.id in content.map(el => el.id));
    let nbAdded = 0, lastSelectedID = 0;
    content.forEach(el => {
        if (!(el.id in availableUsers.map(el => el.id))) {
            nbAdded++;
            lastSelectedID = el.id;
            availableUsers.push({value: el.id, text: el.firstname+" "+el.lastname});
        }
    });
    updateUserSelect((nbAdded==1)? lastSelectedID: undefined);
}

function addScenarioSelection(content) {
    availableScenarios = availableScenarios.filter(el => el.id in content.map(el => el.id));
    let nbAdded = 0, lastSelectedID = 0;
    content.forEach(el => {
        if (!(el.id in availableScenarios.map(el => el.id))) {
            nbAdded++;
            lastSelectedID = el.id;
            availableScenarios.push({value: el.id, text: el.name});
        }
    });
    updateScenarioSelect((nbAdded==1)? lastSelectedID: undefined);
}

function search() {
    const selectedUser = document.getElementById("user-select").value;
    const selectedScenario = document.getElementById("scenario-select").value;

    charts.splice(0, charts.length);
    infoBoxes.splice(0, infoBoxes.length);

    if (selectedUser == "<error>" || selectedScenario == "<error>") {
        console.error("Error loading data: no data found");
        return;
    }

    let promise = null;
    if (selectedUser == "<all>") { // selected all users, get average informations
        if (selectedScenario == "<all>")
            promise = Statistics.generateStatistics(charts, infoBoxes);
        else
            promise = Statistics.generateScenarioStatistics(charts, infoBoxes, selectedScenario);
    } else { // one user selected, get user informations
        if (selectedScenario == "<all>") // selected all scenarios, get average informations
            promise = Statistics.generateUserStatistics(charts, infoBoxes, selectedUser);
        else // one scenario selected, get scenario informations
            promise = Statistics.generateUserScenarioStatistics(charts, infoBoxes, selectedScenario, selectedUser);
    }

    let hasResults = false;
    if (promise != null)
        promise.then(() => {
            hasResults = true;
            window.indico.refreshStatistics();
        }).catch(err => {});

        setTimeout(() => {
            if (hasResults) return;
            document.getElementById("loadzone").style.display = "none";
            document.getElementById("nodatazone").style.display = "none";
            document.getElementById("errorzone").style.display = "block";
        }, 3000);
}

if (!window.indico) window.indico = {};
window.indico.refreshStatistics = () => {
    if (dom != null) dom.$forceUpdate();
    if (charts.length == 0 && infoBoxes.length == 0)
        document.getElementById("nodatazone").style.display = "block";
    else document.getElementById("nodatazone").style.display = "none";
};

let displayUserPagination;
let displayScenarioPagination;

export default {
    name: "Statistics",
    data: () => {
        return {charts, infoBoxes, user: User.currentUser, API, availableUsers, availableScenarios}
    },
    components: {
        Topbar,
        Chart,
        ValidateButton,
        InfoBox,
        PaginationChoice
    },
    setup() {
        if (!User.currentUser.canLearner()) window.history.back();
        return {window};
    },
    mounted() {
        dom = this;
        displayUserPagination = () => {
            this.$refs["userPagination"].show();
        };
        displayScenarioPagination = () => {
            this.$refs["scenarioPagination"].show();
        };
        setup();
    },
    methods: {search, addUserSelection, addScenarioSelection}
};
</script>

<style>
#loadzone, #nodatazone, #errorzone {
    animation: spawn-in 100ms ease;
}
</style>