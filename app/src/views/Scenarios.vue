<template>
    <!-- Scenario list web page -->
    <div class="min-h-screen flex flex-col">
        <div class="p-2"> <!-- Header -->
            <Topbar></Topbar>
        </div>
        <div class="block md:flex grow">
            <div class="m-2 grow-0">
                <!-- Left panel containing the different scenario view modes -->
                <div class="bg-white rounded min-w-[12vw] divide-y grow">
                    <h2 class="text-2xl leading-9 font-extrabold text-indigo-600 px-6 py-2 whitespace-nowrap">{{ User.LANGUAGE.DATA.PAGES.SCENARIOS }}</h2>
                    <div class="md:pt-8 flex md:flex-col md:overflow-x-visible overflow-x-scroll justify-between">
                        <!-- All scenarios -->
                        <a class="whitespace-nowrap md:min-w-full md:p-4 md:m-4 p-2 m-2 rounded-lg text-base font-semibold text-left text-indigo-800 outline-none hover:border-indigo-300" 
                            :class="(window.location.href.split('#')[1] == 'all')?'bg-indigo-600 text-indigo-50 shadow-lg shadow-indigo-600': ''"
                            href="#all">
                            {{ User.LANGUAGE.DATA.SCENARIOS.PAGES.VIEW.TITLE }}
                        </a>
                        <!-- Pending scenarios (only if connected) -->
                        <a v-if="User.currentUser.canLearner()" class="whitespace-nowrap md:min-w-full md:p-4 md:m-4 p-2 m-2 rounded-lg text-base font-semibold text-left text-indigo-800 outline-none hover:border-indigo-300"
                            :class="(window.location.href.split('#')[1] == 'pending')?'bg-indigo-600 text-indigo-50 shadow-lg shadow-indigo-600': ''"
                            href="#pending">
                            {{ User.LANGUAGE.DATA.SCENARIOS.PAGES.OWN.TITLE }}
                        </a>
                        <!-- Edit scenario (only if teacher or admin) -->
                        <a v-if="User.currentUser.canTeacher()" class="whitespace-nowrap md:min-w-full md:p-4 md:m-4 p-2 m-2 rounded-lg text-base font-semibold text-left text-indigo-800 outline-none hover:border-indigo-300"
                            :class="(window.location.href.split('#')[1] == 'editing')?'bg-indigo-600 text-indigo-50 shadow-lg shadow-indigo-600': ''"
                            href="#editing">
                            {{ User.LANGUAGE.DATA.SCENARIOS.PAGES.EDIT.TITLE }}
                        </a>
                    </div>
                </div>
            </div>
            <!-- Page content -->
            <div class="flex flex-col grow m-2">
                <!-- Top bar with filters for the scenarios (for example the machine used for the scenario) -->
                <div class="bg-white shadow-lg p-2 rounded-lg w-full h-fit flex md:flex-row flex-col grow-0">
                    <div class="flex md:justify-left justify-between">
                        <h2 class="m-1 p-1">{{ User.LANGUAGE.DATA.PAGES.MACHINES }}: </h2>
                        <select id="machines-select" class="min-w-0 border-none rounded bg-indigo-50 p-1 m-1 pr-8">
                            <option value="<loading>">{{ User.LANGUAGE.DATA.ACTIONS.LOADING }} ...</option>
                        </select>
                        <!-- Paginatioon modal for the machines -->
                        <PaginationChoice 
                            ref="machinePagination" :title="User.LANGUAGE.DATA.PAGINATION.MACHINE_SELECTION"
                            :selectID="'#machines-select'" :callback="addMachineSelection" :route="API.ROUTE.MACHINES"
                            :displayAttribute="el => el.name" :identifier="el => el.id" :selectedValues="availableMachines.map(el => el.id)">
                        </PaginationChoice>
                    </div>
                    <!-- Search button -->
                    <div class="flex grow justify-between">
                        <span></span>
                        <ValidateButton v-on:click="search">{{ User.LANGUAGE.DATA.ACTIONS.SEARCH }}</ValidateButton>
                    </div>
                </div>
                <!-- SCenarios list content -->
                <div class="flex flex-col grow m-2 overflow-x-hidden overflow-y-scroll">
                    <!-- create new scenario button (only visible in edit mode) -->
                    <div v-if="window.location.href.split('#')[1] == 'editing'" class="m-4 w-fit h-fit">
                        <RedirectButton href="/scenarios/create">
                            <component :is="icon.plus" class="flex-shrink-0 h-5 text-white mr-2" aria-hidden="true" />
                            {{ User.LANGUAGE.DATA.SCENARIOS.ACTIONS.NEW }}
                        </RedirectButton>
                    </div>
                    <!-- Scenarios list -->
                    <div class="m-2 flex grow flex-wrap justify-evenly">
                        <!-- Scenarios in #all mode -->
                        <Scenario v-if="window.location.href.split('#')[1] == 'all'" v-for="item in scenarios.all">
                            <template v-slot:title>{{item.title}}</template>
                            <template v-slot:machine>{{item.machine}}</template>
                            <template v-slot:description>{{item.description}}</template>
                            <template v-slot:href><RedirectButton :href="item.view">{{ User.LANGUAGE.DATA.ACTIONS.VIEW }}</RedirectButton></template>
                        </Scenario>
                        <!-- Scenarios in #edit mode -->
                        <Scenario v-if="window.location.href.split('#')[1] == 'editing'" v-for="item in scenarios.editing">
                            <template v-slot:title>{{item.title}}</template>
                            <template v-slot:machine>{{item.machine}}</template>
                            <template v-slot:description>{{item.description}}</template>
                            <template v-slot:href><RedirectButton :href="item.edit" v-if="item.id != 6">{{ User.LANGUAGE.DATA.ACTIONS.EDIT }}</RedirectButton></template>
                            <template v-slot:remove><DangerousButton v-on:click="removeScenario(item.id, $event.target)" v-if="item.id != 6">{{ User.LANGUAGE.DATA.ACTIONS.REMOVE }}</DangerousButton></template>
                        </Scenario>
                        <!-- Scenarios in #pending mode -->
                        <Scenario v-if="window.location.href.split('#')[1] == 'pending'" v-for="item in scenarios.pending">
                            <template v-slot:title>{{item.title}}</template>
                            <template v-slot:machine>{{item.machine}}</template>
                            <template v-slot:description>{{item.description}}</template>
                        </Scenario>
                        <!-- Delete validation popup called when deleting a scenario in edit mode -->
                        <ValidatePopup ref="delete-popup"></ValidatePopup>
                    </div>
                    <!-- Scenario list bottom buttons -->
                    <div class="m-2 flex grow flex-wrap justify-evenly">
                        <!-- More button for all scenarios -->
                        <OutlineButton
                            v-if="(window.location.href.split('#')[1] == 'all' || window.location.href.split('#')[1] == 'editing') && obj.displayMoreAllButton"
                            v-on:click="loadNextAllScenarios();">
                            {{ User.LANGUAGE.DATA.ACTIONS.MORE }}
                        </OutlineButton>
                        <!-- More button for own scenarios (pending) -->
                        <OutlineButton
                            v-if="window.location.href.split('#')[1] == 'pending' && obj.displayMoreAllButton"
                            v-on:click="loadNextOwnScenarios();">
                            {{ User.LANGUAGE.DATA.ACTIONS.MORE }}
                        </OutlineButton>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Topbar from "../components/Topbar.vue";
