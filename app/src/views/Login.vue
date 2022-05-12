<template>
    <div class="relative flex p-4 md:p-8 min-h-screen flex-col justify-center">
        <div class="bg-white p-4 md:p-8 shadow-xl mx-auto rounded-lg">
            <div class="mx-auto max-w-md">
                <div class="flex center">
                    <img src="../assets/images/icons/logo_indigo.png" class="hidden md:block h-10" alt="Tailwind Play" />
                    <h2 class="text-2xl leading-9 font-extrabold text-indigo-600 px-6 whitespace-nowrap">
                        Se connecter
                    </h2>
                </div>
                <!-- <form action="/api/login" method="post"> -->
                    <div class="divide-y divide-gray-300/50">
                        <div class="space-y-6 py-8 text-base leading-7 text-gray-400">
                            <div class="md:flex block justify-between">
                                <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">Nom d'utilisateur: </p>
                                <input type="text" id="input-username" name="username" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                            </div>
                            <div class="md:flex block justify-between">
                                <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">Mot de passe: </p>
                                <input type="password" id="input-password" name="password" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                            </div>
                        </div>
                        <div id="log-zone" class="border-none overflow-y-hidden h-[0px]">
                            <p class="opacity-0 text-center text-indigo-600">Message</p>
                        </div>
                        <div class="pt-8 flex justify-between">
                            <BackButton>Annuler</BackButton>
                            <button id="btn-validate" v-on:click="onValidate" class="whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700">
                                Valider
                            </button>
                        </div>
                    </div>
                <!-- </form> -->
            </div>
        </div>
    </div>
</template>

<script>
import BackButton from "../components/BackButton.vue";
import User from "../script/User";
import API from "../script/API";
import { redirectHome } from "../script/common";

function setup() {
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

    let debugMode = false;
    if (debugMode) {/// DEBUG /// Should be a GET request to API
        let user = new User(
            credentials.username.value,
            credentials.password.value,
            "", "", "", "", 0
        );
        if (User.sameCredentials(user, User.USER_ADMIN)) user = User.USER_ADMIN;
        if (User.sameCredentials(user, User.USER_TEACHER)) user = User.USER_TEACHER;
        if (User.sameCredentials(user, User.USER_LEARNER)) user = User.USER_LEARNER;
        if (user.token == "") { // error: not a admin/teacher/learner account
            logMessage("Identifiant ou mot de passe incorrect");
            document.querySelector("input[name=username]").focus();
            return;
        }
        localStorage.setItem("user", User.toJSON(user));
        btn.innerHTML = "Valider";
        window.history.back();
        return;
    } /// DEBUG ///

    //// REAL ///
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
    //// REAL ///

}

export default {
    name: "Login",
    components: {
        BackButton
    },
    mounted() {
        setup();
    },
    methods: {onValidate}
};
</script>