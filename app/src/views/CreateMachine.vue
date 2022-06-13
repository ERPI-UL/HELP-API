<template>
    <div class="min-h-screen max-h-screen flex flex-col">
        <div class="p-2"> <!-- Header -->
            <Topbar></Topbar>
        </div>
        <div id="content" class="flex grow min-h-0">
            <div class="flex m-auto grow-0 w-fit m-2 mx-auto max-w-full">
                <div class="flex grow flex-col my-auto min-h-0 max-h-inherit md:max-h-full">
                    <div id="scenario-header" class="flex flex-col grow max-h-full min-h-0">
                        <h2 class="text-2xl text-indigo-600 font-extrabold mx-2 my-1 bg-white p-2 rounded-lg">{{ action }} une machine</h2>
                        <div class="flex md:flex-row flex-col p-2 min-h-0">
                            <!-- Machien's basic informations -->
                            <div class="flex flex-col h-full bg-white rounded-lg p-2 max-w-full space-y-2">
                                <div class="flex md:flex-row flex-col justify-between"> <!-- Machine name input (input label and input zone) -->
                                    <p class="text-gray-500 font-base text-lg p-2 mr-4">Nom de la machine : </p>
                                    <input type="text" id="input-machinename" name="scenario-name" value="" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                </div>
                                <div class="flex flex-col grow-0"> <!-- Machine description input (input label and input zone) -->
                                    <p class="text-gray-500 font-base text-lg p-2 mr-4">Description de la machine : </p>
                                    <textarea id="input-machinedesc" rows="5" style="resize: both;" class="md:size-to-parent px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100"></textarea>
                                </div>
                                <div class="flex justify-between grow-0"> <!-- Machine description input (input label and input zone) -->
                                    <p class="text-gray-500 font-base text-lg p-2 mr-4">Modèle 3D : </p>
                                    <input type="file" name="" id="model-input" accept=".glb">
                                    <label for="model-input">
                                        <p class="md:size-to-parent border whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100 cursor-pointer">Ajouter un modèle 3D</p>
                                    </label>
                                </div>
                            </div>
                            <!-- Machine's targets -->
                            <div class="flex grow flex-col md:mt-0 mt-2 md:ml-2 ml-0 bg-white rounded-lg p-2 min-h-0 max-h-screen space-y-2">
                                <div class="flex flex-row">
                                    <p class="text-gray-500 font-base text-lg p-2 mr-4">Cibles de la machine : </p>
                                    <p id="generate-btn" class="border whitespace-nowrap inline-flex px-4 py-2 border-gray-100 rounded-md text-base font-medium text-gray-500 bg-gray-50 cursor-default">
                                        Générer
                                    </p>
                                </div>
                                <div class="flex grow flex-col min-h-0">
                                    <div class="flex flex-col grow space-y-2 p-2 h-fit min-h-0 overflow-y-scroll overflow-x-hidden border border-gray-200 rounded">
                                        <div v-for="el in machineTargets"> <!-- For each target, display an input with the target's name in it -->
                                            <input 
                                                type="text" name="machine-target" :id="'machine-target-'+el.id" v-bind:value="el.name" v-on:change="setMachineTarget(el.id, $event.target.value);"
                                                v-on:focus="setSelectedTarget($event.target);" v-on:blur="setSelectedTarget(null);"
                                                class="whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100"
                                            >
                                        </div>
                                    </div>
                                    <!-- Target deletion / addition buttons -->
                                    <div class="flex justify-between space-x-1 pt-2">
                                        <button ref="delete-btn" v-on:click="removeMachineTarget();" class="bg-red-600 p-1 h-fit w-fit flex flex-row shadow rounded opacity-50 cursor-auto">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 m-auto text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M20 12H4" /> <!-- Remove button icon -->
                                            </svg>
                                            <p class="whitespace-nowrap text-white m-auto mx-1">Supprimer</p> <!-- Remove button label -->
                                        </button>
                                        <button v-on:click="addMachineTarget();" class="bg-indigo-600 p-1 h-fit w-fit flex flex-row shadow rounded">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 m-auto text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" /> <!-- Add button icon -->
                                            </svg>
                                            <p class="whitespace-nowrap text-white m-auto mx-1">Ajouter</p> <!-- Add button label -->
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <!-- Machine's main cancel / save button -->
                        <div class="flex flex-col bg-white rounded-lg p-2 m-2">
                            <div id="log-zone" class="border-none overflow-y-hidden h-[0px]"> <!-- Message log zone -->
                                <p class="opacity-0 text-center text-indigo-600"></p>
                            </div>
                            <div class="flex grow justify-between"> <!-- Buttons -->
                                <BackButton>Annuler</BackButton> <!-- Cancel button -->
                                <ValidateButton id="validate-button" v-on:click="saveMachine">{{action}}</ValidateButton> <!-- Save button -->
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

