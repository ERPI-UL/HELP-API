<template>
    <div class="min-h-screen max-h-screen flex flex-col">
        <div class="p-2"> <!-- Header -->
            <Topbar></Topbar>
        </div>
        <div id="content" class="flex flex-row grow min-h-0">
            <div class="flex flex-col grow-0 w-fit m-2">
                <div class="flex grow flex-col"> <!-- left panel (basic informations) -->
                    <div id="scenario-header" class="flex flex-col grow">
                        <h2 class="text-2xl text-indigo-600 font-extrabold mx-2 my-1 bg-white p-2 rounded-lg">{{ User.LANGUAGE.DATA.SCENARIOS.MESSAGES.MAIN_INFORMATIONS }}</h2>
                        <div class="flex flex-col m-2 h-fit bg-white rounded-lg p-2">
                            <div class="flex justify-between"> <!-- Scenario name input (input label and input zone) -->
                                <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">{{ User.LANGUAGE.DATA.SCENARIOS.MESSAGES.SCENARIO_NAME }} : </p>
                                <input type="text" id="input-scenarioname" name="scenario-name" value="" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                            </div>
                            <div class="flex flex-col grow-0"> <!-- Scenario description input (input label and input zone) -->
                                <p class="text-gray-500 font-base text-lg p-2 mr-4">{{ User.LANGUAGE.DATA.SCENARIOS.MESSAGES.SCENARIO_DESCRIPTION }} : </p>
                                <textarea id="input-scenariodesc" name="scenario-desc" rows="10" style="resize: both;" class="md:size-to-parent px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100"></textarea>
                            </div>
                            <div class="flex justify-between mt-2 h-fit bg-white rounded-lg"> <!-- Machine selection zone -->
                                <p class="text-gray-500 font-base text-lg p-2 mr-4">{{ User.LANGUAGE.DATA.SCENARIOS.MESSAGES.TARGET_MACHINE }} : </p>
                                <select name="machines" id="select-machines" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 pr-10 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                    <!-- available machines goes here, plus the <select> option -->
                                    <option value="<select>">{{ User.LANGUAGE.DATA.ACTIONS.SELECT }} ...</option>
                                </select>
                                <!-- Machine pagination popup -->
                                <PaginationChoice 
                                    ref="machinePagination" :title="User.LANGUAGE.DATA.PAGINATION.MACHINE_SELECTION"
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
                                <BackButton>{{pageMode==MODE_VIEW? User.LANGUAGE.DATA.ACTIONS.BACK : User.LANGUAGE.DATA.ACTIONS.CANCEL}}</BackButton> <!-- Cancel button -->
                                <ValidateButton id="save-btn" v-if="pageMode != MODE_VIEW" v-on:click="() => saveScenario(this)">{{ User.LANGUAGE.DATA.ACTIONS.SAVE }}</ValidateButton> <!-- Save button -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="flex flex-col grow w-fit m-2 min-w-0"> <!-- right panel (steps customization) -->
                <div id="tabs" class="flex grow-0 justify-between">
                    <h2 id="MODE_STEP_h2" v-on:click="updateMode(MODE_STEPS);" class="flex grow justify-start text-2xl text-indigo-600 font-extrabold mx-2 my-1 bg-white py-2 px-4 rounded-lg cursor-pointer select-none">{{ User.LANGUAGE.DATA.SCENARIOS.MESSAGES.STEPS }}</h2>
                    <h2 id="MODE_MODEL_h2" v-on:click="updateMode(MODE_MODEL);" class="flex grow justify-end text-2xl text-indigo-600 font-extrabold mx-2 my-1 bg-white py-2 px-4 rounded-lg cursor-pointer select-none">{{ User.LANGUAGE.DATA.SCENARIOS.MESSAGES.MODEL }}</h2>
                </div>
                <!-- steps zone -->
                <div id="MODE_STEP_div" :class="obj.mode==MODE_STEPS? '': 'hidden'" class="flex flex-col m-2 grow overflow-auto border border-2 border-white rounded-lg p-4">
                    <!-- START FLAG ELEMENT -->
                    <div class="whitespace-nowrap inline-flex items-center justify-center px-4 py-2 rounded-md shadow-sm text-base border border-gray-200 font-medium text-gray-600 bg-white w-fit">
                        <component :is="icon.flag" class="flex-shrink-0 h-5 text-gray-600 mr-2" aria-hidden="true" />
                        <p>{{ User.LANGUAGE.DATA.SCENARIOS.MESSAGES.START }}</p>
                    </div>
                    <div id="steps-zone">
                        <!-- step blocks goes here -->
                    </div>
                    <!-- END FLAG ELEMENT -->
                    <div class="h-fit whitespace-nowrap inline-flex items-center justify-center px-4 py-2 w-fit rounded-md shadow-sm text-base border border-gray-200 font-medium text-gray-600 bg-white">
                        <component :is="icon.stop" class="flex-shrink-0 h-5 text-gray-600 mr-2" aria-hidden="true" />
                        <p>{{ User.LANGUAGE.DATA.SCENARIOS.MESSAGES.END }}</p>
                    </div>
                </div>
                <!-- model 3D view zone -->
                <div id="MODE_MODEL_div" :class="obj.mode==MODE_MODEL? '': 'hidden'" class="flex flex-col grow m-2 border-2 border-white border rounded-lg overflow-hidden">
                    <div class="fixed"> <!-- CONTROL ICONS -->
                        <div v-on:click="toogleControls($event.target)" class="control-btn flex rounded-lg shadow border border-gray-200 bg-gray-100 m-2 w-8 h-8 cursor-pointer hover:shadow-lg hover:bg-gray-50">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 m-auto text-gray-600" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M3.707 2.293a1 1 0 00-1.414 1.414l14 14a1 1 0 001.414-1.414l-1.473-1.473A10.014 10.014 0 0019.542 10C18.268 5.943 14.478 3 10 3a9.958 9.958 0 00-4.512 1.074l-1.78-1.781zm4.261 4.26l1.514 1.515a2.003 2.003 0 012.45 2.45l1.514 1.514a4 4 0 00-5.478-5.478z" clip-rule="evenodd" />
                                <path d="M12.454 16.697L9.75 13.992a4 4 0 01-3.742-3.741L2.335 6.578A9.98 9.98 0 00.458 10c1.274 4.057 5.065 7 9.542 7 .847 0 1.669-.105 2.454-.303z" />
                            </svg>
                            <div class="tooltip absolute translate-x-9 py-[0.2rem] px-2 whitespace-nowrap bg-gray-50 border border-gray-200 rounded-lg">{{ User.LANGUAGE.DATA.SCENARIOS.MESSAGES.SHOW_HIDE_CONTROLS }}</div>
                        </div>
                        <div v-on:click="resetControls($event.target)" class="control-btn flex rounded-lg shadow border border-gray-200 bg-gray-100 m-2 w-8 h-8 cursor-pointer hover:shadow-lg hover:bg-gray-50">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 m-auto text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                <path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                            </svg>
                            <div class="tooltip absolute translate-x-9 py-[0.2rem] px-2 whitespace-nowrap bg-gray-50 border border-gray-200 rounded-lg">{{ User.LANGUAGE.DATA.SCENARIOS.MESSAGES.RESET_VIEW }}</div>
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
    setDisplayMachinesCallback,
    setEditPositionCallback
} from "../script/CreateScenario";

