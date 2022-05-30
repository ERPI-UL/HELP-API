<template>
    <div class="min-h-screen max-h-screen flex flex-col">
        <div class="p-2">
            <Topbar></Topbar>
        </div>
        <div id="content" class="flex flex-row grow min-h-0">
            <div class="flex flex-col grow-0 w-fit m-2">
                <div class="flex grow flex-col"> <!-- left panel (basic informations) -->
                    <div id="scenario-header" class="flex flex-col grow">
                        <h2 class="text-2xl text-indigo-600 font-extrabold mx-2 my-1 bg-white p-2 rounded-lg">Informations principales</h2>
                        <div class="flex flex-col m-2 h-fit bg-white rounded-lg p-2">
                            <div class="flex justify-between">
                                <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">Nom du scénario : </p>
                                <input type="text" id="input-scenarioname" name="scenario-name" value="" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                            </div>
                            <div class="flex flex-col grow-0">
                                <p class="text-gray-500 font-base text-lg p-2 mr-4">Description du scénario : </p>
                                <textarea id="input-scenariodesc" name="scenario-desc" rows="10" style="resize: both;" class="md:size-to-parent px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100"></textarea>
                            </div>
                            <div class="flex justify-between mt-2 h-fit bg-white rounded-lg">
                                <p class="text-gray-500 font-base text-lg p-2 mr-4">Machine cible : </p>
                                <select name="machines" id="select-machines" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 pr-10 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                    <!-- available machines goes here, plus the <select> option -->
                                    <option value="<select>">Sélectionner ...</option>
                                </select>
                                <PaginationChoice
                                    ref="machinePagination" :title="'Sélection machines'"
                                    :selectID="'#select-machines'" :callback="addMachineSelection" :route="API.ROUTE.MACHINES"
                                    :displayAttribute="el => el.name" :identifier="el => el.id" :selectedValues="availableMachines.map(el => el.id)">
                                </PaginationChoice>
                            </div>
                        </div>
                        <div id="navbar" class="flex flex-col justify-between h-fit mx-2 rounded-lg bg-white p-2">
                            <div id="log-zone" class="border-none overflow-y-hidden h-[0px]">
                                <p class="opacity-0 text-center text-indigo-600"></p>
                            </div>
                            <div class="flex grow-0 justify-between">
                                <BackButton>Annuler</BackButton>
                                <ValidateButton id="save-btn" v-on:click="saveScenario">Enregistrer</ValidateButton>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="flex flex-col grow w-fit m-2 min-w-0"> <!-- right panel (steps customization) -->
                <h2 class="text-2xl text-indigo-600 font-extrabold mx-2 my-1 bg-white p-2 rounded-lg">Étapes</h2>
                <div class="flex flex-col m-2 grow overflow-auto border border-2 border-white rounded-lg p-4">
                    <div class="whitespace-nowrap inline-flex items-center justify-center px-4 py-2 rounded-md shadow-sm text-base border border-gray-200 font-medium text-gray-600 bg-white w-fit">
                        <component :is="icon.flag" class="flex-shrink-0 h-5 text-gray-600 mr-2" aria-hidden="true" />
                        <p>Début</p>
                    </div>
                    <span class="step-link"></span>
                    <div id="steps-zone">
                        <!-- step blocks goes here -->
                    </div>
                    <ValidateButton v-on:click="addStep">
                        <component :is="icon.plus" class="flex-shrink-0 h-5 text-white mr-2" aria-hidden="true" />
                        <p>Ajouter une étape</p>
                    </ValidateButton>
                    <span class="step-link"></span>
                    <div class="h-fit whitespace-nowrap inline-flex items-center justify-center px-4 py-2 w-fit rounded-md shadow-sm text-base border border-gray-200 font-medium text-gray-600 bg-white">
                        <component :is="icon.stop" class="flex-shrink-0 h-5 text-gray-600 mr-2" aria-hidden="true" />
                        <p>Fin</p>
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
import PaginationChoice from "../components/PaginationChoice.vue";
import API from '../script/API';
import {
    FlagIcon,
    StopIcon,
    PlusCircleIcon
} from "@heroicons/vue/solid"
import User from '../script/User';
import { redirectHome } from '../script/common';

