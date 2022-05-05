<template>
    <div class="relative flex p-8 min-h-screen flex-col justify-center">
        <div class="bg-white p-4 md:p-8 shadow-xl mx-auto rounded-lg">
            <div class="mx-auto max-w-md">
                <div class="flex center">
                    <img src="../assets/images/icons/logo_indigo.png" class="hidden md:block h-10" alt="Tailwind Play" />
                    <h2 class="text-2xl leading-9 font-extrabold text-indigo-600 px-6 whitespace-nowrap">
                        Se connecter
                    </h2>
                </div>
                <form action="/api/login" method="post">
                    <div class="divide-y divide-gray-300/50">
                        <div class="space-y-6 py-8 text-base leading-7 text-gray-400">
                            <div class="md:flex block justify-between">
                                <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">Nom d'utilisateur: </p>
                                <input type="text" name="username" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                            </div>
                            <div class="md:flex block justify-between">
                                <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">Mot de passe: </p>
                                <input type="password" name="password" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                            </div>
                        </div>
                        <div class="pt-8 flex justify-between">
                            <Backbutton>Annuler</Backbutton>
                            <input type="submit"
                                class="whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700"
                                value="Valider"
                                href="/"
                            />
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import Backbutton from "../components/Backbutton.vue";

export default {
    name: "Login",
    components: {
        Backbutton
    }
};
</script>