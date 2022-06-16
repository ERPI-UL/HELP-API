<template>
    <!-- Forget password page, used to receive an email when the user's password is lost -->
    <div class="relative flex p-4 md:p-8 min-h-screen flex-col justify-center">
        <div class="bg-white p-4 md:p-8 shadow-xl mx-auto rounded-lg">
            <div class="mx-auto max-w-md">
                <!-- Modal title -->
                <div class="flex center">
                    <img src="../assets/images/logo_indigo.png" class="hidden md:block h-10" alt="Tailwind Play" />
                    <h2 class="text-2xl leading-9 font-extrabold text-indigo-600 px-6 whitespace-nowrap">
                        {{ User.LANGUAGE.DATA.FORGOTPASSWORD.MESSAGES.FORGOT_PASSWORD }}
                    </h2>
                </div>
                <!-- Modal information text -->
                <p class="text-gray-600">{{ User.LANGUAGE.DATA.FORGOTPASSWORD.MESSAGES.DESCRIPTION }}</p>
                <div class="divide-y divide-gray-300/50">
                    <div class="space-y-6 py-8 text-base leading-7 text-gray-400">
                        <!-- Username or email input zone -->
                        <div class="block justify-between">
                            <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">{{ User.LANGUAGE.DATA.COMMON.USERNAME + " " + User.LANGUAGE.DATA.COMMON.OR.toLowerCase() + " " + User.LANGUAGE.DATA.COMMON.EMAIL }}: </p>
                            <input type="email" id="input-username-email" name="email" class="size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
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
                            {{ User.LANGUAGE.DATA.ACTIONS.VALIDATE }} <!-- Validate button -->
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
 * Creates a keydown event listener for enter press (if so emulated a validate button click)
 */
function setup() {
    window.addEventListener("keydown", ev => {
        if (ev.key != "Enter") return;
        const btn = document.getElementById("btn-validate");
        if (btn) btn.click();
    });
}

/**
 * Shows a log message to the user
 * @param {string} msg message to display
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
 * When the user clicks on the validate button
 * checks if the user entered an email or a username
 * and if so makes an API call to send an email to the user
 */
function onValidate() {
    const input = document.getElementById("input-username-email");
    if (input.value.trim() == "") {
        logMessage(User.LANGUAGE.DATA.FORGOTPASSWORD.LOGS.SPECIFY_USERNAME_EMAIL);
        input.focus();
        return;
    }
    API.execute(API.ROUTE.RESET+input.value, API.METHOD_GET).then(res => {
        logMessage(res.message);
        redirectHome();
    }).catch(err => {
        switch (err.status) {
            case 404:
                logMessage(User.LANGUAGE.DATA.FORGOTPASSWORD.LOGS.INCORRECT_USERNAME_EMAIL);
                break;
            default:
                logMessage(User.LANGUAGE.DATA.REGISTER.LOGS.SERVER_ERROR);
                break;
        }
    });
}

export default {
    name: "Login",
    components: {
        BackButton
    },
    data() { return {User}; },
    mounted() {
        setup();
    },
    methods: {onValidate}
};
</script>