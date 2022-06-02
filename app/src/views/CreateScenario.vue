<template>
    <div class="min-h-screen max-h-screen flex flex-col">
        <div class="p-2"> <!-- Header -->
            <Topbar></Topbar>
        </div>
        <div id="content" class="flex flex-row grow min-h-0">
            <div class="flex flex-col grow-0 w-fit m-2">
                <div class="flex grow flex-col"> <!-- left panel (basic informations) -->
                    <div id="scenario-header" class="flex flex-col grow">
                        <h2 class="text-2xl text-indigo-600 font-extrabold mx-2 my-1 bg-white p-2 rounded-lg">Informations principales</h2>
                        <div class="flex flex-col m-2 h-fit bg-white rounded-lg p-2">
                            <div class="flex justify-between"> <!-- Scenario name input (input label and input zone) -->
                                <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">Nom du scénario : </p>
                                <input type="text" id="input-scenarioname" name="scenario-name" value="" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                            </div>
                            <div class="flex flex-col grow-0"> <!-- Scenario description input (input label and input zone) -->
                                <p class="text-gray-500 font-base text-lg p-2 mr-4">Description du scénario : </p>
                                <textarea id="input-scenariodesc" name="scenario-desc" rows="10" style="resize: both;" class="md:size-to-parent px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100"></textarea>
                            </div>
                            <div class="flex justify-between mt-2 h-fit bg-white rounded-lg"> <!-- Machine selection zone -->
                                <p class="text-gray-500 font-base text-lg p-2 mr-4">Machine cible : </p>
                                <select name="machines" id="select-machines" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 pr-10 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                    <!-- available machines goes here, plus the <select> option -->
                                    <option value="<select>">Sélectionner ...</option>
                                </select>
                                <!-- Machine pagination popup -->
                                <PaginationChoice 
                                    ref="machinePagination" :title="'Sélection machines'"
                                    :selectID="'#select-machines'" :callback="addMachineSelection" :route="API.ROUTE.MACHINES"
                                    :displayAttribute="el => el.name" :identifier="el => el.id" :selectedValues="availableMachines.map(el => el.id)">
                                </PaginationChoice>
                            </div>
                        </div>

                        <div id="navbar" class="flex flex-col justify-between h-fit mx-2 rounded-lg bg-white p-2">
                            <div id="log-zone" class="border-none overflow-y-hidden h-[0px]"> <!-- log message zone -->
                                <p class="opacity-0 text-center text-indigo-600"></p>
                            </div>
                            <!-- BUTTONS -->
                            <div class="flex grow-0 justify-between">
                                <BackButton>Annuler</BackButton> <!-- Cancel button -->
                                <ValidateButton id="save-btn" v-on:click="saveScenario">Enregistrer</ValidateButton> <!-- Save button -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="flex flex-col grow w-fit m-2 min-w-0"> <!-- right panel (steps customization) -->
                <div id="tabs" class="flex grow-0 justify-between">
                    <h2 v-on:click="mode=MODE_STEPS; updateMode(MODE_STEPS);" :class="mode==MODE_STEPS? 'shadow-lg': 'bg-indigo-50 text-indigo-300'" class="flex grow justify-start text-2xl text-indigo-600 font-extrabold mx-2 my-1 bg-white py-2 px-4 rounded-lg cursor-pointer select-none">Étapes</h2>
                    <h2 v-on:click="mode=MODE_MODEL; updateMode(MODE_MODEL);" :class="mode==MODE_MODEL? 'shadow-lg': 'bg-indigo-50 text-indigo-300'" class="flex grow justify-end text-2xl text-indigo-600 font-extrabold mx-2 my-1 bg-white py-2 px-4 rounded-lg cursor-pointer select-none">Modèle</h2>
                </div>
                <!-- steps zone -->
                <div :class="mode==MODE_STEPS? '': 'hidden'" class="flex flex-col m-2 grow overflow-auto border border-2 border-white rounded-lg p-4">
                    <!-- START FLAG ELEMENT -->
                    <div class="whitespace-nowrap inline-flex items-center justify-center px-4 py-2 rounded-md shadow-sm text-base border border-gray-200 font-medium text-gray-600 bg-white w-fit">
                        <component :is="icon.flag" class="flex-shrink-0 h-5 text-gray-600 mr-2" aria-hidden="true" />
                        <p>Début</p>
                    </div>
                    <span class="step-link"></span> <!-- link between steps -->
                    <div id="steps-zone">
                        <!-- step blocks goes here -->
                    </div>
                    <!-- ADD STEP BUTTON -->
                    <ValidateButton v-on:click="addStep">
                        <component :is="icon.plus" class="flex-shrink-0 h-5 text-white mr-2" aria-hidden="true" />
                        <p>Ajouter une étape</p>
                    </ValidateButton>
                    <span class="step-link"></span> <!-- link between steps -->
                    <!-- END FLAG ELEMENT -->
                    <div class="h-fit whitespace-nowrap inline-flex items-center justify-center px-4 py-2 w-fit rounded-md shadow-sm text-base border border-gray-200 font-medium text-gray-600 bg-white">
                        <component :is="icon.stop" class="flex-shrink-0 h-5 text-gray-600 mr-2" aria-hidden="true" />
                        <p>Fin</p>
                    </div>
                </div>
                <!-- model 3D view zone -->
                <div :class="mode==MODE_MODEL? '': 'hidden'" class="flex flex-col grow m-2 border-2 border-white border rounded-lg overflow-hidden">
                    <div class="fixed"> <!-- CONTROL ICONS -->
                        <div v-on:click="setControlMode('translate')" class="rounded-lg shadow border border-gray-200 bg-gray-100 m-2 w-8 h-8 p-1 cursor-pointer hover:shadow-lg hover:bg-gray-50">
                            <img src="../assets/images/logos/move.png" alt="move icon">
                        </div>
                        <div v-on:click="setControlMode('rotate')" class="rounded-lg shadow border border-gray-200 bg-gray-100 m-2 w-8 h-8 p-1 cursor-pointer hover:shadow-lg hover:bg-gray-50">
                            <img src="../assets/images/logos/rotate.png" alt="rotate icon">
                        </div>
                        <div v-on:click="setControlMode('scale')" class="rounded-lg shadow border border-gray-200 bg-gray-100 m-2 w-8 h-8 p-1.5 cursor-pointer hover:shadow-lg hover:bg-gray-50">
                            <img src="../assets/images/logos/scale.png" alt="rotate icon">
                        </div>
                    </div>
                    <canvas id="3D-view" class="flex grow"></canvas>
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
} from "@heroicons/vue/solid";