import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";

/**
 * Displays a message to the user (in the log-zone html element)
 * @param {string} msg - The message to display
 */
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

function setup() {
    const modelInput = document.getElementById("model-input");
    modelInput.addEventListener("change", function(e) {
        const file = e.target.files[0];
        const modelLabel = document.querySelector("label[for='model-input']");
        modelLabel.firstElementChild.innerHTML = file.name;
        modelLabel.firstElementChild.classList.remove("text-black", "bg-gray-50", "hover:bg-gray-100");
        modelLabel.firstElementChild.classList.add("text-white", "bg-indigo-600", "hover:bg-indigo-700");

        const generateBtn = document.getElementById("generate-btn");
        generateBtn.classList.remove("border-gray-100", "text-gray-500", "cursor-default");
        generateBtn.classList.add("border-gray-200", "text-black", "cursor-pointer", "hover:bg-gray-100", "shadow-sm");
        generateBtn.addEventListener("click", () => { generateTargets(file); });
    });
}

function generateTargets(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const data = e.target.result;
        const model = new Blob([data], {type: file.type});
        const loader = new GLTFLoader();
        loader.load(URL.createObjectURL(model), gltf => {
            gltf.scene.traverse(node => {
                if (node.isMesh) {
                    /**@type {string} */
                    const name = node.name.toLowerCase();
                    const conditions = [
                        !name.match(/^(plane|circle)[0-9]+(_[0-9]+)*$/)
                    ];
                    if (conditions.every(condition => condition)) {
                        // add the target (it's a valid name)
                        addMachineTarget({name: node.name});
                    }
                }
            })
        });
    };
    reader.readAsArrayBuffer(file);
}

/**
 * Machine class, represents a machine with it's attributes 
 */
class Machine {
    id = 0;
    name = "";
    description = "";
    /**@type {{name:string,id:number}[]} Machine targets*/
    targets = [];
    constructor(id, name, description, targets) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.targets = targets;
    }
}

/**
 * Updates the dom elements according to the machineTargets array, and sort the targets alphabetically
 */
function updateDom() {
    // sort the targets by name
    machineTargets = machineTargets.sort((a, b) => {
        if (a.name < b.name) return -1;
        if (a.name > b.name) return 1;
        return 0;
    });
    // update vue.js dom
    if (dom != null) dom.$forceUpdate();

    // if a new target is added, select it (it has no name so we use that to detect it)
    let elements = dom.$el.querySelectorAll("machine-target");
    if (elements) elements.forEach(el => {
        console.log("el: "+el.value);
        if (el.value == "") el.focus();
    });
}

/**@type {Machine} original machine retreived from API (used to detect changes for modification mode)*/
let originalMachine = null;

/**
 * Retreives the current edited machine's informations with an API call, and store it in the originalMachine variable 
 */
function retreiveMachineInfos() {
    if (action=="Modifier")
        API.execute_logged(API.ROUTE.MACHINES+queryParameters.idMachine, API.METHOD_GET, User.currentUser.getCredentials(), {}, API.TYPE_JSON).then(res => {
            document.getElementById('input-machinename').value = res.name;
            document.getElementById('input-machinedesc').value = res.description;
            machineTargets.splice(0, machineTargets.length);
            console.log(res.targets.map(t => t.id+" - "+t.name).join("\n"));
            res.targets.forEach(target => addMachineTarget(target))
            originalMachine = new Machine(res.id, res.name, res.description, res.targets);
        }).catch(err => {
            redirectHome();
            console.error(err);
        });
}

/**
 * Save the modifications made on the machine (for edit mode), makes API POST-PUT-DELETE calls according to the changes
 * @param {Machine} name - The current modified (or not) machine name
 * @param {Machine} description - The current modified (or not) machine description
 * @param {Machine} targets - The current modified (or not) machine targets list
 */