class BlockInfo {
    id = 0;
    ordernumber = 0;
    name = "";
    label = "";
    type = {name: "action"}
    choice = null
    description = "";
    /**@type {{name:string,id:number}[]} */
    targets = [];
    position = {x: 0, y: 0, z: 0};

    constructor(id, ordernumber, name, label, description, targets, position, type, btnInfos) {
        this.id = id;
        this.ordernumber = ordernumber;
        this.name = name;
        this.label = label;
        this.description = description;
        this.targets = targets;
        this.position = position;
        this.type = {name: type};
        this.choice = type != "choice"? null: btnInfos;
    }
}

function logMessage(msg) {
    const btn = document.getElementById("save-btn");
    btn.innerHTML = "Enregistrer";
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

let availableMachines = [];
let availableTargets = [];

function updateAvailableTargets() {
    let selectTargets = document.querySelectorAll("select[name=select-targets]");
    selectTargets.forEach(select => {
        const defaultValue = select.value;
        let alwayshere = false;
        select.innerHTML = "";
        select.value = "";
        availableTargets.forEach(target => {
            let option = document.createElement("option");
            option.value = target.id;
            if (option.value == defaultValue)
                alwayshere = true;
            option.innerHTML = target.name;
            select.appendChild(option);
        });
        if (alwayshere) {
            select.value = defaultValue;
        }
    })
}

function updateAvailableMachines(selectValue) {
    let selectMachines = document.getElementById("select-machines");
    selectMachines.innerHTML = "";
    if (availableMachines.length == 0) {
        let option1 = document.createElement("option");
        option1.value = "";
        option1.innerHTML = "-- -- -- -- --";
        selectMachines.appendChild(option1);
    }
    availableMachines.forEach(machine => {
        let option = document.createElement("option");
        option.value = machine.id;
        option.innerHTML = machine.name;
        selectMachines.appendChild(option);
    });
    let option2 = document.createElement("option");
    option2.value = "<select>";
    option2.innerHTML = "Sélectionner ...";
    selectMachines.appendChild(option2);

    setTimeout(() => {
        if (selectValue != undefined)
            selectMachines.value = selectValue;
    }, 10);
}

let availableRedirects = [];
function updateAvailableRedirects() {
    availableRedirects = Array.from(document.querySelectorAll(".step-part-container")).map(step => {
        return {
            id: parseInt(step.id.split("-")[1]),
            name: step.querySelector("input[name='scenario-name']").value
        }
    });
    document.querySelectorAll(".redirect-btn").forEach(select => {
        let defaultValue = select.value;
        select.innerHTML = "";
        availableRedirects.forEach(step => {
            let option = document.createElement("option");
            option.value = step.id;
            option.innerHTML = step.name;
            if (option.value === defaultValue || option.innerHTML === defaultValue) {
                option.selected = true;
            }
            select.appendChild(option);
        });
    });
}

function onMachineChanged() {
    let val = document.getElementById("select-machines").value;
    switch (val) {
        case "<select>":
            displayMachineSelection();
            break;
    
        default:
            availableTargets = [];
            const curMachine = availableMachines.find(machine => {
                return machine.id == val;
            });
            if (!curMachine) return;
            availableTargets = curMachine.targets;
            updateAvailableTargets();
            break;
    }
}

let originalScenario = null;
function fetchScenario() {
    return new Promise((resolve, reject) => {
        const url = window.location.pathname.split("/");
        if (url[url.length-1] == "create") { // create mode, don't fetch anything
            resolve();
            return;
        }
        // else fetch the scenario's informations and build the blocks
        let queryParameters = {};
        let parts = window.location.href.split("?");
        if (parts[1])
            parts[1].split("&").forEach(part => {
                let item = part.split("=");
                queryParameters[item[0]] = decodeURIComponent(item[1]);
            });
        API.execute(API.ROUTE.SCENARIOS+queryParameters["idScenario"], API.METHOD_GET, undefined, API.TYPE_JSON).then(res => {
            originalScenario = res;
            document.querySelector("input[name=scenario-name]").value = res.name;
            document.querySelector("textarea[name=scenario-desc]").value = res.description;
            API.execute(API.ROUTE.MACHINES+res.machine.id, API.METHOD_GET, undefined, API.TYPE_JSON).then(machine => {
                availableMachines = [{
                    name: machine.name,
                    id: machine.id,
                    targets: machine.targets
                }];
                updateAvailableMachines();
                onMachineChanged();
                document.getElementById("select-machines").value = res.machine.id;
                res.steps.forEach(step => {
                    createScenarioBlock(step.name, step.label, step.description, step.targets, step.position, step.type, step.type!="choice"?undefined: step.choice, step.id);
                });
                resolve();
            }).catch(reject);
        }).catch(reject);
    });
}

function setup() {
        fetchScenario().then(res => {
        updateAvailableMachines();
        updateAvailableTargets();
        const machineSelect = document.getElementById("select-machines");
        machineSelect.addEventListener("change", onMachineChanged);
    }).catch(console.error);
}

function addStep() {
    createScenarioBlock();
}

function blockInfoFromDom(dom) {
    return new BlockInfo(
        parseInt(dom.querySelector("h2").id.split("-")[1]),
        parseInt(dom.querySelector("h2").innerHTML.split(" ")[1]),
        dom.querySelector("input[name=scenario-name]").value,
        dom.querySelector("input[name=scenario-title]").value,
        dom.querySelector("textarea[name=scenario-desc]").value,
        Array.from(dom.querySelectorAll("select[name=select-targets]")).map(select => parseInt(select.value)),
        {
            x: parseFloat(dom.querySelector("input[name=pos-x]").value),
            y: parseFloat(dom.querySelector("input[name=pos-y]").value),
            z: parseFloat(dom.querySelector("input[name=pos-z]").value)
        },
        dom.querySelector("select[name='step-mode']").value,
        {
            option_left: {
                label: dom.querySelector("input[name='btn-left-label']")?.value,
                redirect: dom.querySelector("select[name='btn-left-redirect']")?.value
            },
            option_right: {
                label: dom.querySelector("input[name='btn-right-label']")?.value,
                redirect: dom.querySelector("select[name='btn-right-redirect']")?.value
            }
        }
    );
}

function compileScenario() {
    const informations = {
        name: document.querySelector("input[name=scenario-name]"),
        description: document.querySelector("textarea[name=scenario-desc]"),
        machine: document.getElementById("select-machines")
    };

    const checks = [
        {msg: "Veuillez renseigner un nom", el: informations.name, cond: el => el.value.length > 0},
        {msg: "Veuillez renseigner une description", el: informations.description, cond: el => el.value.length > 0},
        {msg: "Veuillez sélectionner une machine", el: informations.machine, cond: el => el.value.length > 0},
        {msg: "Évitez de préciser la machine dans le nom", el: informations.name, cond: el => !el.value.includes(availableMachines.find(m => m.id == informations.machine.value).name)},
    ];
    
    for (let i = 0; i < checks.length; i++) {
        const check = checks[i];
        if (!check.cond(check.el)) {
            check.el.focus();
            logMessage(check.msg);
            return;
        }
    }

    let scenario = {
        id: originalScenario?.id,
        name: informations.name.value,
        description: informations.description.value,
        machine: {
            name: "",
            id: parseInt(informations.machine.value)
        },
        steps: scenarioBlocks.map(block => blockInfoFromDom(block.dom))
    };
    return scenario;
}

function saveCreations() {
    const button = document.getElementById("save-btn");
    const scenario = compileScenario();

    button.innerHTML = "...";
    API.execute_logged(API.ROUTE.SCENARIOS, API.METHOD_POST, User.currentUser.getCredentials(), scenario, API.TYPE_JSON).then(res => {
        button.innerHTML = "Enregistré !";
        redirectHome();
    }).catch(err => err.json().then(console.error));
}

function stepEquals(a, b) {
    const conditions = [
        a.name == b.name,
        a.label == b.label,
        a.description == b.description,
        a.targets.length == b.targets.length,
        a.targets.every(target => b.targets.findIndex(t => t.id == target) >= 0),
        a.position.x == b.position.x,
        a.position.y == b.position.y,
        a.position.z == b.position.z,
        a.type.name == b.type,
        a.choice?.option_left.label     == b.choice?.option_left.label,
        a.choice?.option_left.redirect  == b.choice?.option_left.redirect,
        a.choice?.option_right.label    == b.choice?.option_right.label,
        a.choice?.option_right.redirect == b.choice?.option_right.redirect
    ];
    return conditions.every(c => c);
}

function saveModifications() {
    logMessage("Erreur: Modification de scénario non supportée");
    const scenario = compileScenario();
    if (scenario.name != originalScenario.name || scenario.description != originalScenario.description) {
        API.execute_logged(API.ROUTE.MACHINES, API.METHOD_PUT, User.currentUser.getCredentials(), {name: scenario.name, description: scenario.description}, API.TYPE_JSON).then(res => {
            // basic infos modified
        }).catch(err => console.log(err));
    }
    
    let addedSteps = [];
    let modifiedSteps = [];
    let removedSteps = [];
    scenario.steps.forEach(step => {
        let index = originalScenario.steps.findIndex(el => {
            return el.id === step.id;
        });
        if (index < 0) addedSteps.push(step);
        else if (!stepEquals(step, originalScenario.steps[index]))
            modifiedSteps.push(step);
    });
    originalScenario.steps.forEach(step => {
        let index = scenario.steps.findIndex(el => {
            return el.id === step.id;
        });
        if (index < 0) removedSteps.push(step);
    });

    let deleteCounter = 0;
    let modifyCounter = 0;
    let addCounter = 0;
    const checkForDelete = () => {
        if (deleteCounter++ >= removedSteps.length) {
            if (modifiedSteps.length > 0) {
                modifiedSteps.forEach(step => {
                    API.execute_logged(API.ROUTE.STEPS + step.id, API.METHOD_PUT, User.currentUser.getCredentials(), step, API.TYPE_JSON).then(res => {
                        // modified
                    }).catch(err => console.log(err)).finally(checkForModify);
                });
            } else checkForModify();
        }
    };
    const checkForModify = () => {
        if (modifyCounter++ >= removedSteps.length) {
            if (addedSteps.length > 0) {
                addedSteps.forEach(step => {
                    API.execute_logged(API.ROUTE.SCENARIOS+scenario.id+API.ROUTE.__STEPS, API.METHOD_POST, User.currentUser.getCredentials(), step, API.TYPE_JSON).then(res => {
                        // added
                    }).catch(err => console.log(err)).finally(checkForAddition);
                })
            } else checkForAddition();
        }
    }
    const checkForAddition = () => {
        if (addCounter++ >= addedSteps) {
            logMessage("Modifications sauvegardés.");
            // redirectHome();
        }
    }
    if (removedSteps.length > 0) {
        removedSteps.forEach(step => {
            API.execute_logged(API.ROUTE.STEPS + step.id, API.METHOD_DELETE, User.currentUser.getCredentials(), undefined, API.TYPE_JSON).then(res => {
                // removed
            }).catch(err => console.log(err)).finally(checkForDelete);
        });
    } else checkForDelete();
}

function saveScenario() {
    const url = window.location.pathname.split("/");
    if (url[url.length-1] == "edit")
        saveModifications();
    else saveCreations();
}

let displayMachineSelection = () => {};

function addMachineSelection(content) {
    availableMachines = availableMachines.filter(el => el.id in content.map(el => el.id));
    let nbAdded = 0; let lastMachineID = 0;
    content.forEach(el => {
        let inside = false;
        availableMachines.forEach(e => {if (e.id == el.id) inside = true;});
        if (!inside) {
            nbAdded++;
            lastMachineID = el.id;
            const targets = [];
            availableMachines.push({
                name: el.name,
                id: el.id,
                targets: targets
            });
            API.execute(API.ROUTE.MACHINES+el.id, API.METHOD_GET, undefined, API.TYPE_JSON).then(res => {
                res.targets.forEach(t => targets.push({
                    id: t.id,
                    name: t.name
                }));
                updateAvailableTargets();
            }).catch(console.error);
        }
    });
    updateAvailableMachines((nbAdded==1)? lastMachineID : undefined);
    updateAvailableTargets();
    onMachineChanged();
}

function getBlockDiv(id, name, title, desc, targets, pos, mode="action", btnInfos={option_left: {label: "Bouton gauche", redirect: ""}, option_right: {label: "Bouton droit", redirect: ""}}) {
    let tgs = "";
    // if (targets)
    //     targets.forEach(target => {
    //         tgs += `<select name="select-targets" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 pr-10 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100" value="${target.id}">${target.name}</select>`
    //     });
    const container = document.createElement("div");
    container.classList.add("step-part-container", "flex", "flex-col", "h-fit", "w-fit", "max-w-[80%]");
    container.id = "stepcontainer-" + id;
    container.innerHTML = 
    `<div class="flex justify-between m-1">
        <h2 id="stepname-${id}" class="text-sm m-1 text-indigo-600 font-extrabold">Étape ${scenarioBlocks.length+1}</h2>
        <button onclick="window.indico.removeScenarioBlock(${id});" id="steprem-${id}" class="bg-red-600 p-1 h-fit w-fit flex flex-row shadow rounded">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 m-auto text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
        </button>
    </div>
    <div class="flex flex-col grow p-1 rounded w-fit min-w-0 min-h-0 max-w-full">
        <div class="flex justify-between mb-1 min-w-0 min-h-0">
            <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">Identifiant de l'étape : </p>
            <input type="text" id="input-stepid-${id}" name="scenario-name" value="${name??""}" class="h-fit md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black min-w-0 min-h-0 bg-gray-50 hover:bg-gray-100">
        </div>
        <div class="flex justify-between mb-1 min-w-0 min-h-0">
            <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">Titre de l'étape : </p>
            <input type="text" id="input-stepname-${id}" name="scenario-title" value="${title??""}" class="h-fit md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black min-w-0 min-h-0 bg-gray-50 hover:bg-gray-100">
        </div>
        <div class="flex justify-between mb-1 min-w-0 min-h-0">
            <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">Description de l'étape : </p>
            <textarea id="input-stepdesc-${id}" name="scenario-desc" rows="2" cols="30" style="resize: both;" class="md:size-to-parent px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100 min-w-0 min-h-0">${desc??""}</textarea>
        </div>
        <div class="flex justify-between mb-1 min-w-0 min-h-0">
            <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">Cibles de l'étape : </p>
            <div id="steptargets-${id}" class="md:size-to-parent flex grow min-w-0 min-h-0 px-2 py-2 space-x-2 border border-gray-200 rounded-md text-base font-medium text-black">
                <div class="flex flex-col justify-left space-y-1">
                    <button onclick="window.indico.addStepTarget(${id});" id="steptargetsadd-${id}" class="bg-indigo-600 p-1 h-fit flex justify-left shadow rounded">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 m-auto text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
                        </svg>
                        <p class="whitespace-nowrap text-white m-auto">Ajouter</p>
                    </button>
                    <button onclick="window.indico.removeStepTarget(${id});" id="steptargetsrem-${id}" class="bg-red-600 p-1 h-fit flex justify-left shadow rounded">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 m-auto text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M20 12H4" />
                        </svg>
                        <p class="whitespace-nowrap text-white center m-auto">Supprimer</p>
                    </button>
                </div>
                <div id="steptargetscontainer-${id}" class="flex space-x-2 h-fit m-auto overflow-y-hidden overflow-x-scroll min-w-0 min-h-0">
                    ${tgs}
                </div>
            </div>
        </div>
        <div class="flex justify-between mb-1 min-w-0 min-h-0">
            <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">Type d'étape : </p>
            <select name="step-mode" value="${mode??"action"}" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 pr-10 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                <option value="action">Action</option>
                <option value="info">Information</option>
                <option value="choice">Choix</option>
            </select>
        </div>
        <div id="btn-config-zone" class="flex flex-col justify-between mb-1 ml-2 p-1 bg-gray-50 border border-gray-100 rounded-md min-w-0 min-h-0" style="display: none;">
            <h2 id="stepname-${id}" class="text-sm m-1 text-gray-500 font-extrabold">Configuration des boutons</h2>
            <div style="border-bottom: solid 2px #F3F4F6;">
                <div class="flex justify-between mb-1 min-w-0 min-h-0">
                    <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">Texte du bouton gauche : </p>
                    <input type="text" name="btn-left-label" value="${btnInfos?.option_left?.label??""}" class="h-fit md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black min-w-0 min-h-0 bg-gray-50 hover:bg-gray-100">
                </div>
                <div class="flex justify-between mb-1 min-w-0 min-h-0">
                    <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">Étape cible du bouton gauche : </p>
                    <select name="btn-left-redirect" value="${btnInfos?.option_left?.redirect??""}" class="redirect-btn h-fit md:size-to-parent whitespace-nowrap inline-flex px-4 pr-8 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black min-w-0 min-h-0 bg-gray-50 hover:bg-gray-100">

                    </select>
                </div>
            </div>
            <div>
                <div class="flex justify-between mt-1 mb-1 min-w-0 min-h-0">
                    <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">Texte du bouton droit : </p>
                    <input type="text" name="btn-right-label" value="${btnInfos?.option_right?.label??""}" class="h-fit md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black min-w-0 min-h-0 bg-gray-50 hover:bg-gray-100">
                </div>
                <div class="flex justify-between min-w-0 min-h-0">
                    <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">Étape cible du bouton droit : </p>
                    <select name="btn-right-redirect" value="${btnInfos?.option_right?.redirect??""}" class="redirect-btn h-fit md:size-to-parent whitespace-nowrap inline-flex px-4 pr-8 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black min-w-0 min-h-0 bg-gray-50 hover:bg-gray-100">

                    </select>
                </div>
            </div>
        </div>
        <div class="justify-between mb-1">
            <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">Position du texte : </p>
            <div class="flex justify-between">
                <div id="shift" class="flex">
                    <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">X: </p>
                    <input type="number" name="pos-x" id="input-stepposx-${id}" value="${pos!=undefined?pos.x:"0"}" class="input-numbers whitespace-nowrap inline-flex max-w-[72px] text-center p-1 center border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                </div>
                <div id="shift" class="flex">
                    <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">Y: </p>
                    <input type="number" name="pos-y" id="input-stepposy-${id}" value="${pos!=undefined?pos.y:"0"}" class="input-numbers whitespace-nowrap inline-flex max-w-[72px] text-center p-1 center border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                </div>
                <div id="shift" class="flex">
                    <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">Z: </p>
                    <input type="number" name="pos-z" id="input-stepposz-${id}" value="${pos!=undefined?pos.z:"0"}" class="input-numbers whitespace-nowrap inline-flex max-w-[72px] text-center p-1 center border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                </div>
            </div>
        </div>
    </div>`;
    return container;
}

let ID_COUNTER = 1;
let scenarioBlocks = [];
function createScenarioBlock(name, title, desc, targets, pos, mode, btnInfos, id) {
    if (id) ID_COUNTER = id;
    const newID = ID_COUNTER++;
    const stepZone = document.getElementById("steps-zone");
    const newBlock = getBlockDiv(newID, name, title, desc, targets, pos, mode, btnInfos);
    stepZone.appendChild(newBlock);
    stepZone.appendChild(document.createElement("span")).classList.add("step-link");
    
    if (scenarioBlocks.length > 0)
        scenarioBlocks[scenarioBlocks.length-1].next = newID;
    scenarioBlocks.push({
        dom: newBlock,
        id: newID,
        next: 0,
        previous: (scenarioBlocks.length > 0)? scenarioBlocks[scenarioBlocks.length-1].id: 0
    });

    setTimeout(() => {
        const selects = [];
        if (targets) targets.forEach(target => {selects.push({el: window.indico.addStepTarget(newID, target.id, target.name), id: target.id});});
        updateAvailableTargets();
        selects.forEach(select => {select.el.value = select.id});
        
        newBlock.querySelector("input[name='scenario-name']").addEventListener("change", ev => {
            let index = availableRedirects.findIndex(step => step.id == newID);
            if (index >= 0) availableRedirects[index].name = ev.target.value;
            updateAvailableRedirects();
        });

        let stepMode = newBlock.querySelector("select[name='step-mode']");
        stepMode.stepDiv = newBlock;
        const onModeChange = ev => {
            let btnConfigZone = ev.target.stepDiv.querySelector("#btn-config-zone");
            switch (ev.target.value) {
                case "choice": btnConfigZone.style.display = "block"; break;
                default: btnConfigZone.style.display = "none"; break;
            }
        };
        stepMode.addEventListener("change", onModeChange);
        if (mode && stepMode.value != mode) {
            stepMode.value = mode;
            onModeChange({target: stepMode});
        }
        updateAvailableRedirects();
        if (mode == "choice") {
            const leftRedirect = availableRedirects.find(step => step.name === btnInfos.option_left.redirect);
            const rightRedirect = availableRedirects.find(step => step.name === btnInfos.option_right.redirect);
            if (leftRedirect) newBlock.querySelector("select[name='btn-left-redirect']").value = leftRedirect.id+"";
            if (rightRedirect) newBlock.querySelector("select[name='btn-right-redirect']").value = rightRedirect.id+"";
        }
    }, 10);
}

function removeScenarioBlock(id) {
    const blockIndex = scenarioBlocks.findIndex(el => el.id == id);
    const block = scenarioBlocks[blockIndex];
    if (!block) return;
    const dom = block.dom;
    dom.nextElementSibling.remove();
    dom.remove();
    let current = block;
    if (current.next == 0 && scenarioBlocks.length > 1) {
        const prev = scenarioBlocks.find(el => el.next == id);
        if (prev) prev.next = 0;
    }
    while (current.next != 0) {
        let currentIndex = scenarioBlocks.findIndex(el => el.id == current.next);
        if (currentIndex < 0) {
            current.next = 0;
            break;
        } else {
            current = scenarioBlocks[currentIndex];
            document.getElementById("stepname-"+current.id).innerHTML = "Étape "+(currentIndex);
        }
    }
    scenarioBlocks.splice(blockIndex, 1);
}

function addStepTarget(stepID, value, label) {
    const select = document.createElement("select");
    select.name = "select-targets";
    select.classList.add("md:size-to-parent", "whitespace-nowrap", "inline-flex", "px-4", "py-2", "pr-10", "border-gray-200", "rounded-md", "shadow-sm", "text-base", "font-medium", "text-black", "bg-gray-50", "hover:bg-gray-100");
    if (value) select.value = value;
    if (label) select.innerHTML = label;
    document.getElementById("steptargetscontainer-"+stepID).appendChild(select);
    if (!value || !label) updateAvailableTargets();
    return select;
}

function removeStepTarget(stepID) {
    document.getElementById("steptargetscontainer-"+stepID).lastElementChild?.remove();
    updateAvailableTargets();
}

if (window.indico == undefined) window.indico = {};
window.indico.removeStepTarget = removeStepTarget;
window.indico.addStepTarget = addStepTarget;
window.indico.removeScenarioBlock = removeScenarioBlock;

window.displayJSON = function(str) {
    console.log(JSON.stringify(JSON.parse(str.replaceAll("\\", "")), null, 2));
}

export default {
    name: "CreateScenario",
    components: {
        Topbar,
        BackButton,
        ValidateButton,
        PaginationChoice
    },
    data() {return {icon: {flag: FlagIcon, stop: StopIcon, plus: PlusCircleIcon}, API, availableMachines};},
    mounted() {
        setup();
        displayMachineSelection = () => {
            this.$refs["machinePagination"].show();
        }
    },
    methods: {saveScenario, addStep, addMachineSelection}
};
</script>

<style>
@keyframes spawn-in {
    0% {
        opacity: 0;
        transform: translateY(10px);
    }
    100% {
        opacity: 1;
        transform: translateY(0px);
    }
}

.step-link {
    margin: 0.5em 1em;
    width: 0.2em;
    height: 2em;
    min-height: 2em;
    max-height: 2em;
    border-radius: 1em;
    background-color: #4B5563;
    display: block;
}

.step-part-container {
    margin: 0.5em 0;
    width: 10em;
    height: 5em;
    border-radius: 0.5em;
    background-color: white;
    box-shadow: 0px 4px 8px #0001;
    animation: spawn-in 200ms ease;
}
</style>