import {
    saveScenario,
    addStep,
    addMachineSelection,
    availableMachines,
    fetchScenario,
    updateAvailableMachines,
    updateAvailableTargets,
    onMachineChanged,
    setDisplayMachinesCallback
} from "../script/CreateScenario";

import  {
    checkForCanvasSetup,
    startRendering,
    stopRendering,
    set3DMachineModel,
    setControlMode
} from "../script/Scenario3DEditor";

/**
 * Setup function, called at the beginning.
 * Fetches the original scenario if in edit mode, updates all the available machines, targets, etc.
 * and attaches all the required event listeners
 */
function setup() {
        fetchScenario().then(res => {
        updateAvailableMachines();
        updateAvailableTargets();
        const machineSelect = document.getElementById("select-machines");
        machineSelect.addEventListener("change", ev => {
            onMachineChanged(ev);
            
            // get the machine ID to load the correct 3D model
            const id = parseInt(ev.target.value)
            if (isNaN(id)) return;
            set3DMachineModel(id);
            const link = API.ROUTE.MACHINES+id+API.ROUTE.__MODEL;
        });
    }).catch(console.error);
}

const MODE_STEPS = "steps";
const MODE_MODEL = "model";
let mode = MODE_STEPS;

function updateMode(newMode) {
    if (newMode == MODE_MODEL) {
        setTimeout(() => {
            checkForCanvasSetup();
            startRendering();
        }, 10);
    } else {
        stopRendering();
    }
}

export default {
    name: "CreateScenario",
    components: {
        Topbar,
        BackButton,
        ValidateButton,
        PaginationChoice
    },
    data() {return {icon: {flag: FlagIcon, stop: StopIcon, plus: PlusCircleIcon}, API, availableMachines, mode, MODE_STEPS, MODE_MODEL};},
    mounted() {
        setup();
        // set the callback to show the machine pagination window
        setDisplayMachinesCallback(() => {
            this.$refs["machinePagination"].show();
        });
    },
    methods: {saveScenario, addStep, addMachineSelection, updateMode, setControlMode}
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