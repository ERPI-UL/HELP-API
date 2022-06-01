<template>
    <!-- Login page, with username and password inputs to log into an account -->
    <div class="relative flex p-4 md:p-8 min-h-screen flex-col justify-center">
        <div class="bg-white p-4 md:p-8 shadow-xl mx-auto rounded-lg">
            <div class="mx-auto max-w-md">
                <!-- Modal title -->
                <div class="flex center">
                    <img src="../assets/images/icons/logo_indigo.png" class="hidden md:block h-10" alt="Tailwind Play" />
                    <h2 class="text-2xl leading-9 font-extrabold text-indigo-600 px-6 whitespace-nowrap">
                        Se connecter
                    </h2>
                </div>
                <div class="divide-y divide-gray-300/50">
                    <div class="space-y-6 pt-8 text-base leading-7 text-gray-400">
                        <!-- Username input -->
                        <div class="md:flex block justify-between">
                            <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">Nom d'utilisateur: </p>
                            <input type="text" id="input-username" name="username" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                        </div>
                        <!-- Password input -->
                        <div class="md:flex block justify-between">
                            <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">Mot de passe: </p>
                            <input type="password" id="input-password" name="password" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                        </div>
                        <!-- Forgot password button (to redirect to ForgotPassword.vue file) -->
                        <div class="md:flex block" v-on:click="forgotPassword();">
                            <p class="text-indigo-600 hover:underline cursor-pointer">Mot de passe oublié</p>
                        </div>
                    </div>
                    <!-- Message log zone -->
                    <div id="log-zone" class="border-none overflow-y-hidden h-[0px]">
                        <p class="opacity-0 text-center text-indigo-600"></p>
                    </div>
                    <!-- Buttons -->
                    <div class="pt-8 flex justify-between">
                        <BackButton>Annuler</BackButton> <!-- Cancel -->
                        <button id="btn-validate" v-on:click="onValidate" class="whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700">
                            Valider <!-- Validate -->
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import BackButton from "../components/BackButton.vue";
import User from "../script/User";
import API from "../script/API";
import { redirectHome } from "../script/common";

/**
 * When the forgot password button is clicked, redirect the user to the ForgotPassword page
 */
function forgotPassword() {
    window.location.href = '/forgotPassword';
}

/**
 * Attaches a event listener to the enter key to emultate a validate button click
 */
function setup() {
    window.addEventListener("keydown", ev => {
        if (ev.key != "Enter") return;
        const btn = document.getElementById("btn-validate");
        if (btn) btn.click();
    });
}

/**
 * Displays a log message to the user
 * @param {string} msg message to show
 */
function logMessage(msg) {
    const btn = document.getElementById("btn-validate");
    btn.innerHTML = "Valider";
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

/**
 * When the user clicks on the validate button,
 * check if all the inputs are filled correctly and if so
 * makes an API call to get the user's token / informations
 * and then redirects the user to the home page
 */
function onValidate() {
    const btn = document.getElementById("btn-validate");
    btn.innerHTML = "...";

    const credentials = {
        username: document.getElementById("input-username"),
        password: document.getElementById("input-password")
    };

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

    API.execute(API.ROUTE.LOGIN, API.METHOD_POST, {grant_type: "password", username: credentials.username.value, password: credentials.password.value}, API.TYPE_FORM).then(data => {
        if (data.error) logMessage(data.error);
        else {
            User.fromToken({token: data.access_token, type: data.token_type}).fetchInformations().then(user => {
                User.saveUser(user);
                logMessage("Connecté à "+user.username);
                btn.innerHTML = "Valider";
                redirectHome();
            }).catch(err => {
                console.error(err);
            });
        }
    }).catch(err => {
        console.error("Token request error: ", err);
        btn.innerHTML = "Valider";
        switch (err.status) {
            case 401:
                logMessage("Mot de passe invalide.");
                break;
            case 404:
                logMessage("Nom d'utilisateur invalide.");
                break;
        
            default:
                logMessage("Erreur lors de la connexion au serveur");
                break;
        }
    });

}

export default {
    name: "ForgotPassword",
    components: {
        BackButton
    },
    mounted() {
        setup();
    },
    methods: {onValidate, forgotPassword}
};
</script>