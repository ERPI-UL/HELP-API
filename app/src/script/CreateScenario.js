import { getBlockDiv } from "./ScenarioBlock";
import User from '../script/User';
import { redirectHome } from '../script/common';

/**
 * BlockInfo class, represents a visual scenario step
 */
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

/**
 * Checks if two scenario blocks are equals, depending of their names, descriptions, targets, positions, etc.
 */
 function stepEquals(a, b) {
    const conditions = [
        a.name == b.name,
        a.ordernumber == b.ordernumber,
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

/**
 * Logs a message to the user
 * @param {string} msg message to display to the user
 */
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

// Current available machines in the machine html select
let availableMachines = [];
// Current available targets in the targets html selects (in the tutorial steps)
let availableTargets = [];

/**
 * Updates the available machines' targets inside all the targets html selects
 */
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

/**
 * Updates the available machines inside the machine html select
 */
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
            
            // fire the onchange event
            if (document.createEvent) {
                var evt = document.createEvent("HTMLEvents");
                evt.initEvent("change", false, true);
                selectMachines.dispatchEvent(evt);
            } else selectMachines.fireEvent("onchange");
    }, 10);
}

// available steps to redirect to in a button redirection html select (in choice steps)
let availableRedirects = [];
/**
 * Updates the available steps in every html redirection select
 */
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

/**
 * Event listener for machine selection change event,
 * updates the available targets for the new ones
 */
function onMachineChanged() {
    let val = document.getElementById("select-machines").value;
    switch (val) {
        case "<select>":
            displayMachineSelection();
            break;
    
        default:
            availableTargets = [];
            const curMachine = availableMachines.find(machine => machine.id == val);
            if (!curMachine) return;
            availableTargets = curMachine.targets;
            updateAvailableTargets();
            break;
    }
}

// callback used to display the machine pagination modal
// (overritten in CreateScenario.vue using the setDisplayMachinesCallback function)
let displayMachineSelection = () => {};
function setDisplayMachinesCallback(callback) {
    displayMachineSelection = callback;
}

/**
 * Adds the new selected content from the pagination window to the available machines list
 * And updates the html machine selects
 */
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

// Original scenario fetched at the beginning (if the page is in edit mode)
let originalScenario = null;

/**
 * Retreives the original edited scenario (if in edit mode) and stores it in the originalScenario variable
 * Updates the machine selection, available targets, available redirections (steps), etc.
 */
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

/**
 * Adds a new scenario block to the interface
 */
 function addStep() {
    createScenarioBlock();
}

/**
 * Removes a step target from a scenario block (from his ID)
 */
 function removeStepTarget(stepID) {
    document.getElementById("steptargetscontainer-"+stepID).lastElementChild?.remove();
    updateAvailableTargets();
}

// TODO : BUG DETECTED, FIX IT
/**
 * Removes a scenario block from the DOM and from the scenario blocks list
 * BUG DETECTED, NOT WORKING YET
 */
 function removeScenarioBlock(id) {
    const blockIndex = scenarioBlocks.findIndex(el => el.id == id);
    const block = scenarioBlocks[blockIndex];
    if (!block) return;
    const dom = block.dom;
    dom.nextElementSibling.remove();
    dom.remove();
    let current = block;
    const prev = scenarioBlocks.find(el => el.next == id);
    if (prev) prev.next = current.next;
    while (current.next != 0) {
        let nextIndex = scenarioBlocks.findIndex(el => el.id == current.next);
        if (nextIndex < 0 || current.next == 0) {
            current.next = 0;
            break;
        } else {
            current = scenarioBlocks[nextIndex];
            document.getElementById("stepname-"+current.id).innerHTML = "Étape "+(nextIndex);
        }
    }
    scenarioBlocks.splice(blockIndex, 1);
}

/**
 * Retreives all the scenario informations from a dom element and returns it as a BlockInfo object
 * @param {HTMLElement} dom the dom element to get the informations from
 */
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
                redirect: availableRedirects.find(r => r.id == parseInt(dom.querySelector("select[name='btn-left-redirect']")?.value)).name
            },
            option_right: {
                label: dom.querySelector("input[name='btn-right-label']")?.value,
                redirect: availableRedirects.find(r => r.id == parseInt(dom.querySelector("select[name='btn-right-redirect']")?.value)).name
            }
        }
    );
}

/**
 * Retreives all the scenario informations from the dom, builds a scenario object from it and returns it
 * Also checks if the scenario inputs are valid and if not, it returns null and displays a log message to the user
 */
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
            return null;
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

/**
 * Saves the scenario to the server with an API call,
 * only executed when the page is in creation mode, not edit mode
 */
 function saveCreations() {
    const button = document.getElementById("save-btn");
    const scenario = compileScenario();

    button.innerHTML = "...";
    API.execute_logged(API.ROUTE.SCENARIOS, API.METHOD_POST, User.currentUser.getCredentials(), scenario, API.TYPE_JSON).then(res => {
        button.innerHTML = "Enregistré !";
        redirectHome();
    }).catch(err => err.json().then(console.error));
}

