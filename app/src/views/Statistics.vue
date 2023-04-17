<template>
    <div class="min-h-screen flex flex-col">
        <div class="p-2">
            <Topbar></Topbar>
        </div>
        <div class="block md:flex grow">
            <div class="m-2 grow-0">
                <!-- Left panel with learning/testing mode choice -->
                <div class="bg-white rounded min-w-[12vw] divide-y grow">
                    <h2 class="text-2xl leading-9 font-extrabold text-indigo-600 px-6 py-2 whitespace-nowrap">Statistiques</h2>
                    <div class="md:pt-8 flex md:flex-col md:overflow-x-visible overflow-x-scroll justify-between">
                        <!-- Learning mode -->
                        <router-link class="whitespace-nowrap md:min-w-full md:p-4 md:m-4 p-2 m-2 rounded-lg text-base font-semibold text-left text-indigo-800 outline-none hover:border-indigo-300" 
                            :class="(window.location.href.split('#')[1] == 'learning')?'bg-indigo-600 text-indigo-50 shadow-lg shadow-indigo-600': ''"
                            to="#learning">
                            {{ User.LANGUAGE.DATA.STATISTICS.PAGES.LEARNING.TITLE }}
                        </router-link>
                        <!-- Testing mode -->
                        <router-link class="whitespace-nowrap md:min-w-full md:p-4 md:m-4 p-2 m-2 rounded-lg text-base font-semibold text-left text-indigo-800 outline-none hover:border-indigo-300"
                            :class="(window.location.href.split('#')[1] == 'testing')?'bg-indigo-600 text-indigo-50 shadow-lg shadow-indigo-600': ''"
                            to="#testing">
                            {{ User.LANGUAGE.DATA.STATISTICS.PAGES.TESTING.TITLE }}
                        </router-link>
                    </div>
                </div>
            </div>
            <!-- Top bar with filters -->
            <div class="m-4 grow">
                <div class="bg-white shadow-lg p-2 rounded-lg w-full h-fit flex md:flex-row flex-col grow">
                    <!-- User selection (only in admin/teacher mode) -->
                    <div class="flex md:justify-left justify-between md:mr-6" v-show="user.canTeacher()">
                        <h2 class="m-1 p-1">{{ User.LANGUAGE.DATA.PAGES.USERS }}: </h2>
                        <select id="user-select" class="min-w-0 border-none rounded bg-indigo-50 p-1 m-1 pr-8">
                            <option value="<loading>">{{ User.LANGUAGE.DATA.ACTIONS.LOADING }} ...</option>
                        </select>
                    </div>
                    <!-- Scenario selection -->
                    <div class="flex md:justify-left justify-between md:mr-6">
                        <h2 class="m-1 p-1">{{ User.LANGUAGE.DATA.PAGES.SCENARIOS }}: </h2>
                        <select id="scenario-select" class="min-w-0 border-none rounded bg-indigo-50 p-1 m-1 pr-8">
                            <option value="<loading>">{{ User.LANGUAGE.DATA.ACTIONS.LOADING }} ...</option>
                        </select>
                    </div>
                    <!-- AR/VR selection -->
                    <div class="flex md:justify-left justify-between md:mr-6">
                        <h2 class="m-1 p-1">{{ User.LANGUAGE.DATA.COMMON.MODE }}: </h2>
                        <select id="scenario-select" class="min-w-0 border-none rounded bg-indigo-50 p-1 m-1 pr-8">
                            <option value="mode_all">{{ User.LANGUAGE.DATA.COMMON.ALL }}</option>
                            <option value="mode_ar">AR</option>
                            <option value="mode_vr">VR</option>
                        </select>
                    </div>
                    <!-- Search button -->
                    <div class="flex grow justify-between">
                        <span></span>
                        <ValidateButton v-on:click="search">{{ User.LANGUAGE.DATA.ACTIONS.SEARCH }}</ValidateButton>
                    </div>
                </div>
                <!-- Statistics list content -->
                <div class="m-2 ml-4 flex flex-col flex-wrap justify-evenly grow">
                    <!-- Loading dom information element -->
                    <div class="mt-10 overflow-hidden" id="loadzone" style="display: none;">
                        <p class="text-center md:text-4xl text-2xl text-gray-500">{{ User.LANGUAGE.DATA.STATISTICS.MESSAGES.LOADING_DATA.TITLE }}</p>
                        <p class="text-center md:text-2xl text-xl text-gray-400">{{ User.LANGUAGE.DATA.STATISTICS.MESSAGES.LOADING_DATA.DESCRIPTION }}</p>
                    </div>
                    <!-- No data dom information element -->
                    <div class="mt-10 overflow-hidden" id="nodatazone" style="display: none;">
                        <p class="text-center md:text-4xl text-2xl text-gray-500">{{ User.LANGUAGE.DATA.STATISTICS.MESSAGES.NO_DATA.TITLE }}</p>
                        <p class="text-center md:text-2xl text-xl text-gray-400">{{ User.LANGUAGE.DATA.STATISTICS.MESSAGES.NO_DATA.DESCRIPTION }}</p>
                    </div>
                    <!-- Error dom information element -->
                    <div class="mt-10 overflow-hidden" id="errorzone" style="display: none;">
                        <p class="text-center md:text-4xl text-2xl text-gray-500">{{ User.LANGUAGE.DATA.STATISTICS.MESSAGES.PROBLEM_DATA.TITLE }}</p>
                        <p class="text-center md:text-2xl text-xl text-gray-400">{{ User.LANGUAGE.DATA.STATISTICS.MESSAGES.PROBLEM_DATA.DESCRIPTION }}</p>
                    </div>
                    <!-- Statistics zone -->
                    <div class="flex flex-col grow max-w-full">
                        <!-- Info boxes at the top -->
                        <div class="flex flex-wrap grow-0 justify-evenly max-h-full">
                            <InfoBox v-for="box in infoBoxes" :boxTitle="box.title" :boxInfos="box.infos"></InfoBox>
                        </div>
                        <!-- Statistics Graphics -->
                        <div class="flex flex-wrap grow justify-evenly">
                            <Chart v-for="chart in charts" :title="chart.title" :chartInfos="chart.data"></Chart>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- User pagination modal -->
        <PaginationChoice v-if="User.currentUser.canTeacher()"
            ref="userPagination" :title="User.LANGUAGE.DATA.PAGINATION.USER_SELECTION"
            :selectID="'#user-select'" :callback="addUserSelection" :route="API.ROUTE.USERS"
            :displayAttribute="el => el.firstname+' '+el.lastname" :identifier="el => el.id" :selectedValues="availableUsers.map(el => el.id)">
        </PaginationChoice>
        <!-- Scenarios pagination modal -->
        <PaginationChoice
            ref="scenarioPagination" :title="User.LANGUAGE.DATA.PAGINATION.SCENARIO_SELECTION"
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

