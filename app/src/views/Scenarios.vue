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
                        <a v-if="user.canTeacher()" class="whitespace-nowrap md:min-w-full md:p-4 md:m-4 p-2 m-2 rounded-lg text-base font-semibold text-left text-indigo-800 outline-none hover:border-indigo-300"
                            :class="(window.location.href.split('#')[1] == 'editing')?'bg-indigo-600 text-indigo-50 shadow-lg shadow-indigo-600': ''"
                            href="#editing">
                            Créer / Modifier
                        </a>
                    </div>
                </div>
            </div>
            <div class="flex flex-col grow m-2">
                <div class="bg-white shadow-lg p-2 rounded-lg w-full h-fit flex md:flex-row flex-col grow-0">
                    <div class="flex md:justify-left justify-between">
                        <h2 class="m-1 p-1">Machines: </h2>
                        <select id="machines-select" class="min-w-0 border-none rounded bg-indigo-50 p-1 m-1 pr-8">
                            <option value="<loading>">Chargement ...</option>
                        </select>
                        <PaginationChoice
                            ref="machinePagination" :title="'Sélection machines'"
                            :selectID="'#machines-select'" :callback="addMachineSelection" :route="API.ROUTE.MACHINES"
                            :displayAttribute="el => el.name" :identifier="el => el.id" :selectedValues="availableMachines.map(el => el.id)">
                        </PaginationChoice>
                    </div>
                    <div class="flex grow justify-between">
                        <span></span>
                        <ValidateButton v-on:click="search">Chercher</ValidateButton>
                    </div>
                </div>
                <div class="flex flex-col grow m-2 overflow-x-hidden overflow-y-scroll">
                    <div v-if="window.location.href.split('#')[1] == 'editing'" class="m-4 w-fit h-fit">
                        <RedirectButton href="/scenarios/create">
                            <component :is="icon.plus" class="flex-shrink-0 h-5 text-white mr-2" aria-hidden="true" />
                            Nouveau scénario
                        </RedirectButton>
                    </div>
                    <div class="m-2 flex grow flex-wrap justify-evenly"> <!-- Scenario -->
                        <Scenario v-if="window.location.href.split('#')[1] == 'all'" v-for="item in scenarios.all">
                            <template v-slot:title>{{item.title}}</template>
                            <template v-slot:machine>{{item.machine}}</template>
                            <template v-slot:description>{{item.description}}</template>
                        </Scenario>
                        <Scenario v-if="window.location.href.split('#')[1] == 'editing'" v-for="item in scenarios.editing">
                            <template v-slot:title>{{item.title}}</template>
                            <template v-slot:machine>{{item.machine}}</template>
                            <template v-slot:description>{{item.description}}</template>
                            <template v-slot:href><RedirectButton :href="item.href">Editer</RedirectButton></template>
                            <template v-slot:remove><DangerousButton v-on:click="removeScenario(item.id, $event.target)" v-if="item.id != 6">Supprimer</DangerousButton></template>
                        </Scenario>
                        <Scenario v-if="window.location.href.split('#')[1] == 'pending'" v-for="item in scenarios.pending">
                            <template v-slot:title>{{item.title}}</template>
                            <template v-slot:machine>{{item.machine}}</template>
                            <template v-slot:description>{{item.description}}</template>
                        </Scenario>
                        <ValidatePopup ref="delete-popup"></ValidatePopup>
                    </div>
                    <div class="m-2 flex grow flex-wrap justify-evenly">
                        <OutlineButton
                            v-if="(window.location.href.split('#')[1] == 'all' || window.location.href.split('#')[1] == 'editing') && obj.displayMoreAllButton"
                            v-on:click="loadNextAllScenarios();">
                            Voir plus
                        </OutlineButton>
                        <OutlineButton
                            v-if="window.location.href.split('#')[1] == 'pending' && obj.displayMoreAllButton"
                            v-on:click="loadNextOwnScenarios();">
                            Voir plus
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

let loadNextAllScenarios = () => {return Alliterator != null && Alliterator.isNext();}
let loadNextOwnScenarios = () => {return Owniterator != null && Owniterator.isNext();}

function attachAllListeners(it) {
    it.promise.then(res => {
        const data = res.data.map(el => {return {
            id: el.id??"ID inconnu",
            title: el.name??"Titre inconnu",
            description: el.description??"Description inconnue",
            machine: el.machine.name??"Machine inconnue",
            href: "/scenarios/edit?idScenario="+el.id
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

function attachOwnListeners(it) {
    it.promise.then(res => {
        scenarios.pending.concat(res.map(el => {
            return {
                title: el.name??"Titre inconnu",
                description: el.description??"Description inconnue",
                machine: el.machine != null? el.machine.name: "Machine inconnue"
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

function fetchAllScenarios(idMachine) {
    scenarios.all = [];
    scenarios.editing = [];
    Alliterator = API.iterate( API.ROUTE.SCENARIOS+(idMachine==null?"": API.createParameters({idMachine: idMachine})) );
    attachAllListeners(Alliterator);
}

function fetchOwnScenarios(idMachine) {
    scenarios.pending = [];
    Owniterator = API.iterate( API.ROUTE.USERS+User.currentUser.id+API.ROUTE.__SCENARIOS+(idMachine==null?"": API.createParameters({idMachine: idMachine})), 1, 10, true);
    attachOwnListeners(Owniterator);
}

function removeScenario(id, caller) {
    const el = this.$refs["delete-popup"];
    el.show("Supprimer un scénario", "Voulez-vous supprimer "+(scenarios.editing.find(el => el.id == id).title)+" ?", "Annuler", "Supprimer");
    el.setPosition(caller);
    el.setCallback(() => {
        API.execute_logged(API.ROUTE.SCENARIOS+id, API.METHOD_DELETE, User.currentUser.getCredentials(), {}, API.TYPE_JSON).then(res => {
            let dom = caller;
            while (dom.id != "scenario-parent") dom = dom.parentElement;
            dom.remove();
        }).catch(console.error);
    });
}

const scenarios = {
    all: [
        
    ],
    pending: [
        
    ],
    editing: [
        
    ]
}

let availableMachines = [];
function updateMachinesSelect(selectValue) {
    const userSelect = document.getElementById("machines-select");
    let val = userSelect.value;
    userSelect.innerHTML = "";
    const userOptions = [{value: "<all>", text: "Toutes"}];
    availableMachines.forEach(machine => userOptions.push(machine));
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
        return {window, scenarios, user: User.currentUser, icon: {plus: PlusIcon}, obj, API, availableMachines}
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