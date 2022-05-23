<template>
    <div class="min-h-screen flex flex-col px-2">
        <div class="py-2">
            <Topbar></Topbar>
        </div>
        <div class="flex flex-col grow bg-white my-8 rounded-lg shadow-lg w-fit px-4 mx-auto divide-y max-w-full">
            <div class="flex justify-between">
                <h3 class="font-bold md:text-2xl text-xl text-gray-500 m-4 text-left">Mon profile</h3>
            </div>
            <div class="flex flex-col grow">
                <div class="flex flex-col h-full">
                    <div id="profile" class="p-4 flex justify-center">
                        <div id="main" class="flex mx-8">
                            <component :is="icon.user" class="flex-shrink-0 h-12 text-indigo-600 rounded-xl border border-indigo-600 border-4" aria-hidden="true" />
                            <h2 class="text-indigo-600 font-bold text-2xl my-2 mx-8">{{User.currentUser.username}}</h2>
                        </div>
                    </div>
                    <div class="flex md:flex-row flex-col justify-between m-2 max-w-full">
                        <p class="text-gray-500 font-base md:text-lg text-md p-2 mr-8">Nom d'utilisateur: </p>
                        <input disabled="disabled" type="text" id="input-username" name="username" :value="User.currentUser.username" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-100 rounded-md shadow-sm text-base font-medium text-gray-500 bg-gray-50">
                    </div>
                    <div class="flex md:flex-row flex-col justify-between m-2 max-w-full">
                        <p class="text-gray-500 font-base md:text-lg text-md p-2 mr-8">Prénom: </p>
                        <input type="text" id="input-firstname" name="given-name" :value="User.currentUser.firstname" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                    </div>
                    <div class="flex md:flex-row flex-col justify-between m-2 max-w-full">
                        <p class="text-gray-500 font-base md:text-lg text-md p-2 mr-8">Nom: </p>
                        <input type="text" id="input-lastname" name="family-name" :value="User.currentUser.lastname" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                    </div>
                    <div class="flex md:flex-row flex-col justify-between m-2 max-w-full">
                        <p class="text-gray-500 font-base md:text-lg text-md p-2 mr-8">Email: </p>
                        <input type="text" id="input-email" :value="User.currentUser.email" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                    </div>
                </div>
                <div class="flex justify-between h-fit pt-2 pb-4">
                    <DangerousButton id="delete-btn" v-on:click="removeAccount">Supprimer</DangerousButton>
                    <ValidateButton v-on:click="onAccountSave">
                        Mettre à jour
                    </ValidateButton>
                </div>
                <ValidatePopup ref="delete-popup"></ValidatePopup>
            </div>
            <div>
                <div class="flex flex-col grow h-full">
                    <p class="text-gray-600 font-base text-base p-2 mr-8">Modifier le mot de passe:</p>
                    <div class="flex md:flex-row flex-col justify-between m-2 max-w-full">
                        <p class="text-gray-500 font-base md:text-lg text-md p-2 mr-8">Ancien Mot de passe : </p>
                        <input type="password" id="input-oldpassword" name="old-password" value="" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                    </div>
                    <div class="flex md:flex-row flex-col justify-between m-2 max-w-full">
                        <p class="text-gray-500 font-base md:text-lg text-md p-2 mr-8">Nouveau Mot de passe : </p>
                        <input type="password" id="input-newpassword" name="new-password" value="" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                    </div>
                    <div class="flex md:flex-row flex-col justify-between m-2 max-w-full">
                        <p class="text-gray-500 font-base md:text-lg text-md p-2 mr-8">Confirmez le mot de passe: </p>
                        <input type="password" id="input-confirm" name="password-confirm" value="" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                    </div>
                </div>
                <div class="flex grow justify-between h-fit pt-2 pb-4">
                    <Backbutton>Retour</Backbutton>
                    <ValidateButton v-on:click="onMDPChange">
                        Mettre à jour
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

function onAccountSave(ev) {
    const updateBtn = ev.target;
    updateBtn.innerHTML = "...";
    const infos = {
        firstname: document.getElementById("input-firstname"),
        lastname: document.getElementById("input-lastname"),
        email: document.getElementById("input-email")
    }
    API.execute_logged(API.ROUTE.USER, API.METHOD_PUT, User.currentUser.getCredentials(), {
        firstname: infos.firstname.value,
        lastname: infos.lastname.value,
        email: infos.email.value
    }, API.TYPE_JSON).then(data => {
        infos.firstname.value = data.firstname;
        infos.lastname.value = data.lastname;
        infos.email.value = data.email;
        User.currentUser.firstname = data.firstname;
        User.currentUser.lastname = data.lastname;
        User.currentUser.email = data.email;
        User.saveUser();
        updateBtn.innerHTML = "Mettre à jour";
    }).catch(err => {
        console.log(err);
        updateBtn.innerHTML = "Mettre à jour";
        switch (err.status) {
            default:
                break;
        }
    });
}

function onMDPChange(ev) {
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
        console.log(data);
        updateBtn.innerHTML = "Mettre à jour";
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
    methods: {onAccountSave, onMDPChange, removeAccount}
};
</script>

<style>
</style>