/**
 * Updates the html user select to correspond to the availableUsers variable
 */
function updateUserSelect(selectValue) {
    const userSelect = document.getElementById("user-select");
    let val = userSelect.value;
    userSelect.innerHTML = "";
    const userOptions = [{value: "<all>", text: User.LANGUAGE.DATA.COMMON.ALL}];
    availableUsers.forEach(user => userOptions.push(user));
    userOptions.push({value: "<select>", text: User.LANGUAGE.DATA.ACTIONS.SELECT+" ..."});

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

/**
 * Updates the html scenario select to correspond to the availableScenarios variable
 */
function updateScenarioSelect(selectValue) {
    const scenarioSelect = document.getElementById("scenario-select");
    let val = scenarioSelect.value;
    scenarioSelect.innerHTML = "";
    const scenarioOptions = [{value: "<all>", text: User.LANGUAGE.DATA.COMMON.ALL}];
    availableScenarios.forEach(scenario => scenarioOptions.push(scenario));
    scenarioOptions.push({value: "<select>", text: User.LANGUAGE.DATA.ACTIONS.SELECT+" ..."});

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

/**
 * Adds the event listeners to the user html select and scenario html select
 */
function setup() {
    let userSelect = document.getElementById("user-select");
    let scenarioSelect = document.getElementById("scenario-select");

    // fill the user select with all the available users and attach listener
    if (User.currentUser.canTeacher()) {
        updateUserSelect();
        userSelect.addEventListener("change", ev => {
            if (ev.target.value == "<select>") {
                displayUserPagination();
            }
        });
    }

    // fill the scenario select with all the available scenarios for the current user
    updateScenarioSelect();
    scenarioSelect.addEventListener("change", ev => {
        if (ev.target.value == "<select>") {
            displayScenarioPagination();
        }
    });

    search();
}

/**
 * Adds the newly selectes users from the pagination to the availableUsers variable (if they are not already in it)
 * and updates the html select
 */
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

/**
 * Adds the newly selected scenarios from the pagination to the availableScenarios variable (if they are not already in it)
 * and updates the html select
 */
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

/**
 * Displays the corresponding info boxes and graphics to the user based on the search filters
 * there is 4 cases: AllUsers/AllScenarios - AllUsers/OneScenario - OneUser/AllScenarios - OneUser/OneScenario
 */
function search() {
    const selectedUser = document.getElementById("user-select").value;
    const scenarioSelect = document.getElementById("scenario-select");
    const selectedScenario = scenarioSelect==null?"0":scenarioSelect.value;

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
            promise = Statistics.generateUserStatistics(charts, infoBoxes, User.currentUser.canTeacher()?selectedUser:User.currentUser.id);
        else // one scenario selected, get scenario informations
            promise = Statistics.generateUserScenarioStatistics(charts, infoBoxes, selectedScenario, User.currentUser.canTeacher()?selectedUser:User.currentUser.id);
    }

    let hasResults = false;
    if (promise != null)
        promise.then(() => {
            hasResults = true;
            window.indico.refreshStatistics();
        }).catch(err => {});

        // if not response is received for 8 seconds, display an error message
        setTimeout(() => {
            if (hasResults || charts.length > 0 || infoBoxes.length > 0) return;
            document.getElementById("loadzone").style.display = "none";
            document.getElementById("nodatazone").style.display = "none";
            document.getElementById("errorzone").style.display = "block";
        }, 8000);
}

if (!window.indico) window.indico = {};
window.indico.refreshStatistics = () => {
    if (dom != null) dom.$forceUpdate();
    if (charts.length == 0 && infoBoxes.length == 0)
        document.getElementById("nodatazone").style.display = "block";
    else document.getElementById("nodatazone").style.display = "none";
};

// callbacks used to show the pagination windows (overrided in the mounted() vue.js function)
let displayUserPagination;
let displayScenarioPagination;

export default {
    name: "Statistics",
    data: () => {
        return {charts, infoBoxes, user: User.currentUser, API, availableUsers, availableScenarios, User}
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