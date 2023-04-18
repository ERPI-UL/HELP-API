<template>
    <div class="min-h-screen max-h-screen flex flex-col">
        <div class="p-2"> <!-- Header -->
            <Topbar></Topbar>
        </div>
        <div id="content" class="flex flex-row justify-between grow min-h-0">
            <div
                id="left-side"
                class="flex flex-col min-w-0 transition-none"
                style="width: 70%;"
            > <!-- steps customization -->
                <h2 class="flex justify-start text-2xl text-indigo-600 font-extrabold mx-2 mr-1 my-1 bg-white py-2 px-4 rounded-lg select-none">{{ User.LANGUAGE.DATA.SCENARIOS.MESSAGES.STEPS }}</h2>
                <!-- steps zone -->
                <div id="steps-container" class="flex grow relative flex-col m-2 mr-1 overflow-auto border border-2 border-white rounded-lg p-2">
                    <div class="absolute flex w-2 h-2 right-0 bottom-0"> <!-- BOTTOM BUTTONS -->
                        <div class="fixed flex translate-x-[-100%] translate-y-[-100%] space-x-4">
                            <div class="flex space-x-2">
                                <button
                                    id="run-scenario"
                                    v-show="!scenario_running"
                                    class="bg-indigo-600 px-2 py-2 h-fit flex justify-left shadow-md rounded text-white hover:bg-indigo-700 hover:shadow-lg"
                                    @click="runScenario"
                                >
                                    <component :is="PlayIcon" class="w-6 h-6" />
                                    <p class="px-1"> {{ User.LANGUAGE.DATA.ACTIONS.RUN_SCENARIO }} </p>
                                </button>
                                
                                <button
                                    id="prev-run-step"
                                    v-show="scenario_running"
                                    class="bg-indigo-600 px-2 py-2 h-fit flex justify-left shadow-md rounded text-white hover:bg-indigo-700 hover:shadow-lg"
                                    @click="previousStep"
                                >
                                    <component :is="ChevronLeftIcon" class="w-6 h-6" />
                                </button>
                                
                                <button
                                    id="pause-scenario"
                                    v-show="scenario_running"
                                    class="bg-indigo-600 px-2 py-2 h-fit flex justify-left shadow-md rounded text-white hover:bg-indigo-700 hover:shadow-lg"
                                    @click="runScenario"
                                >
                                    <component :is="StopIcon" class="w-6 h-6" />
                                </button>
                                
                                <button
                                    id="next-run-step"
                                    v-show="scenario_running"
                                    class="bg-indigo-600 px-2 py-2 h-fit flex justify-left shadow-md rounded text-white hover:bg-indigo-700 hover:shadow-lg"
                                    @click="nextStep"
                                >
                                    <component :is="ChevronRightIcon" class="w-6 h-6" />
                                </button>
                            </div>
                            <button
                                id="edit-position"
                                v-show="pageMode == MODE_VIEW"
                                class="bg-indigo-600 px-2 py-2 h-fit flex justify-left shadow-md rounded text-white hover:bg-indigo-700 hover:shadow-lg"
                                @click="editScenario"
                            >
                                <component :is="PencilIcon" class="w-6 h-6" />
                                <p class="px-1">{{ User.LANGUAGE.DATA.ACTIONS.EDIT }}</p>
                            </button>
                        </div>
                    </div>

                    <!-- START FLAG ELEMENT -->
                    <div class="whitespace-nowrap inline-flex items-center justify-center px-4 py-2 rounded-md shadow-sm text-base border border-gray-200 font-medium text-gray-600 bg-white w-fit">
                        <component :is="icon.flag" class="flex-shrink-0 h-5 text-gray-600 mr-2" aria-hidden="true" />
                        <p>{{ User.LANGUAGE.DATA.SCENARIOS.MESSAGES.START }}</p>
                    </div>
                    <div id="steps-zone" @click="deselectStep">
                        <!-- step blocks goes here -->
                    </div>
                    <!-- END FLAG ELEMENT -->
                    <div class="h-fit whitespace-nowrap inline-flex items-center justify-center px-4 py-2 w-fit rounded-md shadow-sm text-base border border-gray-200 font-medium text-gray-600 bg-white">
                        <component :is="icon.stop" class="flex-shrink-0 h-5 text-gray-600 mr-2" aria-hidden="true" />
                        <p>{{ User.LANGUAGE.DATA.SCENARIOS.MESSAGES.END }}</p>
                    </div>
                </div>
            </div>
            <div id="steps-resize" class="resize-slider flex my-2 px-1 cursor-col-resize select-none"> <!-- separator with resize slider -->
                <span class="flex w-1 grow rounded-lg bg-slate-300">
                    
                </span>
            </div>
            <div
                id="right-side"
                class="flex flex-col grow-0 transition-none"
                style="width: 30%;"
            >
                <!-- model 3D view zone -->
                <h2 class="flex justify-start text-2xl text-indigo-600 font-extrabold mx-2 ml-1 my-1 bg-white py-2 px-4 h-fit rounded-lg select-none">{{ User.LANGUAGE.DATA.SCENARIOS.MESSAGES.MODEL }}</h2>
                <div class="flex flex-col grow m-2 ml-1 border-2 border-white border rounded-lg overflow-hidden">
                    <div class="fixed"> <!-- CONTROL ICONS -->
                        <div v-show="pageMode !== MODE_VIEW" v-on:click="toogleControls($event.target)" class="control-btn flex rounded-lg shadow border border-gray-200 bg-gray-100 m-2 w-8 h-8 cursor-pointer hover:shadow-lg hover:bg-gray-50">
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
                <div class="flex mb-2 flex-col"> <!-- basic informations -->
                    <div id="scenario-header" class="flex flex-col grow">
                        <h2 class="text-2xl text-indigo-600 font-extrabold mx-2 ml-1 my-1 bg-white p-2 rounded-lg">{{ User.LANGUAGE.DATA.SCENARIOS.MESSAGES.MAIN_INFORMATIONS }}</h2>
                        <div class="flex flex-col m-2 ml-1 h-fit bg-white rounded-lg p-2">
                            <div class="flex justify-between"> <!-- Scenario name input (input label and input zone) -->
                                <p class="text-gray-500 font-base text-lg p-2 mr-4 whitespace-nowrap">{{ User.LANGUAGE.DATA.SCENARIOS.MESSAGES.SCENARIO_NAME }} : </p>
                                <input type="text" id="input-scenarioname" name="scenario-name" value="" class="md:size-to-parent whitespace-nowrap inline-flex min-w-0 max-w-full px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                            </div>
                            <div class="flex flex-col grow-0"> <!-- Scenario description input (input label and input zone) -->
                                <p class="text-gray-500 font-base text-lg p-2 mr-4">{{ User.LANGUAGE.DATA.SCENARIOS.MESSAGES.SCENARIO_DESCRIPTION }} : </p>
                                <textarea id="input-scenariodesc" name="scenario-desc" rows="4" style="resize: both;" class="md:size-to-parent px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100"></textarea>
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
    PlusCircleIcon,
    PlayIcon,
    PencilIcon,
    ChevronLeftIcon,
    ChevronRightIcon
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
    setEditPositionCallback,
    editPositionCallback,
    blockInfoFromDom
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
function setup(obj) {
    // if view mode, disable all the inputs, textarea, selects
    if (obj.pageMode == MODE_VIEW) {
        disableEl(document.getElementById("input-scenarioname"));
        disableEl(document.getElementById("input-scenariodesc"));
        disableEl(document.getElementById("select-machines"));
    }

    const resizeBar = document.getElementById("steps-resize");
    const content = document.getElementById("content");
    const leftSide = document.getElementById("left-side");
    const rightSide = document.getElementById("right-side");
    resizeBar.addEventListener("mousedown", ev => {
        const rect = content.getBoundingClientRect();
        const moveEvent = ev => {
            let percent = (ev.clientX - rect.left) / rect.width;
            percent = Math.max(0.2, Math.min(0.8, percent));
            leftSide.style.width = `${percent * 100}%`;
            rightSide.style.width = `${(1 - percent) * 100}%`;
            window.onresize();
        };
        window.addEventListener("mousemove", moveEvent);
        window.addEventListener("mouseup", ev => {
            window.removeEventListener("mousemove", moveEvent);
        });
    });

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
    }).catch(console.error);

    setTimeout(() => {
        checkForCanvasSetup();
        startRendering();
    }, 10);
}