import Scenario from "../components/Scenario.vue";
import RedirectButton from "../components/RedirectButton.vue";
import OutlineButton from "../components/OutlineButton.vue";
import DangerousButton from "../components/DangerousButton.vue";
import ValidatePopup from "../components/ValidatePopup.vue";
import ValidateButton from "../components/ValidateButton.vue";
import User from "../script/User";
import API from '../script/API';
import PaginationChoice from "../components/PaginationChoice.vue";
import {
    PlusIcon
} from "@heroicons/vue/solid";

let dom = null;
let Alliterator = null;
let Owniterator = null;
let obj = {
    displayMoreAllButton: false,
    displayMoreOwnButton: false
};

// more scenarios ballback (all), redefined in attachAllListener function
let loadNextAllScenarios = () => {return Alliterator != null && Alliterator.isNext();}
// more scenarios ballback (own), redefined in attachOwnListener function
let loadNextOwnScenarios = () => {return Owniterator != null && Owniterator.isNext();}

/**
 * Attaches listeners to the new generated iterator for all scenarios
 * and changes the laodNextAllScenarios function for the new iterator
 */
function attachAllListeners(it) {
    it.promise.then(res => {
        const data = res.data.map(el => {return {
            id: el.id,
            title: el.name,
            description: el.description,
            machine: el.machine.name,
            edit: "/scenarios/edit?idScenario="+el.id,
            view: "/scenarios/view?idScenario="+el.id
        }});
        scenarios.all = scenarios.all.concat(data);
        scenarios.editing = scenarios.editing.concat(data);
        obj.displayMoreAllButton = Alliterator.isNext();
        if (dom != null) dom.$forceUpdate();
    }).catch(err => {
        console.error(err);
        obj.displayMoreAllButton = false;
        if (dom != null) dom.$forceUpdate();
    });
    loadNextAllScenarios = () => {
        iterator = it.next();
        if (iterator != null) {
            attachAllListeners(iterator);
            return iterator.isNext();
        } else return false;
    };
}

/**
 * Attaches listeners to the new generated iterator for own scenarios
 * and changes the laodNextOwnScenarios function for the new iterator
 */