import  {
    checkForCanvasSetup,
    startRendering,
    stopRendering,
    set3DMachineModel,
    toogleTransformEnabled,
    setLabel,
    clearLabels,
    resetCameraTransform
} from "../script/Scenario3DEditor";
import { disableEl } from '../script/common';

/**
 * Setup function, called at the beginning.
 * Fetches the original scenario if in edit mode, updates all the available machines, targets, etc.
 * and attaches all the required event listeners
 */
function setup() {
    // if view mode, disable all the inputs, textarea, selects
    if (pageMode == MODE_VIEW) {
        disableEl(document.getElementById("input-scenarioname"));
        disableEl(document.getElementById("input-scenariodesc"));
        disableEl(document.getElementById("select-machines"));
    }

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
        });
        updateMode(MODE_STEPS);
    }).catch(console.error);
}

const MODE_STEPS = "steps";
const MODE_MODEL = "model";
let obj = {mode: ""};

let editedBlock = null;

function updateMode(newMode) {
    return new Promise((resolve, reject) => {
        if (newMode == MODE_MODEL) {
            setTimeout(() => {
                checkForCanvasSetup();
                startRendering();
                resolve();
            }, 10);
        } else {
            if (editedBlock != null) {    
                const dom = document.getElementById("stepcontainer-"+editedBlock.id);
                dom.querySelector("input[name='pos-x']").value = editedBlock.position.x;
                dom.querySelector("input[name='pos-y']").value = editedBlock.position.y;
                dom.querySelector("input[name='pos-z']").value = editedBlock.position.z;
                editedBlock = null;
                clearLabels();
            }
            stopRendering();
            resolve();
        }

        if (obj.mode != newMode) {
            const stepH2 = document.getElementById("MODE_STEP_h2");
            const modelH2 = document.getElementById("MODE_MODEL_h2");
            const stepDIV = document.getElementById("MODE_STEP_div");
            const modelDIV = document.getElementById("MODE_MODEL_div");
            stepH2.classList[newMode == MODE_STEPS? "remove": "add"]("bg-indigo-50", "text-indigo-300");
            stepH2.classList[newMode == MODE_STEPS? "add": "remove"]("shadow-lg");
            modelH2.classList[newMode == MODE_MODEL? "remove": "add"]("bg-indigo-50", "text-indigo-300");
            modelH2.classList[newMode == MODE_MODEL? "add": "remove"]("shadow-lg");
            stepDIV.classList[newMode == MODE_MODEL? "add": "remove"]("hidden");
            modelDIV.classList[newMode == MODE_MODEL? "remove": "add"]("hidden");
            obj.mode = newMode;
        }
    })
}