let selectedBlock = null;
let setposinterval = -1;
setEditPositionCallback(block => {
    const dom = document.getElementById("stepcontainer-"+block?.id);

    if (block !== selectedBlock) {
        clearLabels();
        const classes = ["border-indigo-600", "shadow-indigo-600"];
        const oldDom = document.getElementById("stepcontainer-"+selectedBlock?.id);
        classes.forEach(c => {
            oldDom?.classList.remove(c);
            dom?.classList.add(c);
        });
        selectedBlock = block;
    }
    
    if (block == null) return;
    setLabel(block);

    if (dom.pageMode == MODE_VIEW) return;
    if (setposinterval !== -1) {
        clearInterval(setposinterval);
        setposinterval = -1;
    }
    const xInput = dom.querySelector("input[name='pos-x']");
    let xValue = xInput.value;
    const yInput = dom.querySelector("input[name='pos-y']");
    let yValue = yInput.value;
    const zInput = dom.querySelector("input[name='pos-z']");
    let zValue = zInput.value;
    setposinterval = setInterval(() => {
        if (selectedBlock === null) {
            clearInterval(setposinterval);
            setposinterval = -1;
            return;
        }
        if (xValue != selectedBlock.position.x) {
            xValue = selectedBlock.position.x;
            xInput.value = xValue;
        }
        if (yValue != selectedBlock.position.y) {
            yValue = selectedBlock.position.y;
            yInput.value = yValue;
        }
        if (zValue != selectedBlock.position.z) {
            zValue = selectedBlock.position.z;
            zInput.value = zValue;
        }
    }, 100);
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

const MODE_VIEW = "view";

function deselectStep(ev) {
    const isInStep = (el, counter=0) => {
        if (counter > 10) return false;
        if (el.id.startsWith('stepcontainer')) return true;
        else if (el.parentElement) return isInStep(el.parentElement, counter+1);
        else return false;
    }
    
    if (!isInStep(ev.target)) {
        editPositionCallback(null);
    }
}

let dom = null;
function runScenario(ev) {
    if (dom.scenario_running) {
        dom.scenario_run_step = null;
        dom.scenario_running = false;
    } else {
        dom.scenario_run_step = 0;
        dom.scenario_running = true;
    }
    updateSelectedStep();
}

function updateSelectedStep() {
    const steps = dom.$el.querySelectorAll(".step-part-container");
    if (dom.scenario_run_step === null) dom.scenario_run_step = -1;
    else dom.scenario_run_step = Math.max(0, Math.min(dom.scenario_run_step, steps.length-1));
    steps.forEach((s, i) => {
        if (i == dom.scenario_run_step) {
            s.classList.add("border-indigo-600", "shadow-indigo-600");
        } else {
            s.classList.remove("border-indigo-600", "shadow-indigo-600");
        }
    });
    const container = dom.$el.querySelector("#steps-container");
    clearLabels();
    if (dom.scenario_run_step == -1) {
        container.scrollTo({
            top: 0,
            behavior: "smooth"
        });
        return;
    } else {
        container.scrollTo({
            top: steps[dom.scenario_run_step].offsetTop - 8,
            behavior: "smooth"
        });
        setLabel(blockInfoFromDom(steps[dom.scenario_run_step]));
    }
}

function nextStep() {
    dom.scenario_run_step++;
    updateSelectedStep();
}

function previousStep() {
    dom.scenario_run_step--;
    updateSelectedStep();
}

function editScenario(ev) {
    window.location.href = "/scenarios/edit?idScenario="+dom.$route.query.idScenario;
}

export default {
    name: "CreateScenario",
    components: {
        Topbar,
        BackButton,
        ValidateButton,
        PaginationChoice,
    },
    data() {
        return {
            User,
            icon: {flag: FlagIcon, stop: StopIcon, plus: PlusCircleIcon},
            API,
            availableMachines,
            pageMode: window.location.pathname.split("/").pop(),
            MODE_VIEW,
            scenario_running: false,
            scenario_run_step: 0,
            PlayIcon,
            StopIcon,
            PencilIcon,
            ChevronLeftIcon,
            ChevronRightIcon,
        };
    },
    mounted() {
        dom = this;
        setup(this);
        // set the callback to show the machine pagination window
        setDisplayMachinesCallback(() => {
            this.$refs["machinePagination"].show();
        });
    },
    methods: {saveScenario, addStep, addMachineSelection, toogleControls, resetControls, deselectStep, runScenario, editScenario, nextStep, previousStep}
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

.resize-slider:hover :nth-child(1) {
    @apply bg-indigo-600
}
</style>