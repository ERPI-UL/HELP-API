<template>
    <!-- Profile page, to see and edit profile informations -->
    <div class="min-h-screen flex flex-col px-2">
        <div class="py-2"> <!-- Header -->
            <Topbar></Topbar>
        </div>
        <div class="flex flex-col grow bg-white my-8 rounded-lg shadow-lg w-fit px-4 mx-auto divide-y max-w-full">
            <!-- Title -->
            <div class="flex justify-between">
                <h3 class="font-bold md:text-2xl text-xl text-gray-500 m-4 text-left">{{User.LANGUAGE.DATA.PROFILE.TITLE}}</h3>
            </div>
            <div class="flex flex-col grow">
                <div class="flex flex-col h-full">
                    <div id="profile" class="p-4 flex justify-center">
                        <!-- User name header zone -->
                        <div id="main" class="flex mx-8">
                            <component :is="icon.user" class="flex-shrink-0 h-12 text-indigo-600 rounded-xl border border-indigo-600 border-4" aria-hidden="true" />
                            <h2 class="text-indigo-600 font-bold text-2xl my-2 mx-8">{{User.currentUser.username}}</h2>
                        </div>
                    </div>
                    <!-- Language input zone -->
                    <div class="flex md:flex-row flex-col justify-between m-2 max-w-full">
                        <p class="text-gray-500 font-base md:text-lg text-md p-2 mr-8">{{User.LANGUAGE.DATA.COMMON.LANGUAGE}}: </p>
                        <select name="language" id="input-language" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100 pr-10">
                            <option v-for="language in User.AVAILABLE_LANGUAGES" :value="language.CODE">{{language.NAME+" "+language.FLAG}}</option>
                        </select>
                    </div>
                    <!-- Username input zone -->
                    <div class="flex md:flex-row flex-col justify-between m-2 max-w-full">
                        <p class="text-gray-500 font-base md:text-lg text-md p-2 mr-8">{{User.LANGUAGE.DATA.COMMON.USERNAME}}: </p>
                        <input type="text" id="input-username" name="username" :value="User.currentUser.username" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                    </div>
                    <!-- Firstname input zone -->
                    <div class="flex md:flex-row flex-col justify-between m-2 max-w-full">
                        <p class="text-gray-500 font-base md:text-lg text-md p-2 mr-8">{{User.LANGUAGE.DATA.COMMON.FIRSTNAME}}: </p>
                        <input type="text" id="input-firstname" name="given-name" :value="User.currentUser.firstname" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                    </div>
                    <!-- Name input zone -->
                    <div class="flex md:flex-row flex-col justify-between m-2 max-w-full">
                        <p class="text-gray-500 font-base md:text-lg text-md p-2 mr-8">{{User.LANGUAGE.DATA.COMMON.LASTNAME}}: </p>
                        <input type="text" id="input-lastname" name="family-name" :value="User.currentUser.lastname" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                    </div>
                    <!-- Email input zone -->
                    <div class="flex md:flex-row flex-col justify-between m-2 max-w-full">
                        <p class="text-gray-500 font-base md:text-lg text-md p-2 mr-8">{{User.LANGUAGE.DATA.COMMON.EMAIL}}: </p>
                        <input type="text" id="input-email" :value="User.currentUser.email" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                    </div>
                </div>
                <!-- Basic informations buttons -->
                <div class="flex justify-between h-fit pt-2 pb-4">
                    <DangerousButton id="delete-btn" v-on:click="removeAccount">{{User.LANGUAGE.DATA.ACTIONS.DELETE}}</DangerousButton> <!-- Remove user button -->
                    <ValidateButton v-on:click="() => onAccountSave(this)"> <!-- Update informations button -->
                        {{User.LANGUAGE.DATA.ACTIONS.UPDATE}}
                    </ValidateButton>
                </div>
                <ValidatePopup ref="delete-popup"></ValidatePopup> <!-- Delete user validation popup -->
            </div>
            <div>
                <!-- Password edition zone -->
                <div class="flex flex-col grow h-full">
                    <p class="text-gray-600 font-base text-base p-2 mr-8">{{ User.LANGUAGE.DATA.PROFILE.MESSAGES.MODIFY_PASSWORD }}:</p>
                    <!-- Old password -->
                    <div class="flex md:flex-row flex-col justify-between m-2 max-w-full">
                        <p class="text-gray-500 font-base md:text-lg text-md p-2 mr-8">{{ User.LANGUAGE.DATA.PROFILE.MESSAGES.OLD_PASSWORD }} : </p>
                        <input type="password" id="input-oldpassword" name="old-password" value="" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                    </div>
                    <!-- New password -->
                    <div class="flex md:flex-row flex-col justify-between m-2 max-w-full">
                        <p class="text-gray-500 font-base md:text-lg text-md p-2 mr-8">{{ User.LANGUAGE.DATA.PROFILE.MESSAGES.NEW_PASSWORD }} : </p>
                        <input type="password" id="input-newpassword" name="new-password" value="" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                    </div>
                    <!-- Password confirmation -->
                    <div class="flex md:flex-row flex-col justify-between m-2 max-w-full">
                        <p class="text-gray-500 font-base md:text-lg text-md p-2 mr-8">{{ User.LANGUAGE.DATA.REGISTER.MESSAGES.CONFIRM_PASSWORD }}: </p>
                        <input type="password" id="input-confirm" name="password-confirm" value="" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                    </div>
                </div>
                <!-- Password buttons -->
                <div class="flex grow justify-between h-fit pt-2 pb-4">
                    <Backbutton>{{ User.LANGUAGE.DATA.ACTIONS.CANCEL }}</Backbutton> <!-- Cancel button (go back in history) -->
                    <ValidateButton v-on:click="() => onMDPChange(this)"> <!-- Update user password (disconnects the user) -->
                        {{ User.LANGUAGE.DATA.ACTIONS.UPDATE }}
                    </ValidateButton>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Topbar from "../components/Topbar.vue";
