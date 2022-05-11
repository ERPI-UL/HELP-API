<template>
    <div class="relative flex p-4 md:p-8 min-h-screen flex-col justify-center">
        <div class="bg-white p-4 md:p-8 shadow-xl mx-auto rounded-lg">
            <div class="mx-auto max-w-md">
                <div class="flex center">
                    <img src="../assets/images/icons/logo_indigo.png" class="hidden md:block h-10" alt="Tailwind Play" />
                    <h2 class="text-2xl leading-9 font-extrabold text-indigo-600 px-6 whitespace-wrap md:whitespace-nowrap">
                        Connecter un appareil
                    </h2>
                </div>
                <div>
                    <div class="divide-y divide-gray-300/50">
                        <div class="border-none">
                            <div id="login-credentials" v-show="!User.isConnected(User.currentUser)" >
                                <div class="space-y-6 py-8 text-base leading-7 text-gray-400">
                                    <div class="md:flex block justify-between">
                                        <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">Nom d'utilisateur: </p>
                                        <input type="text" name="username" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                    </div>
                                    <div class="md:flex block justify-between">
                                        <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">Mot de passe: </p>
                                        <input type="password" name="password" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                    </div>
                                </div>
                                <div v-show="User.isConnected(User.currentUser)" class="md:flex block justify-left">
                                    <p class="whitespace-nowrap center font-medium text-sm text-gray-500 p-1">Connecté à {{ User.currentUser.username }} : </p>
                                    <a v-on:click="useUserinfos" class="whitespace-nowrap center font-medium text-sm text-indigo-600 p-1 cursor-pointer hover:underline">Utiliser</a>
                                </div>
                            </div>
                            <div id="login-userinfos" v-show="User.isConnected(User.currentUser)">
                                <div class="md:flex block justify-left">
                                    <p class="whitespace-nowrap center font-medium text-sm text-gray-500 p-1">Connecté à {{ User.currentUser.username }} : </p>
                                    <a v-on:click="useCredentials" class="whitespace-nowrap center font-medium text-sm text-indigo-600 p-1 cursor-pointer hover:underline">Changer</a>
                                </div>
                            </div>
                        </div>
                        <div class="space-y-6 py-8 text-base leading-7 text-gray-400">
                            <div class="md:flex block justify-between">
                                <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2 text-center">Code appareil: </p>
                                <div class="flex justify-center">
                                    <input type="number" name="number1" class="input-numbers whitespace-nowrap inline-flex max-w-[32px] text-center p-1 mx-1 center border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                    <input type="number" name="number2" class="input-numbers whitespace-nowrap inline-flex max-w-[32px] text-center p-1 mx-1 center border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                    <input type="number" name="number3" class="input-numbers whitespace-nowrap inline-flex max-w-[32px] text-center p-1 mx-1 center border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                    <input type="number" name="number4" class="input-numbers whitespace-nowrap inline-flex max-w-[32px] text-center p-1 mx-1 center border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                    <input type="number" name="number5" class="input-numbers whitespace-nowrap inline-flex max-w-[32px] text-center p-1 mx-1 center border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                </div>
                            </div>
                        </div>
                        <div id="log-zone" class="border-none overflow-y-hidden h-[0px]">
                            <p class="opacity-0 text-center text-indigo-600">Message</p>
                        </div>
                        <div class="pt-8 flex justify-between">
                            <Backbutton>Annuler</Backbutton>
                            <ValidateButton id="btn-validate" v-on:click="onValidate">Valider</ValidateButton>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Backbutton from "../components/BackButton.vue";
import ValidateButton from "../components/ValidateButton.vue";
import API from '../script/API';
import User from "../script/User";

const setupInputs = () => {
    const inputs = document.querySelectorAll(".input-numbers");
    for (let i = 0; i < inputs.length; i++) {
        const el = inputs.item(i);
        el.addEventListener("keydown", ev => {
            const char = ev.key.charAt(0);
            if (char < '0' || char > '9') {
                el.value = "";
            } else {
                el.value = char;
                if (i < inputs.length - 1) {
                    inputs.item(i + 1).focus();
                } else el.blur();
            }
            if (ev.key == "Backspace" && i > 0) {
                inputs.item(i - 1).focus();
            }
            ev.preventDefault();
        });
    }
    window.addEventListener("keydown", ev => {
        if (ev.key != "Enter") return;
        const btn = document.getElementById("btn-validate");
        if (btn) btn.click();
    });
}

let usingCredentials = !User.isConnected(User.currentUser);
function useCredentials() {
    usingCredentials = true;
    document.getElementById("login-userinfos").style.display = "none";
    document.getElementById("login-credentials").style.display = "inherit";
}

function useUserinfos() {
    usingCredentials = false;
    document.getElementById("login-credentials").style.display = "none";
    document.getElementById("login-userinfos").style.display = "inherit";
}

function logMessage(msg) {
    const btn = document.getElementById("btn-validate");
    btn.innerHTML = "Valider";

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

function onValidate() {
    const btn = document.getElementById("btn-validate");
    btn.innerHTML = "...";
    const credentials = {
        username: document.querySelector("input[name=username]"),
        password: document.querySelector("input[name=password]"),
        number: {
            value: document.querySelector("input[name=number1]").value +
                document.querySelector("input[name=number2]").value +
                document.querySelector("input[name=number3]").value +
                document.querySelector("input[name=number4]").value +
                document.querySelector("input[name=number5]").value,
            focus() {document.querySelector("input[name=number1]").focus()}
        }
    };

    if (usingCredentials) { // check for user credentials
        if (credentials.username.value.trim() == "") {
            logMessage("Veuillez renseigner un nom d'utilisateur.");
            credentials.username.focus();
            return;
        }
        if (credentials.password.value.trim() == "") {
            logMessage("Veuillez renseigner un mot de passe.");
            credentials.password.focus();
            return;
        }
    }

    if (credentials.number.value.trim().length < 5) {
        logMessage("Veuillez renseigner un code appareil valide.");
        credentials.number.focus();
        return;
    }

    if (credentials.username) {
        API.execute(API.ROUTE.LOGIN, API.METHOD_POST, {username: credentials.username.value, password: credentials.password.value}, API.TYPE_FORM).then(res => {
            sendEasyConnectRequest({
                token: User.currentUser.token.type + " " + User.currentUser.token.token,
                code: credentials.number.value
            });
        }).catch(err => {
            console.error(err);
            logMessage("Nom d'utilisateur ou mot de passe incorrect.");
        });
        
    } else {
        sendEasyConnectRequest({
            token: User.currentUser.token.type + " " + User.currentUser.token.token,
            code: credentials.number.value
        });
    }
}

function sendEasyConnectRequest(data) {
    API.execute_logged(API.ROUTE.EASY_CONNECT, API.METHOD_POST, User.currentUser.getCredentials(), data, API.TYPE_JSON).then(res => {
        logMessage("Appareil connecté au compte.");
    }).catch(err => {
        console.error(err);
        switch (err.status) {
            case 404:
                logMessage("Erreur: Appareil inconnu.");
                break;
            default:
                logMessage("Erreur lors de la connexion.");
                break;
        }
    });
}

export default {
    name: "Easyconnect",
    components: {
        Backbutton,
        ValidateButton
    },
    setup() {
        return {User, usingCredentials};
    },
    mounted() {
        setupInputs();
    },
    methods: {onValidate, useCredentials, useUserinfos}
    
};
</script>