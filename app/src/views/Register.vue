<template>
    <div class="flex min-h-screen p-4 md:p-8 flex-col justify-center">
        <div class="bg-white p-4 md:p-8 shadow-xl mx-auto rounded-lg">
            <div class="max-h-full">
                <div class="flex center">
                    <img src="../assets/images/icons/logo_indigo.png" class="hidden md:block h-10" alt="Tailwind Play" />
                    <h2 class="text-2xl leading-9 font-extrabold text-indigo-600 px-6">
                        S'inscrire
                    </h2>
                </div>
                <div>
                    <div class="space-y-1 md:space-y-4 py-8 text-base leading-7 text-gray-400 max-h-full">
                        <div class="md:flex block justify-between">
                            <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">Prénom: </p>
                            <input type="text" id="given-name" name="given-name" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                        </div>
                        <div class="md:flex block justify-between">
                            <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">Nom: </p>
                            <input type="text" id="family-name" name="family-name" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                        </div>
                        <div class="md:flex block justify-between">
                            <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">Nom d'utilisateur: </p>
                            <input type="text" id="username" name="username" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                        </div>
                        <div class="md:flex block justify-between">
                            <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">Adresse mail: </p>
                            <input type="text" id="email" name="email" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                        </div>
                        <div class="md:flex block justify-between">
                            <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">Mot de passe: </p>
                            <input type="password" id="new-password" name="new-password" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                        </div>
                        <div class="md:flex block justify-between">
                            <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">Confirmez le mot de passe: </p>
                            <input type="password" id="password-confirm" name="password-confirm" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                        </div>
                    </div>
                    <div id="log-zone" class="border-none overflow-y-hidden h-[0px]">
                        <p class="opacity-0 text-center text-indigo-600">Message</p>
                    </div>
                    <div class="pt-8 flex justify-between">
                        <Backbutton>Annuler</Backbutton>
                        <ValidateButton id="btn-validate" v-on:click="register">S'inscrire</ValidateButton>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Backbutton from "../components/Backbutton.vue";
import ValidateButton from "../components/ValidateButton.vue";
import API from "../script/API";

function setup() {
    window.addEventListener("keydown", ev => {
        if (ev.key != "Enter") return;
        const btn = document.getElementById("btn-validate");
        if (btn) btn.click();
    });
}

let logTimeout = -1;
function logMessage(msg) {
    const btn = document.getElementById("btn-validate");
    btn.innerHTML = "S'inscrire";

    const div = document.getElementById("log-zone");
    const txt = div.firstElementChild;
    txt.innerHTML = msg;
    txt.classList.add("opacity-100");
    div.style.height = txt.getBoundingClientRect().height+"px";
    if (logTimeout != -1) clearTimeout(logTimeout);
    logTimeout = setTimeout(() => {
        txt.classList.remove("opacity-100");
        div.style.height = "0px";
        logTimeout = -1;
    }, 3000);
}

function register() {
    const btn = document.getElementById("btn-validate");
    btn.innerHTML = "..."
    const credentials = {
        givenName: document.getElementById("given-name"),
        familyName: document.getElementById("family-name"),
        username: document.getElementById("username"),
        email: document.getElementById("email"),
        newPassword: document.getElementById("new-password"),
        passwordConfirm: document.getElementById("password-confirm")
    };
    if (credentials.givenName.value.trim() == "") {
        logMessage("Veuillez renseigner un prénom.");
        credentials.givenName.focus();
        return;
    }
    if (credentials.familyName.value.trim() == "") {
        logMessage("Veuillez renseigner un nom de famille.");
        credentials.familyName.focus();
        return;
    }
    if (credentials.username.value.trim() == "") {
        logMessage("Veuillez renseigner un nom d'utilisateur.");
        credentials.username.focus();
        return;
    }
    const REGEX_EMAIL = /(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/;
    if (!credentials.email.value.trim().match(REGEX_EMAIL)) {
        logMessage("Veuillez renseigner une adresse mail valide.");
        credentials.email.focus();
        return;
    }
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

    API.execute("/users", "POST", {
        username: credentials.username.value.trim(),
        email: credentials.email.value.trim(),
        firstname: credentials.givenName.value.trim(),
        lastname: credentials.familyName.value.trim(),
        password: credentials.newPassword.value.trim()
    }).then(() => {
        logMessage("Compte créé avec succès.");
        btn.innerHTML = "S'inscrire";
        setTimeout(window.history.back, 1000);
    }).catch(err => {
        logMessage("Erreur lors de la création du compte.");
        btn.innerHTML = "S'inscrire";
    });
}

export default {
    name: "Register",
    components: {
        Backbutton,
        ValidateButton
    },
    mounted() {
        setup();
    },
    methods: {register}
};
</script>