import { UserIcon } from "@heroicons/vue/solid";
import User from "../script/User";
import Backbutton from "../components/BackButton.vue";
import ValidateButton from "../components/ValidateButton.vue";
import DangerousButton from "../components/DangerousButton.vue";
import ValidatePopup from "../components/ValidatePopup.vue";
import API from '../script/API';

/**
 * Removes the user's account from the database with an API call (also removes all his informations)
 * Spawn the validation popup to confirm deletion
 */
function removeAccount() {
    const el = this.$refs["delete-popup"];
    el.show("Supprimer mon compte", "Voulez-vous supprimer "+User.currentUser.username+" ?", "Annuler", "Supprimer");
    el.setPosition(document.getElementById("delete-btn"));
    el.setCallback(() => {
        API.execute_logged(API.ROUTE.USER, API.METHOD_DELETE, User.currentUser.getCredentials(), {}, API.TYPE_JSON).then(res => {
            User.forgetUser();
            window.location.href = "/";
        }).catch(console.error);
    });
}

/**
 * Event listener when the user save informations button is pressed
 * Makes en API call to update all the user's informations and redirects him to the home page
 */
function onAccountSave(ev) {
    const updateBtn = ev.target;
    updateBtn.innerHTML = "...";
    const infos = {
        firstname: document.getElementById("input-firstname"),
        lastname: document.getElementById("input-lastname"),
        username: document.getElementById("input-username"),
        email: document.getElementById("input-email")
    }
    API.execute_logged(API.ROUTE.USER, API.METHOD_PUT, User.currentUser.getCredentials(), {
        firstname: infos.firstname.value,
        lastname: infos.lastname.value,
        username: infos.username.value,
        email: infos.email.value,
    }, API.TYPE_JSON).then(data => {
        infos.firstname.value = data.firstname;
        infos.lastname.value = data.lastname;
        infos.email.value = data.email;
        User.currentUser.firstname = data.firstname;
        User.currentUser.lastname = data.lastname;
        User.currentUser.email = data.email;
        updateBtn.innerHTML = "Mettre à jour";
        User.saveUser();
        obj.$router.go(-1);
    }).catch(err => {
        console.log(err);
        updateBtn.innerHTML = "Mettre à jour";
        switch (err.status) {
            default:
                break;
        }
    });
}

/**
 * Event listener when the user save password button is pressed
 * Makes en API call to update the user's password and disconnects the user + goes back home
 */
function onMDPChange(obj, ev) {
    const updateBtn = ev.target;
    updateBtn.innerHTML = "...";
    const infos = {
        oldpassword: document.getElementById("input-oldpassword"),
        newpassword: document.getElementById("input-newpassword"),
        confirm: document.getElementById("input-confirm")
    };
    if (infos.newpassword.value !== infos.confirm.value) {
        updateBtn.innerHTML = "Mettre à jour";
        alert("Les mots de passe ne sont pas identiques");
        return;
    }
    API.execute(API.ROUTE.PASSWORD, API.METHOD_POST, {
        username: User.currentUser.username,
        old: infos.oldpassword.value,
        new: infos.newpassword.value
    }, API.TYPE_JSON).then(data => {
        updateBtn.innerHTML = "Mettre à jour";
        User.forgetUser();
        obj.$router.go(-1);
    }).catch(err => {
        console.log(err);
    });
}

export default {
    name: "Profile",
    components: {
        Topbar,
        Backbutton,
        ValidateButton,
        DangerousButton,
        ValidatePopup
    },
    setup() {
        if (!User.isConnected(User.currentUser)) {window.location.href = "/login";}
        return {icon: {user: UserIcon}, User};
    },
    mounted() {
        const langInput = document.getElementById("input-language");
        langInput.value = User.LANGUAGE.CODE;
        langInput.addEventListener("change", ev => {
            User.LoadLanguage(ev.target.value);
            this.$forceUpdate();
        });
    },
    methods: {onAccountSave, onMDPChange, removeAccount}
};
</script>

<style>
</style>