function saveModifications(name, description, targets) {
    if (name != originalMachine.name || description != originalMachine.description) {
        API.execute_logged(API.ROUTE.MACHINES+originalMachine.id, API.METHOD_PUT, User.currentUser.getCredentials(), {
            name: name,
            description: description
        }, API.TYPE_JSON).then(res => {
            // logMessage("Informations de la machine modifiées");
        }).catch(console.error);
    } // else logMessage("Aucune information machine à sauvegarder.")

    let targetsToDelete = [];
    let targetsToAdd = [];
    let targetsToModify = [];
    
    // for each target in the original machine, check if it's still in the edited machine
    // if not, it means that it has been deleted, else if the name isn't the same it has been modified
    originalMachine.targets.forEach(target => {
        let index = targets.findIndex(t => t.id == target.id);
        if (index < 0) targetsToDelete.push(target);
        else if (targets[index].name != target.name) targetsToModify.push(targets[index]);
    });
    // for each target in the edited machine, if it's not in the original machine it means it has been added
    targets.forEach(target => {
        let index = originalMachine.targets.findIndex(t => t.id == target.id);
        if (index < 0) targetsToAdd.push(target);
    });

    const setTaskDone = () => {
        logMessage("Modifications sauvegardées");
        redirectHome();
        // retreiveMachineInfos();
    };

    // When all the targets to delete have been deleted, we can move on to the targets modifications
    let deleteCounter = 0;
    const checkForDelete = () => {if (++deleteCounter >= targetsToDelete.length) modifyTargets();};

    // When all the targets to add have been added, we can notify the user and go back
    let addCounter = 0;
    const checkForAdd = () => {if (++addCounter >= targetsToAdd.length) setTaskDone();};

    // When all the targets to modify have been modified, we can move on to the targets additions
    let modifyCounter = 0;
    const checkForModify = () => {if (modifyCounter >= targetsToModify.length) addTargets();};

    // modifies all the required targets and execute checkForModify to continue to save the modifications after that
    const modifyTargets = () => {
        if (targetsToModify.length > 0) {
            targetsToModify.forEach(target => {
                API.execute_logged(API.ROUTE.MACHINES+API.ROUTE.__TARGETS+target.id, API.METHOD_PUT, User.currentUser.getCredentials(), {name: target.name}).then(res => {
                    // modified
                }).catch(console.error).finally(checkForModify);
            });
        } else checkForModify();
    }

    // adds all the required targets and execute checkForAdd to notify the user when it's all done
    const addTargets = () => {
        if (targetsToAdd.length > 0) {
            targetsToAdd.forEach(target => {
                API.execute_logged(API.ROUTE.MACHINES+originalMachine.id+API.ROUTE.__TARGETS, API.METHOD_POST, User.currentUser.getCredentials(), {name: target.name}).then(res => {
                    // added
                    let index = machineTargets.findIndex(t => t.name == res.name);
                    if (index >= 0) machineTargets[index].id = res.id;
                }).catch(console.error).finally(checkForAdd);
            })
        } else checkForAdd();
    }
    
    // delete all the required targets and execute checkForDelete to continue to save the modifications after that
    if (targetsToDelete.length > 0) {
        targetsToDelete.forEach(target => {
            API.execute_logged(API.ROUTE.MACHINES+API.ROUTE.__TARGETS+target.id, API.METHOD_DELETE, User.currentUser.getCredentials()).then(res => {
                // deleted
            }).catch(console.error).finally(checkForDelete);
        });
    } else checkForDelete();
}

/**
 * Save new created the machine (for create mode)
 * Retreives the informations from the dom elements and send them to the API
 */
