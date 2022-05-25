<template>
    <div class="min-h-screen max-h-screen flex flex-col">
        <div class="p-2">
            <Topbar></Topbar>
        </div>
        <div id="content" class="flex grow min-h-0">
            <div class="flex m-auto grow-0 w-fit m-2 mx-auto max-w-full">
                <div class="flex grow flex-col my-auto min-h-0 max-h-inherit md:max-h-full"> <!-- left panel (basic informations) -->
                    <div id="scenario-header" class="flex flex-col grow max-h-full min-h-0">
                        <h2 class="text-2xl text-indigo-600 font-extrabold mx-2 my-1 bg-white p-2 rounded-lg">{{ action }} une machine</h2>
                        <div class="flex md:flex-row flex-col p-2 min-h-0">
                            <div class="flex flex-col h-full bg-white rounded-lg p-2 max-w-full">
                                <div class="flex md:flex-row flex-col justify-between">
                                    <p class="text-gray-500 font-base text-lg p-2 mr-4">Nom de la machine : </p>
                                    <input type="text" id="input-machinename" name="scenario-name" value="" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                </div>
                                <div class="flex flex-col grow-0">
                                    <p class="text-gray-500 font-base text-lg p-2 mr-4">Description de la machine : </p>
                                    <textarea id="input-machinedesc" rows="5" style="resize: both;" class="md:size-to-parent px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100"></textarea>
                                </div>
                            </div>
                            <div class="flex grow flex-col md:mt-0 mt-2 md:ml-2 ml-0 bg-white rounded-lg p-2 min-h-0 max-h-screen">
                                <p class="text-gray-500 font-base text-lg p-2 mr-4">Cibles de la machine : </p>
                                <div class="flex grow flex-col min-h-0">
                                    <div class="flex flex-col grow space-y-2 p-2 h-fit min-h-0 overflow-y-scroll overflow-x-hidden border border-gray-200 rounded">
                                        <div v-for="el in machineTargets">
                                            <input 
                                                type="text" name="machine-target" v-bind:value="el.data" v-on:change="setMachineTarget(el.id, $event.target.value);"
                                                v-on:focus="setSelectedTarget($event.target);"
                                                class="whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100"
                                            >
                                        </div>
                                    </div>
                                    <div class="flex justify-between space-x-1 pt-2">
                                        <button v-on:click="removeMachineTarget();" class="bg-red-600 p-1 h-fit w-fit flex flex-row shadow rounded">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 m-auto text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M20 12H4" />
                                            </svg>
                                            <p class="whitespace-nowrap text-white m-auto mx-1">Supprimer</p>
                                        </button>
                                        <button v-on:click="addMachineTarget();" class="bg-indigo-600 p-1 h-fit w-fit flex flex-row shadow rounded">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 m-auto text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
                                            </svg>
                                            <p class="whitespace-nowrap text-white m-auto mx-1">Ajouter</p>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="flex flex-col bg-white rounded-lg p-2 m-2">
                            <div id="log-zone" class="border-none overflow-y-hidden h-[0px]">
                                <p class="opacity-0 text-center text-indigo-600"></p>
                            </div>
                            <div class="flex grow justify-between">
                                <BackButton>Annuler</BackButton>
                                <ValidateButton id="validate-button" v-on:click="saveMachine">{{action}}</ValidateButton>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Topbar from "../components/Topbar.vue";
import BackButton from "../components/BackButton.vue";
import ValidateButton from "../components/ValidateButton.vue";
import API from '../script/API';
import User from '../script/User';
import { redirectHome } from '../script/common';

function logMessage(msg) {
    const btn = document.getElementById("validate-button");
    btn.innerHTML = action;
    const div = document.getElementById("log-zone");
    const txt = div.firstElementChild;
    if (txt.innerHTML.length < 1)
        txt.innerHTML = msg;
    else txt.innerHTML += "<br>"+msg;
    txt.classList.add("opacity-100");
    div.style.height = txt.getBoundingClientRect().height+"px";
    setTimeout(() => {
        txt.classList.remove("opacity-100");
        let liste = txt.innerHTML.split("<br>");
        liste.pop();
        txt.innerHTML = liste.join("<br>");
        div.style.height = "0px";
    }, 3000);
}

class Machine {
    id = 0;
    name = "";
    description = "";
    targets = [];
    constructor(id, name, description, targets) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.targets = targets;
    }
}