setEditPositionCallback(block => {
    updateMode(MODE_MODEL).then(() => {
        setLabel(block.label, block.position);
        editedBlock = block;
    });
});

function setIcon(el, state) {
    if (state) {
        el.innerHTML = `<path fill-rule="evenodd" d="M3.707 2.293a1 1 0 00-1.414 1.414l14 14a1 1 0 001.414-1.414l-1.473-1.473A10.014 10.014 0 0019.542 10C18.268 5.943 14.478 3 10 3a9.958 9.958 0 00-4.512 1.074l-1.78-1.781zm4.261 4.26l1.514 1.515a2.003 2.003 0 012.45 2.45l1.514 1.514a4 4 0 00-5.478-5.478z" clip-rule="evenodd" />
                        <path d="M12.454 16.697L9.75 13.992a4 4 0 01-3.742-3.741L2.335 6.578A9.98 9.98 0 00.458 10c1.274 4.057 5.065 7 9.542 7 .847 0 1.669-.105 2.454-.303z" />
                       `;
    } else el.innerHTML = `<path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                           <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
                       `;
}

function getCTRLBtn(el, counter) {
    if (counter > 4) return null;
    if (el.classList.contains("control-btn"))
        return el;
    else if (el.parentElement)
        return getCTRLBtn(el.parentElement);
    else return null;
}

/**@param {HTMLElement} el */
function toogleControls(el) {
    const state = toogleTransformEnabled();
    const btn = getCTRLBtn(el);
    if (btn) setIcon(btn.querySelector("svg"), !state);
}

/**@param {HTMLElement} el */
function resetControls(el) {
    const state = resetCameraTransform();
}

const pageMode = window.location.pathname.split("/").pop();
const MODE_VIEW = "view";

export default {
    name: "CreateScenario",
    components: {
        Topbar,
        BackButton,
        ValidateButton,
        PaginationChoice
    },
    data() {return {User, icon: {flag: FlagIcon, stop: StopIcon, plus: PlusCircleIcon}, API, availableMachines, obj, MODE_STEPS, MODE_MODEL, pageMode, MODE_VIEW};},
    mounted() {
        setup();
        // set the callback to show the machine pagination window
        setDisplayMachinesCallback(() => {
            this.$refs["machinePagination"].show();
        });
    },
    methods: {saveScenario, addStep, addMachineSelection, updateMode, toogleControls, resetControls}
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
    margin: 0.5em 0.5em 0.5em 1em;
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
.insert-btn {
    display: flex;
    margin-top: auto;
    margin-bottom: auto;
    cursor: pointer;
    color: #4B556380;
    transform: translateX(0em);
    padding: 0.2em;
    border-radius: 0.375em;
} .insert-btn:hover {
    transform: translateX(0.3em);
    color: #4F46E5;
    background-color: #4B556310;
}
.insert-btn > p {
    color: #4B556300;
} .insert-btn:hover > p {
    color: inherit;
}
</style>