<template>
    <div class="min-h-screen max-h-screen flex flex-col">
        <div class="p-2">
            <Topbar></Topbar>
        </div>
        <div id="content" class="flex grow min-h-0">
            <div class="flex m-auto grow-0 w-fit m-2">
                <div class="flex grow flex-col"> <!-- left panel (basic informations) -->
                    <div id="scenario-header" class="flex flex-col grow">
                        <h2 class="text-2xl text-indigo-600 font-extrabold mx-2 my-1 bg-white p-2 rounded-lg">{{ action }} une machine</h2>
                        <div class="flex flex-col m-2 h-fit bg-white rounded-lg p-2">
                            <div class="flex justify-between">
                                <p class="text-gray-500 font-base text-lg p-2 mr-4">Nom de la machine : </p>
                                <input type="text" id="input-machinename" name="scenario-name" value="" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                            </div>
                            <div class="flex flex-col grow-0">
                                <p class="text-gray-500 font-base text-lg p-2 mr-4">Description de la machine : </p>
                                <textarea id="input-machinedesc" rows="10" style="resize: both;" class="md:size-to-parent px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100"></textarea>
                            </div>
                            <div id="log-zone" class="border-none overflow-y-hidden h-[0px]">
                                <p class="opacity-0 text-center text-indigo-600">Message</p>
                            </div>
                            <div class="flex grow justify-between mt-2">
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

function logMessage(msg) {
    const btn = document.getElementById("validate-button");
    btn.innerHTML = action;

    const div = document.getElementById("log-zone");
    const txt = div.firstElementChild;
    txt.innerHTML = msg;
    txt.classList.add("opacity-100");
    div.style.height = txt.getBoundingClientRect().height+"px";
    setTimeout(() => {
        txt.classList.remove("opacity-100");
        div.style.height = "0px";
    }, 3000);
}

function saveMachine() {
    const button = document.getElementById("validate-button");
    button.innerHTML = "...";
    API.execute_logged(API.ROUTE.MACHINES+(action=="Créer"?"":queryParameters.idMachine), action=='Créer'? API.METHOD_POST: API.METHOD_PUT, User.currentUser.getCredentials(), {
        name: document.getElementById('input-machinename').value,
        description: document.getElementById('input-machinedesc').value
    }).then(res => {
        logMessage("Machine créée avec succès !");
        button.innerHTML = action;
    }).catch(err => {
        logMessage("Erreur lors de la création de la machine.");
        console.error(err);
    });
}

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
    data() {return {action};},
    mounted() {
        API.execute_logged(API.ROUTE.MACHINES+queryParameters.idMachine, API.METHOD_GET, User.currentUser.getCredentials(), {}, API.TYPE_JSON).then(res => {
            document.getElementById('input-machinename').value = res.name;
            document.getElementById('input-machinedesc').value = res.description;
        }).catch(console.error);
    },
    methods: {saveMachine}
};
</script>

<style>
</style>