function updateDom() {
    // sort the targets by name
    machineTargets = machineTargets.sort((a, b) => {
        if (a.data < b.data) return -1;
        if (a.data > b.data) return 1;
        return 0;
    });
    // update vue.js dom
    if (dom != null) dom.$forceUpdate();
}

let originalMachine = null;
function retreiveMachineInfos() {
    if (action=="Modifier")
        API.execute_logged(API.ROUTE.MACHINES+queryParameters.idMachine, API.METHOD_GET, User.currentUser.getCredentials(), {}, API.TYPE_JSON).then(res => {
            document.getElementById('input-machinename').value = res.name;
            document.getElementById('input-machinedesc').value = res.description;
            machineTargets.splice(0, machineTargets.length);
            res.targets.forEach(target => addMachineTarget(target))
            originalMachine = new Machine(res.id, res.name, res.description, res.targets);
        }).catch(err => {
            redirectHome();
            console.error(err);
        });
}

function saveModifications(name, description, targets) {
    if (name != originalMachine.name || description != originalMachine.description) {
        API.execute_logged(API.ROUTE.MACHINES+originalMachine.id, API.METHOD_PUT, User.currentUser.getCredentials(), {
            name: name,
            description: description
        }, API.TYPE_JSON).then(res => {
            //logMessage("Informations de la machine modifiées");
        }).catch(console.error);
    } // else logMessage("Aucune information machine à sauvegarder.")

    let _toRemove = [];
    let targetsToDelete = Array.from(originalMachine.targets);
    targets.forEach(target => {
        let index = targetsToDelete.findIndex(t => t.id == target.id);
        if (index >= 0) _toRemove.push(index);
    });
    for(let i = _toRemove.length-1; i >= 0; i--) targetsToDelete.splice(_toRemove[i], 1);

    _toRemove = [];
    let targetsToAdd = Array.from(targets);
    originalMachine.targets.forEach(target => {
        let index = targetsToAdd.findIndex(t => t.name == target.data && t.id == target.id);
        if (index >= 0) _toRemove.push(index);
    });
    for(let i = _toRemove.length-1; i >= 0; i--) targetsToAdd.splice(_toRemove[i], 1);

    _toRemove = [];
    let targetsToModify = Array.from(originalMachine.targets);
    targetsToModify.forEach(target => {
        let index = targets.findIndex(t => t.data != target.name && t.id == target.id);
        if (index < 0) _toRemove.push(targetsToModify.findIndex(t => t.id == target.id));
        else targetsToModify[index].name = targets[index].data;
    });
    for(let i = _toRemove.length-1; i >= 0; i--) targetsToModify.splice(_toRemove[i], 1);

    let taskDone = [false, false, false];
    const setTaskDone = (nbr) => {taskDone[nbr] = true; if (!taskDone[0] || !taskDone[1] || !taskDone[2]) return; logMessage("Modifications sauvegardées"); retreiveMachineInfos();};
    let deleteCounter = 0;
    const checkForDelete = () => {deleteCounter++; if (deleteCounter < targetsToDelete.length) return; setTaskDone(0)};
    let addCounter = 0;
    const checkForAdd = () => {addCounter++; if (addCounter < targetsToAdd.length) return; setTaskDone(1)};
    let modifyCounter = 0;
    const checkForModify = () => {modifyCounter++; if (modifyCounter < targetsToModify.length) return; setTaskDone(2)};

    targetsToDelete.forEach(target => {
        API.execute_logged(API.ROUTE.MACHINES+API.ROUTE.__TARGETS+target.id, API.METHOD_DELETE, User.currentUser.getCredentials()).then(res => {
            checkForDelete();
            console.log("Target "+target.id+" ("+target.name+") supprimée");
        }).catch(console.error);
    });
    targetsToModify.forEach(target => {
        API.execute_logged(API.ROUTE.MACHINES+API.ROUTE.__TARGETS+target.id, API.METHOD_PUT, User.currentUser.getCredentials(), {name: target.name}).then(res => {
            checkForModify();
            console.log("Target "+target.id+" ("+target.name+") modifiée");
        }).catch(console.error);
    });
    if (targetsToAdd.length > 0)
        API.execute_logged(API.ROUTE.MACHINES+originalMachine.id+API.ROUTE.__TARGETS, API.METHOD_POST, User.currentUser.getCredentials(), targetsToAdd.map(t => t.data)).then(res => {
            checkForAdd();
            res.forEach(target => {
                let index = machineTargets.findIndex(t => t.data == target.name);
                if (index >= 0) machineTargets[index].id = target.id;
            });
            updateDom();
            console.log("Targets ("+targetsToAdd.map(t => t.data)+")  ajoutés");
        }).catch(console.error);

    if (targetsToAdd.length == 0) checkForAdd();
    if (targetsToDelete.length == 0) checkForDelete();
    if (targetsToModify.length == 0) checkForModify();
}

