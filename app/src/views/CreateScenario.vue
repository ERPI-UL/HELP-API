<template>
    <div class="min-h-screen max-h-screen flex flex-col">
        <div class="p-2">
            <Topbar></Topbar>
        </div>
        <div id="navbar" class="flex grow-0 justify-between h-fit mx-2 p-1">
            <BackButton>Annuler</BackButton>
            <h2 class="text-2xl font-semibold text-gray-600 p-1">Créer un scénario</h2>
            <ValidateButton v-on:click="saveScenario">Enregistrer</ValidateButton>
        </div>
        <div id="content" class="flex flex-row grow min-h-0">
            <div class="flex flex-col grow-0 w-fit m-2">
                <div class="flex grow flex-col"> <!-- left panel (basic informations) -->
                    <div id="scenario-header" class="flex flex-col grow">
                        <h2 class="text-2xl text-indigo-600 font-extrabold mx-2 my-1 bg-white p-2 rounded-lg">Informations principales</h2>
                        <div class="flex flex-col m-2 h-fit bg-white rounded-lg p-2">
                            <div class="flex justify-between">
                                <p class="text-gray-500 font-base text-lg p-2 mr-4">Nom du scénario : </p>
                                <input type="text" id="input-scenarioname" name="scenario-name" value="" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                            </div>
                            <div class="flex flex-col grow-0">
                                <p class="text-gray-500 font-base text-lg p-2 mr-4">Description du scénario : </p>
                                <textarea id="input-scenariodesc" rows="10" style="resize: both;" class="md:size-to-parent px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100"></textarea>
                            </div>
                            <div class="flex justify-between mt-2 h-fit bg-white rounded-lg">
                                <p class="text-gray-500 font-base text-lg p-2 mr-4">Machine cible : </p>
                                <select name="machines" id="select-machines" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 pr-10 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                    <!-- available machines goes here, plus the <new> option -->
                                </select>
                            </div>
                        </div>
                    </div>
                    <div class="flex justify-between m-2 h-fit w-fit">
                        <p class="text-gray-500 font-base text-lg p-2 mr-8">Targets disponibles : </p>
                        <select name="machines" class="select-target md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 pr-10 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                            <!-- current machine's targets goes here  -->
                        </select>
                    </div>
                </div>
            </div>
            <div class="flex flex-col grow w-fit m-2"> <!-- right panel (steps customization) -->
                <h2 class="text-2xl text-indigo-600 font-extrabold mx-2 my-1 bg-white p-2 rounded-lg">Étapes</h2>
                <div class="flex flex-col m-2 grow overflow-auto border border-2 border-white rounded-lg p-4">
                    <div class="h-fit whitespace-nowrap inline-flex items-center justify-center px-4 py-2 w-fit rounded-md shadow-sm text-base border border-gray-200 font-medium text-gray-600 bg-white">
                        <component :is="icon.flag" class="flex-shrink-0 h-5 text-gray-600 mr-2" aria-hidden="true" />
                        <p>Début</p>
                    </div>
                    <span class="step-link"></span>
                    <div id="steps-zone">
                        <!-- step blocks goes here -->
                        <div class="step-part-container flex flex-col h-fit w-fit">
                            <h2 class="text-sm m-1 text-indigo-600 font-extrabold">Etape 1</h2>
                            <div class="flex flex-col grow p-1 rounded w-fit">
                                <div class="flex justify-between mb-1">
                                    <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">Identifiant de l'étape : </p>
                                    <input type="text" id="input-scenarioname" name="scenario-name" value="" class="h-fit md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                </div>
                                <div class="flex justify-between mb-1">
                                    <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">Titre de l'étape : </p>
                                    <input type="text" id="input-scenarioname" name="scenario-name" value="" class="h-fit md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                </div>
                                <div class="flex justify-between mb-1">
                                    <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">Description de l'étape : </p>
                                    <textarea id="input-scenariodesc" rows="2" style="resize: both;" class="md:size-to-parent px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100"></textarea>
                                </div>
                                <div class="flex justify-between mb-1">
                                    <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">Cibles de l'étape : </p>
                                    <div class="h-fit md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50">//TODO//</div>
                                </div>
                                <div class="justify-between mb-1">
                                    <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">Position du texte : </p>
                                    <div class="flex justify-between">
                                        <div id="shift" class="flex">
                                            <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">X: </p>
                                            <input type="number" name="pos-x" class="input-numbers whitespace-nowrap inline-flex max-w-[72px] text-center p-1 center border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                        </div>
                                        <div id="shift" class="flex">
                                            <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">Y: </p>
                                            <input type="number" name="pos-y" class="input-numbers whitespace-nowrap inline-flex max-w-[72px] text-center p-1 center border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                        </div>
                                        <div id="shift" class="flex">
                                            <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">Z: </p>
                                            <input type="number" name="pos-z" class="input-numbers whitespace-nowrap inline-flex max-w-[72px] text-center p-1 center border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <span class="step-link"></span>
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

import {
    FlagIcon,
    StopIcon,
    PlusCircleIcon
} from "@heroicons/vue/solid"

let availableMachines = [
    {
        name: "Machine 1",
        id: "machine1",
        targets: ["target-11", "target-21", "target-31"]
    },
    {
        name: "Machine 2",
        id: "machine2",
        targets: ["target-12", "target-22", "target-32"]
    }
];
let availableTargets = availableMachines[0].targets;

function updateAvailableTargets() {
    let selectTargets = document.querySelectorAll(".select-target");
    selectTargets.forEach(select => {
        select.innerHTML = "";
        availableTargets.forEach(target => {
            let option = document.createElement("option");
            option.value = target;
            option.innerHTML = target;
            select.appendChild(option);
        });
    })
}

function updateAvailableMachines() {
    let selectMachines = document.getElementById("select-machines");
    selectMachines.innerHTML = "";
    availableMachines.forEach(machine => {
        let option = document.createElement("option");
        option.value = machine.id;
        option.innerHTML = machine.name;
        selectMachines.appendChild(option);
    });
    let option = document.createElement("option");
    option.value = "<new>";
    option.innerHTML = "Nouvelle machine";
    selectMachines.appendChild(option);
}

function setup() {
    updateAvailableMachines();
    updateAvailableTargets();
    const machineSelect = document.getElementById("select-machines");
    machineSelect.addEventListener("change", function(ev) {
        switch (ev.target.value) {
            case "<new>":
                window.location.href = "/machines/create";
                break;
        
            default:
                availableTargets = availableMachines.find(machine => machine.id === ev.target.value).targets;
                updateAvailableTargets();
                break;
        }
    });
}

let steps = [];

function updateSteps() {
    const stepZone = document.getElementById("steps-zone");
    stepZone.innerHTML = "";
    steps.forEach(step => {
        let stepElement = document.createElement("div");
        stepElement.classList.add("step-part-container");
        stepZone.appendChild(stepElement);
        let stepLink = document.createElement("span");
        stepLink.classList.add("step-link");
        stepZone.appendChild(stepLink);
    });
}

function addStep() {
    steps.push({

    });
    updateSteps();
}

function saveScenario() {

}

export default {
    name: "CreateScenario",
    components: {
        Topbar,
        BackButton,
        ValidateButton
    },
    data() {return {icon: {flag: FlagIcon, stop: StopIcon, plus: PlusCircleIcon}};},
    mounted() {
        setup();
    },
    methods: {saveScenario, addStep}
};
</script>

<style>
.step-link {
    margin: 0.5em 1em;
    width: 0.2em;
    height: 2em;
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
}
</style>