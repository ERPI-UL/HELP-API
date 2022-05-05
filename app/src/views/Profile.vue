<template>
    <div class="min-h-screen flex flex-col">
        <div class="p-2">
            <Topbar></Topbar>
        </div>
        <div class="flex flex-col grow bg-white my-8 rounded-lg shadow-lg w-fit px-4 mx-auto divide-y">
            <div class="flex justify-between">
                <h3 class="font-bold text-2xl text-gray-500 m-4 text-left">Mon profile</h3>
            </div>
            <div class="flex flex-col grow">
                <div class="flex flex-col h-full">
                    <div id="profile" class="p-4 flex justify-center">
                        <div id="main" class="flex mx-8">
                            <component :is="icon.user" class="flex-shrink-0 h-12 text-indigo-600 rounded-xl border border-indigo-600 border-4" aria-hidden="true" />
                            <h2 class="text-indigo-600 font-bold text-2xl my-2 mx-8">{{user.username}}</h2>
                        </div>
                    </div>
                    <div class="flex justify-between m-2">
                        <p class="text-gray-500 font-base text-lg p-2 mr-8">Nom d'utilisateur: </p>
                        <input type="text" id="input-username" name="username" :value="user.username" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                    </div>
                    <div class="flex justify-between m-2">
                        <p class="text-gray-500 font-base text-lg p-2 mr-8">Nom: </p>
                        <input type="text" id="input-firstname" name="given-name" :value="user.firstname" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                    </div>
                    <div class="flex justify-between m-2">
                        <p class="text-gray-500 font-base text-lg p-2 mr-8">Prénom: </p>
                        <input type="text" id="input-lastname" name="family-name" :value="user.lastname" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                    </div>
                    <div class="flex justify-between m-2">
                        <p class="text-gray-500 font-base text-lg p-2 mr-8">Email: </p>
                        <input type="text" id="input-email" :value="user.email" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                    </div>
                </div>
                <div class="flex justify-between h-fit pt-2 pb-4">
                    <span></span>
                    <ValidateButton v-on:click="onAccountSave">
                        Modifier
                    </ValidateButton>
                </div>
            </div>
            <div>
                <div class="flex flex-col grow h-full">
                    <p class="text-gray-600 font-base text-base p-2 mr-8">Modifier le mot de passe:</p>
                    <div class="flex justify-between m-2">
                        <p class="text-gray-500 font-base text-lg p-2 mr-8">Mot de passe : </p>
                        <input type="password" id="input-password" name="new-password" value="" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                    </div>
                    <div class="flex justify-between m-2">
                        <p class="text-gray-500 font-base text-lg p-2 mr-8">Confirmez le mot de passe: </p>
                        <input type="password" id="input-confirm" name="password-confirm" value="" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                    </div>
                </div>
                <div class="flex grow justify-between h-fit pt-2 pb-4">
                    <Backbutton>Retour</Backbutton>
                    <ValidateButton v-on:click="onMDPChange">
                        Modifier
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
import Backbutton from "../components/Backbutton.vue";
import ValidateButton from "../components/ValidateButton.vue"

const user = User.fromJSON(localStorage.getItem("user"));

function onAccountSave(ev) {
    console.log(ev.target); // TODO
}

function onMDPChange(ev) {
    console.log(ev.target); // TODO
}

export default {
    name: "Profile",
    components: {
        Topbar,
        Backbutton,
        ValidateButton
    },
    setup() {
        if (!user.connected) {window.location.href = "/login";}
        return {icon: {user: UserIcon}, user: user};
    },
    methods: {onAccountSave, onMDPChange}
};
</script>

<style>
</style>