/**
 * Saves all the modifications brought to a scenario to teh server with multiple API calls
 * according to modifications, additions, deletions, etc. made to the scenario
 */
 function saveModifications() {
    // logMessage("Erreur: Modification de scénario non supportée");
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
        let index = originalScenario.steps.findIndex(el => el.id === step.id);
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
                    API.execute_logged(API.ROUTE.STEPS + step.id, API.METHOD_PUT, User.currentUser.getCredentials(), {
                        name: step.name,
                        label: step.label,
                        description: step.description,
                        ordernumber: step.ordernumber,
                        position: step.position,
                        type: step.type,
                        targets: step.targets,
                        choice: step.choice
                    }, API.TYPE_JSON).then(res => {
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
        if (addCounter++ >= addedSteps.length) {
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

/**
 * Saves the scenario to the server (chooses between saveCreations and saveModifications depending on the page's mode)
 */
function saveScenario() {
    const url = window.location.pathname.split("/");
    if (url[url.length-1] == "edit")
        saveModifications();
    else saveCreations();
}

// scenario block's ID counter (incremented by 1 every time a new block is created)
let ID_COUNTER = 1;
// list of all the current displayed scenario blocks
let scenarioBlocks = [];

/**
 * Creates a new scenario block using the getBlockDiv function, adds it to the scenarioBlocks array,
 * adds it to the DOM and adds the event listeners to it.
 */
 function createScenarioBlock(name, title, desc, targets, pos, mode, btnInfos, id) {
    if (id) ID_COUNTER = id; // if an ID is given, set the counter accordingly
    const newID = ID_COUNTER++; // inscrease by one the counter
    const stepZone = document.getElementById("steps-zone");
    const newBlock = getBlockDiv(newID, name, title, desc, scenarioBlocks.length+1, pos, mode, btnInfos); // create the new block

    // add the new block and a wire behind it (the wire is only here for aesthetic reasons)
    stepZone.appendChild(newBlock);
    stepZone.appendChild(document.createElement("span")).classList.add("step-link");
    
    // add the block to the list (wired list so we set the .next attribute to the new block id)
    if (scenarioBlocks.length > 0)
        scenarioBlocks[scenarioBlocks.length-1].next = newID;
    scenarioBlocks.push({
        dom: newBlock,
        id: newID,
        next: 0,
        previous: (scenarioBlocks.length > 0)? scenarioBlocks[scenarioBlocks.length-1].id: 0
    });

    // timeout to be sure that the DOM is updated and ready for modifications
    setTimeout(() => {
        const selects = [];
        // add each target to the newly created block
        if (targets) targets.forEach(target => {selects.push({el: window.indico.addStepTarget(newID, target.id, target.name), id: target.id});});
        updateAvailableTargets(); // call the update function to fill those new step targets
        selects.forEach(select => {select.el.value = select.id}); // set the value of each select to the target's id
        
        // add en event listener for name change, to update the available redirects (the step names for choice button redirection)
        newBlock.querySelector("input[name='scenario-name']").addEventListener("change", ev => {
            let index = availableRedirects.findIndex(step => step.id == newID);
            if (index >= 0) availableRedirects[index].name = ev.target.value;
            updateAvailableRedirects(); // update all the html selects
        });

        // add an event listener for a step mode change, to display or not the choice button configuration panel
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

        updateAvailableRedirects(); // update the available redirects immediately to fill the html select with the newly created block
        // if the block defaut mode is choice, set all the choice button informations to the given ones
        if (mode == "choice") {
            const leftRedirect = availableRedirects.find(step => step.name === btnInfos.option_left.redirect);
            const rightRedirect = availableRedirects.find(step => step.name === btnInfos.option_right.redirect);
            if (leftRedirect) newBlock.querySelector("select[name='btn-left-redirect']").value = leftRedirect.id+"";
            if (rightRedirect) newBlock.querySelector("select[name='btn-right-redirect']").value = rightRedirect.id+"";
        }
    }, 10);
}

/**
 * Adds a step target to a given scenario block (from his ID)
 */
function addStepTarget(stepID, value, label) {
    // create the select element
    const select = document.createElement("select");
    select.name = "select-targets";
    select.classList.add("md:size-to-parent", "whitespace-nowrap", "inline-flex", "px-4", "py-2", "pr-10", "border-gray-200", "rounded-md", "shadow-sm", "text-base", "font-medium", "text-black", "bg-gray-50", "hover:bg-gray-100");
    // set his value and label
    if (value) select.value = value;
    if (label) select.innerHTML = label;
    // add it to the block and update its available targets
    document.getElementById("steptargetscontainer-"+stepID).appendChild(select);
    if (!value || !label) updateAvailableTargets();
    return select;
}

if (window.indico == undefined) window.indico = {};
window.indico.removeStepTarget = removeStepTarget;
window.indico.addStepTarget = addStepTarget;
window.indico.removeScenarioBlock = removeScenarioBlock;

// FOR DEBUG PURPOSE, DELETE IT LATER
window.displayJSON = function(str) {
    console.log(JSON.parse(str.replaceAll("\\", "")));
}

export {
    BlockInfo,
    logMessage,
    updateAvailableTargets,
    availableMachines,
    availableTargets,
    updateAvailableMachines,
    availableRedirects,
    updateAvailableRedirects,
    onMachineChanged,
    fetchScenario,
    originalScenario,
    addStep,
    blockInfoFromDom,
    compileScenario,
    saveCreations,
    stepEquals,
    saveModifications,
    saveScenario,
    removeStepTarget,
    removeScenarioBlock,
    addStepTarget,
    createScenarioBlock,
    addMachineSelection,
    setDisplayMachinesCallback
};