function attachOwnListeners(it) {
    it.promise.then(res => {
        scenarios.pending.concat(res.map(el => {
            return {
                title: el.name,
                description: el.description,
                machine: el.machine?.name
            }
        }));
        obj.displayMoreOwnButton = Owniterator.isNext();
        if (dom != null) dom.$forceUpdate();
    }).catch(err => {
        if (err.json) err.json().then(console.error);
        else console.error(err);
        obj.displayMoreOwnButton = false;
        if (dom != null) dom.$forceUpdate();
    });
    loadNextOwnScenarios = () => {
        iterator = it.next();
        if (iterator != null) {
            attachOwnListeners(iterator);
            return iterator.isNext();
        } else return false;
    };
}

/**
 * Generates the iterator for all scenarios and resets the scenario list
 */
function fetchAllScenarios(idMachine) {
    scenarios.all = [];
    scenarios.editing = [];
    Alliterator = API.iterate( API.ROUTE.SCENARIOS+(idMachine==null?"": API.createParameters({idMachine: idMachine})) );
    attachAllListeners(Alliterator);
}

/**
 * Generates the iterator for own scenarios and resets the scenario list
 */
function fetchOwnScenarios(idMachine) {
    scenarios.pending = [];
    Owniterator = API.iterate( API.ROUTE.USERS+User.currentUser.id+API.ROUTE.__SCENARIOS+(idMachine==null?"": API.createParameters({idMachine: idMachine})), 1, 10, true);
    attachOwnListeners(Owniterator);
}

/**
 * Removes a scenario from the database with an API call.
 * Spawns a validation popup to confirm the deletion.
 */
function removeScenario(id, caller) {
    const el = this.$refs["delete-popup"];
    el.show(User.LANGUAGE.DATA.SCENARIOS.ACTIONS.REMOVE.TITLE, User.LANGUAGE.DATA.SCENARIOS.ACTIONS.REMOVE.DESCRIPTION, User.LANGUAGE.DATA.ACTIONS.CANCEL, User.LANGUAGE.DATA.ACTIONS.REMOVE);
    el.setPosition(caller);
    el.setCallback(() => {
        API.execute_logged(API.ROUTE.SCENARIOS+id, API.METHOD_DELETE, User.currentUser.getCredentials(), {}, API.TYPE_JSON).then(res => {
            let dom = caller;
            while (dom.id != "scenario-parent") dom = dom.parentElement;
            dom.remove();
        }).catch(console.error);
    });
}

// current displayed scenarios
const scenarios = {
    all: [
        
    ],
    pending: [
        
    ],
    editing: [
        
    ]
}

// current available machines in the machine html select
let availableMachines = [];
/**
 * Updates the options in the machine html select with the new machines in the availableMachines variable
 */
function updateMachinesSelect(selectValue) {
    const userSelect = document.getElementById("machines-select");
    let val = userSelect.value;
    userSelect.innerHTML = "";
    const userOptions = [{value: "<all>", text: User.LANGUAGE.DATA.COMMON.WORDS.ALL}];
    availableMachines.forEach(machine => userOptions.push(machine));
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
 * Adds the content to the availableMachines array (if they are not already in it)
 * and updates the machines html selects
 */
function addMachineSelection(content) {
    availableMachines = availableMachines.filter(el => el.id in content.map(el => el.id));
    let nbAdded = 0, lastSelectedID = 0;
    content.forEach(el => {
        if (!(el.id in availableMachines.map(el => el.id))) {
            nbAdded++;
            lastSelectedID = el.id;
            availableMachines.push({value: el.id, text: el.name});
        }
    });
    updateMachinesSelect((nbAdded==1)? lastSelectedID: undefined);
}

/**
 * Searches for scenarios with the given machine filters
 */
function search() {
    const machineID = parseInt(document.getElementById("machines-select").value);
    fetchAllScenarios(isNaN(machineID)? null: machineID);
    fetchOwnScenarios(isNaN(machineID)? null: machineID);
}

export default {
    name: "Scenarios",
    components: {
        Topbar,
        Scenario,
        RedirectButton,
        OutlineButton,
        DangerousButton,
        ValidatePopup,
        ValidateButton,
        PaginationChoice
    },
    setup() {
        if (window.location.href.split("#").length < 2) window.location.href += "#all";
        return {window, scenarios, User, icon: {plus: PlusIcon}, obj, API, availableMachines}
    },
    mounted() {
        dom = this;
        fetchAllScenarios();
        fetchOwnScenarios();

        updateMachinesSelect();
        document.getElementById("machines-select").addEventListener("change", ev => {
            if (ev.target.value == "<select>") {
                this.$refs["machinePagination"].show();
            }
        });
    },
    methods: {loadNextAllScenarios, loadNextOwnScenarios, removeScenario, addMachineSelection, search}
};
</script>