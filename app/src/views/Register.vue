<template>
    <!-- Register web page -->
    <div class="flex min-h-screen p-4 md:p-8 flex-col justify-center">
        <div class="bg-white p-4 md:p-8 shadow-xl mx-auto rounded-lg">
            <div class="max-h-full">
                <div class="flex center">
                    <!-- Modal Title -->
                    <img src="../assets/images/logo_indigo.png" class="hidden md:block h-10" alt="Tailwind Play" />
                    <h2 class="text-2xl font-extrabold text-indigo-600 px-6">
                        {{ User.LANGUAGE.DATA.ACTIONS.REGISTER }}
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
                            <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">{{ User.LANGUAGE.DATA.COMMON.USERNAME }}: </p>
                            <input type="text" id="username" name="username" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                        </div>
                        <!-- Email input -->
                        <div class="md:flex block justify-between">
                            <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">{{ User.LANGUAGE.DATA.COMMON.EMAIL }}: </p>
                            <input type="email" id="email" name="email" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                        </div>
                        <!-- Password input -->
                        <div class="md:flex block justify-between">
                            <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">{{ User.LANGUAGE.DATA.COMMON.PASSWORD }}: </p>
                            <input type="password" id="new-password" name="new-password" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                        </div>
                        <!-- Password confirmation input -->
                        <div class="md:flex block justify-between">
                            <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">{{ User.LANGUAGE.DATA.REGISTER.MESSAGES.CONFIRM_PASSWORD }}: </p>
                            <input type="password" id="password-confirm" name="password-confirm" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                        </div>
                    </div>
                    <!-- Message log zone -->
                    <div id="log-zone" class="border-none overflow-y-hidden h-[0px]">
                        <p class="opacity-0 text-center text-indigo-600"></p>
                    </div>
                    <!-- Buttons -->
                    <div class="pt-8 flex justify-between">
                        <Backbutton>{{ User.LANGUAGE.DATA.ACTIONS.CANCEL }}</Backbutton> <!-- Cancel button -->
                        <ValidateButton id="btn-validate" v-on:click="register">{{ User.LANGUAGE.DATA.ACTIONS.REGISTER }}</ValidateButton> <!-- Validate button -->
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
}

/**
 * Displays a log message to the user
 * @param {string} msg message to display
 */
function logMessage(msg) {
    const btn = document.getElementById("btn-validate");
    btn.innerHTML = "S'inscrire";
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
        logMessage(User.LANGUAGE.DATA.REGISTER.LOGS.SPECIFY_FIRSTNAME);
        credentials.givenName.focus();
        return;
    }
    if (credentials.familyName.value.trim() == "") {
        logMessage(User.LANGUAGE.DATA.REGISTER.LOGS.SPECIFY_LASTNAME);
        credentials.familyName.focus();
        return;
    }
    if (credentials.username.value.trim() == "") {
        logMessage(User.LANGUAGE.DATA.REGISTER.LOGS.SPECIFY_USERNAME);
        credentials.username.focus();
        return;
    }
    const REGEX_EMAIL = /(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/;
    if (!credentials.email.value.trim().match(REGEX_EMAIL)) {
        logMessage(User.LANGUAGE.DATA.REGISTER.LOGS.SPECIFY_EMAIL);
        credentials.email.focus();
        return;
    }
    if (credentials.newPassword.value.trim().length < 8) {
        logMessage(User.LANGUAGE.DATA.REGISTER.LOGS.SPECIFY_PASSWORD);
        credentials.newPassword.focus();
        return;
    }
    if (credentials.newPassword.value != credentials.passwordConfirm.value) {
        logMessage(User.LANGUAGE.DATA.REGISTER.LOGS.SPECIFY_CONFIRM_PASSWORD);
        credentials.passwordConfirm.focus();
        return;
    }

    API.execute(API.ROUTE.USERS, API.METHOD_POST, {
        username: credentials.username.value.trim(),
        email: credentials.email.value.trim(),
        firstname: credentials.givenName.value.trim(),
        lastname: credentials.familyName.value.trim(),
        password_hash: credentials.newPassword.value.trim()
    }, API.TYPE_JSON).then(() => {
        logMessage(User.LANGUAGE.DATA.REGISTER.LOGS.CREATION_SUCCESS);
        btn.innerHTML = User.LANGUAGE.DATA.ACTIONS.REGISTER;
        redirectHome();
    }).catch(err => {
        console.error("Register error: ", err);
        logMessage(User.LANGUAGE.DATA.REGISTER.LOGS.CREATION_ERROR);
        btn.innerHTML = User.LANGUAGE.DATA.ACTIONS.REGISTER;
    });
}

export default {
    name: "Register",
    components: {
        Backbutton,
        ValidateButton
    },
    data() { return {User}; },
    mounted() {
        setup();
    },
    methods: {register}
};
</script>