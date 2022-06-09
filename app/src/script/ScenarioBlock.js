/**
 * Returns a new HTML scenario block based on the given informations
 * @param {number} id id of the scenario block
 * @param {string} name name of the scenario block
 * @param {string} title title of the scenario block
 * @param {string} desc description of the scenario block
 * @param {{id:number,name:string}[]} ordernumber the order number of the scenario block (step index)
 * @param {{x:number,y:number,z:number}} pos position attribute of the scenario block
 * @param {string} mode mode of the scenario block
 * @param {any} btnInfos choice button informations of the scenario block
 */
 function getBlockDiv(id, name, title, desc, ordernumber, pos, mode="action", btnInfos={option_left: {label: "Bouton gauche", redirect: ""}, option_right: {label: "Bouton droit", redirect: ""}}) {
    const container = document.createElement("div");
    container.classList.add("step-part-container", "flex", "flex-col", "h-fit", "w-fit", "max-w-[80%]");
    container.id = "stepcontainer-" + id;
    container.innerHTML = 
    `<div class="flex justify-between m-1">
        <h2 id="stepname-${id}" class="text-sm m-1 text-indigo-600 font-extrabold">Étape ${ordernumber}</h2>
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
                <div class="flex">
                    <p class="text-gray-500 font-base text-lg p-2 mr-4 my-auto whitespace-nowrap">X: </p>
                    <input type="number" name="pos-x" id="input-stepposx-${id}" value="${pos!=undefined?pos.x:"0"}" class="input-numbers whitespace-nowrap inline-flex max-w-[72px] text-center p-1 center border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                </div>
                <div class="flex">
                    <p class="text-gray-500 font-base text-lg p-2 mr-4 my-auto whitespace-nowrap">Y: </p>
                    <input type="number" name="pos-y" id="input-stepposy-${id}" value="${pos!=undefined?pos.y:"0"}" class="input-numbers whitespace-nowrap inline-flex max-w-[72px] text-center p-1 center border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                </div>
                <div class="flex">
                    <p class="text-gray-500 font-base text-lg p-2 mr-4 my-auto whitespace-nowrap">Z: </p>
                    <input type="number" name="pos-z" id="input-stepposz-${id}" value="${pos!=undefined?pos.z:"0"}" class="input-numbers whitespace-nowrap inline-flex max-w-[72px] text-center p-1 center border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                </div>
                <div class="flex">
                    <button id="edit-position" class="bg-indigo-600 p-4 h-fit flex justify-left shadow-md rounded text-white hover:bg-indigo-700 hover:shadow-lg">Editer</button>
                </div>                
            </div>
        </div>
    </div>`;
    return container;
}

export {getBlockDiv};