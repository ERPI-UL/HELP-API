<template>
    <div class="relative flex p-4 md:p-8 min-h-screen flex-col justify-center">
        <div class="bg-white p-4 md:p-8 shadow-xl mx-auto rounded-lg max-w-full">
            <div class="mx-auto max-w-md">
                <div class="flex center max-w-full">
                    <img src="../assets/images/icons/logo_indigo.png" class="hidden md:block h-10" alt="Tailwind Play" />
                    <h2 class="text-2xl leading-9 font-extrabold text-indigo-600 px-6">
                        Réinitialiser le mot de passe
                    </h2>
                </div>
                <div class="divide-y divide-gray-300/50">
                    <div class="space-y-6 py-8 text-base leading-7 text-gray-400">
                        <div class="md:flex block justify-between">
                            <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">Mot de passe: </p>
                            <input type="password" id="input-password" name="new-password" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                        </div>
                        <div class="md:flex block justify-between">
                            <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">Confirmez le mot de passe: </p>
                            <input type="password" id="input-password" name="password-confirm" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                        </div>
                    </div>
                    <div id="log-zone" class="border-none overflow-y-hidden h-[0px]">
                        <p class="opacity-0 text-center text-indigo-600"></p>
                    </div>
                    <div class="pt-8 flex justify-between">
                        <BackButton>Retour</BackButton>
                        <button id="btn-validate" v-on:click="onValidate" class="whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700">
                            Réinitialiser
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

function setup() {
    const token = getURLParameter("token");
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

    API.execute(API.ROUTE.RESET, API.METHOD_POST, {token: token, password: credentials.newPassword.value}, API.TYPE_JSON).then(data => {
        if (data.error) logMessage(data.error);
        else {
            logMessage("Votre mot de passe a été réinitialisé.");
            redirectHome();
        }
    }).catch(err => {
        btn.innerHTML = "Valider";
        switch (err.status) {
            case 404:
                logMessage("Token de réinitialisation invalide.");
                break;
        
            default:
                logMessage("Erreur lors de la connexion au serveur");
                break;
        }
    });

}

export default {
    name: "Reset",
    components: {
        BackButton
    },
    mounted() {
        setup();
    },
    methods: {onValidate}
};
</script>