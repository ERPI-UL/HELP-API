<template>
    <div class="flex flex-col h-screen">
        <div class="p-2">
            <Topbar></Topbar>
        </div>
        <div class="flex grow m-2">
            <div class="flex m-auto 300 p-4 rounded-lg shadow-lg bg-white">
                <div>
                    <img class="max-h-[30vh] w-auto" src="../assets/images/icons/icon_full.png" alt="" />
                </div>
                <div class="w-[30vw] p-4">
                    <h1 class="text-gray-600 text-2xl font-bold text-center">Indico - Interface Web</h1>
                    <br>
                    <p class="text-gray-500 text-lg text-center">Bienvenue sur l'interface web de l'application <span class="text-indigo-600">Indico</span> !</p>
                    <p class="text-gray-500 text-lg text-center">
                        Pour accéder à toutes les fonctionnalités,
                        <a class="text-indigo-600 hover:underline cursor-pointer" href="/login">connectez-vous</a>
                        à l'application, ou
                        <a class="text-indigo-600 hover:underline cursor-pointer" href="/register">créez un compte</a>
                        .
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Topbar from "../components/Topbar.vue";

export default {
    name: "Home",
    components: {
        Topbar
    },
};
</script>


<style>
</style>