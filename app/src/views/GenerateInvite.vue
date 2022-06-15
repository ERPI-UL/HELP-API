<template>
    <!-- Register web page -->
    <div class="flex min-h-screen p-4 md:p-8 flex-col justify-center">
        <div class="bg-white p-4 md:p-8 shadow-xl mx-auto rounded-lg">
            <div class="max-h-full">
                <div class="flex center">
                    <!-- Modal Title -->
                    <img src="../assets/images/logo_indigo.png" class="hidden md:block h-10" alt="Tailwind Play" />
                    <h2 class="text-2xl font-extrabold text-indigo-600 px-6">
                        {{ User.LANGUAGE.DATA.INVITE.MESSAGES.GENERATE_INVITE }}
                    </h2>
                </div>
                <div>
                    <!-- Modal content, inputs to register -->
                    <div class="space-y-1 md:space-y-4 py-2 md:py-8 text-base text-gray-400 max-h-full">
                        <!-- Firstname input -->
                        <div class="md:flex block justify-between">
                            <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">{{ User.LANGUAGE.DATA.COMMON.FIRSTNAME }}: </p>
                            <input type="text" id="given-name" name="given-name" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                        </div>
                        <!-- Lastname input -->
                        <div class="md:flex block justify-between">
                            <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">{{ User.LANGUAGE.DATA.COMMON.LASTNAME }}: </p>
                            <input type="text" id="family-name" name="family-name" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                        </div>
                        <!-- Username input -->
                        <div class="md:flex block justify-between">
                            <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">{{ User.LANGUAGE.DATA.COMMON.USERNAME }} ({{ User.LANGUAGE.DATA.COMMON.OPTIONAL }}): </p>
                            <input type="text" id="username" name="username" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                        </div>
                        <!-- Email input -->
                        <div class="md:flex block justify-between">
                            <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">{{ User.LANGUAGE.DATA.COMMON.EMAIL }}: </p>
                            <input type="email" id="email" name="email" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                        </div>
                        <!-- Email input -->
                        <div class="md:flex block justify-between">
                            <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">{{ User.LANGUAGE.DATA.COMMON.ROLE }}:</p>
                            <select id="role-select" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black pr-8 bg-gray-50 hover:bg-gray-100">
                            
                            </select>
                        </div>
                    </div>
                    <!-- Message log zone -->
                    <div id="log-zone" class="border-none overflow-y-hidden h-[0px]">
                        <p class="opacity-0 text-center text-indigo-600"></p>
                    </div>
                    <p class="text-gray-400 pt-8">{{ User.LANGUAGE.DATA.INVITE.MESSAGES.VALIDATION_DELAY }}</p>
                    <!-- Buttons -->
                    <div class="pt-2 flex justify-between">
                        <Backbutton>{{ User.LANGUAGE.DATA.ACTIONS.CANCEL }}</Backbutton> <!-- Cancel button -->
                        <ValidateButton id="btn-validate" v-on:click="sendInvite">{{ User.LANGUAGE.DATA.ACTIONS.SEND }}</ValidateButton> <!-- Validate button -->
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Backbutton from "../components/BackButton.vue";
import ValidateButton from "../components/ValidateButton.vue";
import API from "../script/API";
import User from "../script/User";
import { redirectHome } from "../script/common";

/**
 * Registers the event listener for the enter key
 * if it's pressed, emulate a click on the validate button
 */
function setup() {
    window.addEventListener("keydown", ev => {
        if (ev.key != "Enter") return;
        const btn = document.getElementById("btn-validate");
        if (btn) btn.click();
    });

    const roleSelect = document.getElementById("role-select");
    const roles = [
        User.LANGUAGE.DATA.ROLES.VISITOR,
        User.LANGUAGE.DATA.ROLES.LEARNER,
        User.LANGUAGE.DATA.ROLES.TEACHER,
        User.LANGUAGE.DATA.ROLES.ADMIN
    ];
    for (let i = 1; i <= User.currentUser.permissions; i++) {
        const option = document.createElement("option");
        option.value = i;
        option.innerText = roles[i];
        roleSelect.appendChild(option);
    }
}

/**
 * Displays a log message to the user
 * @param {string} msg message to display
 */
function logMessage(msg) {
    const btn = document.getElementById("btn-validate");
    btn.innerHTML = "Envoyer l'invitation";
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
 * Event listener for when the validate button is clicked
 * Checks if all the fields are correctly filled and makes an API call
 * to try to register the User. If so, redirects to the home page
 */
function sendInvite() {
    const btn = document.getElementById("btn-validate");
    btn.innerHTML = "...";

    const credentials = {
        givenName: document.getElementById("given-name"),
        familyName: document.getElementById("family-name"),
        username: document.getElementById("username"),
        email: document.getElementById("email"),
        role: document.getElementById("role-select")
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
    const REGEX_EMAIL = /(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/;
    if (!credentials.email.value.trim().match(REGEX_EMAIL)) {
        logMessage("Veuillez renseigner une adresse mail valide.");
        credentials.email.focus();
        return;
    }

    API.execute_logged(API.ROUTE.INVITE, API.METHOD_POST, User.currentUser.getCredentials(), {
        email: credentials.email.value.trim(),
        firstname: credentials.givenName.value.trim(),
        lastname: credentials.familyName.value.trim(),
        username: credentials.username.value.trim(),
        adminLevel: credentials.role.value
    }, API.TYPE_JSON).then(() => {
        logMessage("Invitation envoyée avec succès.");
        btn.innerHTML = "Envoyer l'invitation";
        redirectHome();
    }).catch(err => {
        if (err.message.json) {
            err.message.json().then(e => {
                logMessage("Erreur : "+e.detail);
            });
        }
        else {
            console.error("Invite error: ", err);
            logMessage("Erreur lors de l'envoie de l'invitation.");
        }
        btn.innerHTML = "Envoyer l'invitation";
    });
}

export default {
    name: "GenerateInvite",
    components: {
        Backbutton,
        ValidateButton
    },
    data() { return {User}; },
    mounted() {
        setup();
    },
    methods: {sendInvite}
};
</script>