function saveMachine() {
    const machineName = document.getElementById('input-machinename');
    const machineDesc = document.getElementById('input-machinedesc');
    const machineTargs = Array.from(machineTargets);

    if (machineName.value.length < 1) {
        machineName.focus();
        logMessage("Veuillez préciser un nom de machine.")
        return;
    }
    if (machineDesc.value.length < 1) {
        machineDesc.focus();
        logMessage("Veuillez préciser une description de machine.")
        return;
    }

    for (let i = 0; i < machineTargs.length; i++) {
        const target = machineTargs[i];
        if (target.data < 1) {
            logMessage("Veuillez préciser un nom de cible.")
            return;
        }
        for (let j = i+1; j < machineTargs.length; j++) {
            const target2 = machineTargs[j];
            if (target2.data == target.data) {
                logMessage("Veuillez ne pas préciser deux fois la même cible.")
                return;
            }
        }
    }

    const button = document.getElementById("validate-button");
    button.innerHTML = "...";
    if (action == "Modifier") {
        // logMessage("Erreur: Modification de machine non implémentée.");
        saveModifications(machineName.value, machineDesc.value, machineTargs);
        return;
    }
    API.execute_logged(API.ROUTE.MACHINES, API.METHOD_POST, User.currentUser.getCredentials(), {
        name: machineName.value,
        description: machineDesc.value
    }).then(res => {
        API.execute_logged(API.ROUTE.MACHINES+res.id+API.ROUTE.__TARGETS, API.METHOD_POST, User.currentUser.getCredentials(), machineTargets.map(el =>el.data), API.TYPE_JSON).then(res => {
            logMessage("Machine créée avec succès !");
            button.innerHTML = action;
            redirectHome();
        }).catch(err => {
            logMessage("Erreur lors de la création des cibles de la machine.");
            console.error(err);
        });
    }).catch(err => {
        logMessage("Erreur lors de la création de la machine.");
        console.error(err);
        err.json().then(json => {
            console.error(json)
            switch (json.detail[0].type) {
                case "IntegrityError":
                    machineName.focus();
                    logMessage("Le nom ["+document.getElementById('input-machinename').value+"] existe déjà.");
                    break;
                default: break;
            }
        });
    });
}

function setMachineTarget(id, newText) {
    let index = machineTargets.findIndex(el => el.id == id);
    machineTargets[index].data = newText;
}

let IDCounter = 0;
function addMachineTarget(target=null) {
    let id = IDCounter++;
    let data = "";
    if (target != null) {
        id = target.id;
        data = target.name;
        IDCounter = id+1;
    }

    machineTargets.push({
        data: data,
        id: id
    });
    updateDom();
}

function setSelectedTarget(target) {
    selectedTarget = target;
}

let selectedTarget = null;
function removeMachineTarget(index) {
    if (!index) {
        index = machineTargets.length-1;
        if (selectedTarget != null)
            index = machineTargets.findIndex(el => el.data == selectedTarget.value);
    }
    machineTargets.splice(index, 1);
    updateDom();
}

let dom = null;
let machineTargets = [];
let urlPath = window.location.pathname.split('/');
let queryParameters = {};
const action = urlPath[urlPath.length-1] == "edit"? "Modifier": "Créer";
let parts = window.location.href.split("?");
if (parts[1])
    parts[1].split("&").forEach(part => {
        let item = part.split("=");
        queryParameters[item[0]] = decodeURIComponent(item[1]);
    });

export default {
    name: "CreateScenario",
    components: {
        Topbar,
        BackButton,
        ValidateButton
    },
    data() {return {action, machineTargets};},
    setup() {
        
    },
    mounted() {
        dom = this;
        retreiveMachineInfos();
    },
    methods: {saveMachine, addMachineTarget, removeMachineTarget, setMachineTarget, setSelectedTarget}
};
</script>

<style>
</style>