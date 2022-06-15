<template>
    <!-- Password reset web page -->
    <div class="relative flex p-4 md:p-8 min-h-screen flex-col justify-center">
        <div class="bg-white p-4 md:p-8 shadow-xl mx-auto rounded-lg max-w-full">
            <div class="mx-auto max-w-md">
                <!-- Modal title -->
                <div class="flex center max-w-full">
                    <img src="../assets/images/logo_indigo.png" class="hidden md:block h-10" alt="Tailwind Play" />
                    <h2 class="text-2xl leading-9 font-extrabold text-indigo-600 px-6">
                        {{ User.LANGUAGE.DATA.RESET.MESSAGES.TITLE.replace("{action}", action) }}
                    </h2>
                </div>
                <!-- Modal content -->
                <div class="divide-y divide-gray-300/50">
                    <div class="space-y-6 py-8 text-base leading-7 text-gray-400">
                        <!-- New password input zone -->
                        <div class="md:flex block justify-between">
                            <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">{{ User.LANGUAGE.DATA.COMMON.PASSWORD }}: </p>
                            <input type="password" id="input-password" name="new-password" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                        </div>
                        <!-- Password confirmation zone -->
                        <div class="md:flex block justify-between">
                            <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">{{ User.LANGUAGE.DATA.REGISTER.MESSAGES.CONFIRM_PASSWORD }}: </p>
                            <input type="password" id="input-password" name="password-confirm" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                        </div>
                    </div>
                    <!-- Message log zone -->
                    <div id="log-zone" class="border-none overflow-y-hidden h-[0px]">
                        <p class="opacity-0 text-center text-indigo-600"></p>
                    </div>
                    <!-- Buttons -->
                    <div class="pt-8 flex justify-between">
                        <BackButton>{{ User.LANGUAGE.DATA.ACTIONS.CANCEL }}</BackButton> <!-- Cancel button -->
                        <button id="btn-validate" v-on:click="onValidate" class="whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700">
                            {{ action }} <!-- Validate button -->
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import BackButton from "../components/BackButton.vue";
import API from "../script/API";
import { redirectHome } from "../script/common";

/**
 * Returns a URL parameter value corresponding to the given name.
 * @param {string} name - The name of the parameter to get.
 * @returns {string} The value of the parameter.
 */
function getURLParameter(name) {
    if (window.location.search == "") return null;
    let res = null;
    window.location.search.replace("?", "").split("&").forEach(param => {
        const parts = param.split("=");
        if (parts[0].trim().toLowerCase() == name.toLowerCase())
            res = decodeURIComponent(parts[1]);
    })
    return res;
}

// password reset token given to the user (usually retreived from the url using getURLParameter)
let token = null;
/**
 * Retreives the token in the URL and creates the keydown listener for the enter key,
 * to emulate a validate button click
 */
function setup() {
    token = getURLParameter("token");
    if (token == null) {
        redirectHome();
        return;
    }

    window.addEventListener("keydown", ev => {
        if (ev.key != "Enter") return;
        const btn = document.getElementById("btn-validate");
        if (btn) btn.click();
    });
}

/**
 * Displays a log message to the user
 * @param {string} msg The message to display.
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
 * Listener for the validate button click
 * Validates the new password and password confirm fields,
 * and makes an API call to reset the password.
 * if successful, redirects to the home page.
 */
function onValidate() {
    const btn = document.getElementById("btn-validate");
    btn.innerHTML = "...";

    const credentials = {
        newPassword: document.querySelector("input[name='new-password']"),
        passwordConfirm: document.querySelector("input[name='password-confirm']")
    };

    if (credentials.newPassword.value.trim().length < 8) {
        logMessage("Veuillez renseigner un mot de passe d'au moins 8 caractères.");
        credentials.newPassword.focus();
        return;
    }
    if (credentials.newPassword.value != credentials.passwordConfirm.value) {
        logMessage("Les deux mots de passe ne correspondent pas.");
        credentials.passwordConfirm.focus();
        return;
    }

    if (token == null) return;
    API.execute(API.ROUTE.RESET, API.METHOD_POST, {token: token, password: credentials.newPassword.value}, API.TYPE_JSON).then(data => {
        if (data.error) logMessage(data.error);
        else {
            logMessage("Votre mot de passe a été réinitialisé.");
            redirectHome();
        }
    }).catch(err => {
        btn.innerHTML = "Valider";
        switch (err.status) {
            case 401:
                logMessage("Token de réinitialisation invalide.");
                break;
            case 422:
                res.json().then(logMessage);
                break;
        
            default:
                logMessage("Erreur lors de la connexion au serveur");
                break;
        }
    });
}

let action = window.location.pathname.split("/").pop() === "reset" ? User.LANGUAGE.DATA.ACTIONS.RESET : User.LANGUAGE.DATA.ACTIONS.CHANGE;

export default {
    name: "Reset",
    components: {
        BackButton
    },
    data() { return {action, User} },
    mounted() {
        setup();
    },
    methods: {onValidate}
};
</script>