function saveMachine() {
    const machineName = document.getElementById('input-machinename');
    const machineDesc = document.getElementById('input-machinedesc');
    const machineTargs = Array.from(machineTargets);

    // if no name has been provided, notify the user and return
    if (machineName.value.length < 1) {
        machineName.focus();
        logMessage("Veuillez préciser un nom de machine.")
        return;
    }
    // if no description has been provided, notify the user and return
    if (machineDesc.value.length < 1) {
        machineDesc.focus();
        logMessage("Veuillez préciser une description de machine.")
        return;
    }

    // if we detect the same target name twice in the targets list, notify the user and return
    for (let i = 0; i < machineTargs.length; i++) {
        const target = machineTargs[i];
        if (target.name < 1) {
            logMessage("Veuillez préciser un nom de cible.")
            return;
        }
        for (let j = i+1; j < machineTargs.length; j++) {
            const target2 = machineTargs[j];
            if (target2.name == target.name) {
                logMessage("Veuillez ne pas préciser deux fois la même cible.")
                return;
            }
        }
    }

    // set the button label to "..." to indicate that the request is being processed
    const button = document.getElementById("validate-button");
    button.innerHTML = "...";

    if (action == "Modifier") { // modification mode, should execute saveModifications instead of this function
        saveModifications(machineName.value, machineDesc.value, machineTargs);
        return;
    }

    // save the machine's basic informations first
    API.execute_logged(API.ROUTE.MACHINES, API.METHOD_POST, User.currentUser.getCredentials(), {
        name: machineName.value,
        description: machineDesc.value
    }).then(res => { // machine has been saved, add the targets to it

        let additionCounter = 0;
        /**
         * check if all targets have been added
         * and if so goes back home after displaying success message
         */
        const checkForAddition = () => {
            console.log("checking : "+additionCounter+" out of "+machineTargs.length);
            if (++additionCounter >= machineTargs.length) {
                logMessage("Machine créée");
                redirectHome();
            }
        }
        
        if (machineTargets.length > 0) { // if there is targets to add, add them one by one
            machineTargets.forEach(target => {
                API.execute_logged(API.ROUTE.MACHINES+res.id+API.ROUTE.__TARGETS, API.METHOD_POST, User.currentUser.getCredentials(), {name: target.name}).then(res => {
                    // target saved, apply the new given id to the targets in the list (to be able to delete them later for example)
                    let index = machineTargets.findIndex(t => t.name == res.name);
                    if (index >= 0) machineTargets[index].id = res.id;
                }).catch(console.error).finally(checkForAddition);
            });
        } else checkForAddition();

    }).catch(err => { // error, notify the user

        logMessage("Erreur lors de la création de la machine.");
        if (!err.json) console.error(err);
        else err.json().then(json => {
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

/**
 * Changes a target's name to [newText] locally
 * @param {number} id the id of the target to change
 * @param {string} newText the new name of the target
 */
function setMachineTarget(id, newText) {
    let index = machineTargets.findIndex(el => el.id == id);
    machineTargets[index].name = newText;
}

let IDCounter = 0;
/**
 * Adds a new target to the list of targets, if no target is provided, a new one is created
 * @param {{id:number,name:string}} target the target object to add (optional)
 */
function addMachineTarget(target=null) {
    let id = IDCounter++;
    let name = "";
    // if a target is provided, use it and modify the id counter to match the current provided ID
    if (target != null) {
        id = target.id ?? id;
        name = target.name;
        IDCounter = id+1;
    }

    machineTargets.push({
        name: name,
        id: id
    });
    updateDom();
}

/**
 * Sets the selected target to the provided one (for delete button)
 */
function setSelectedTarget(target) {
    if (target != null) {
        dom.$refs["delete-btn"].classList.remove("opacity-50", "cursor-auto");
        selectedTarget = target;
    }
    else setTimeout(() => {
        dom.$refs["delete-btn"].classList.add("opacity-50", "cursor-auto");
        selectedTarget = null;
    }, 100);
}

let selectedTarget = null;
/**
 * Removes a target from the list at the given index
 * if no index is provided, it will check if selectedTarget is set and remove this one
 * else, it will remove the target at the list's end
 */
function removeMachineTarget(index) {
    if (!index) { // if no index is provided
        if (selectedTarget != null) {// check if there is a selected target
            let value = selectedTarget.value;
            index = machineTargets.findIndex(el => el.name == value); // if so, find the index of this target
        }
    }
    if (index != undefined) {
        machineTargets.splice(index, 1); // remove the target from the lists
        dom.$refs["delete-btn"].classList.add("opacity-50", "cursor-auto");
    }
    updateDom();
}

let dom = null; // parent dom element of this template
let machineTargets = []; // current machine targets
let urlPath = window.location.pathname.split('/'); // current url path
let queryParameters = {};

// if the url says the page is accessed for edition, set the action to "Modifier"
const action = urlPath[urlPath.length-1] == "edit"? "Modifier": "Créer";

// retreive the query parameters (do get the machine's id from the url)
let parts = window.location.href.split("?");
if (parts[1]) {
    parts[1].split("&").forEach(part => {
        let item = part.split("=");
        queryParameters[item[0]] = decodeURIComponent(item[1]);
    });
}

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
        setup();
        dom = this;
        retreiveMachineInfos();
    },
    methods: {saveMachine, addMachineTarget, removeMachineTarget, setMachineTarget, setSelectedTarget}
};
</script>

<style>
#model-input {
	width: 0.1px;
	height: 0.1px;
	opacity: 0;
	overflow: hidden;
	position: absolute;
	z-index: -1;
}
</style>