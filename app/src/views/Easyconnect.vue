<template>
    <div class="relative flex p-8 min-h-screen flex-col justify-center">
        <div class="bg-white p-4 md:p-8 shadow-xl mx-auto rounded-lg">
            <div class="mx-auto max-w-md">
                <div class="flex center">
                    <img src="../assets/images/icons/logo_indigo.png" class="hidden md:block h-10" alt="Tailwind Play" />
                    <h2 class="text-2xl leading-9 font-extrabold text-indigo-600 px-6 whitespace-wrap md:whitespace-nowrap">
                        Connecter un appareil
                    </h2>
                </div>
                <form action="/api/login" method="post">
                    <div class="divide-y divide-gray-300/50">
                        <div v-if="!user.connected" class="space-y-6 py-8 text-base leading-7 text-gray-400">
                            <div class="md:flex block justify-between">
                                <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">Nom d'utilisateur: </p>
                                <input type="text" name="username" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                            </div>
                            <div class="md:flex block justify-between">
                                <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2">Mot de passe: </p>
                                <input type="password" name="password" class="md:size-to-parent whitespace-nowrap inline-flex px-4 py-2 border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                            </div>
                        </div>
                        <div class="space-y-6 py-8 text-base leading-7 text-gray-400">
                            <div class="md:flex block justify-between">
                                <p class="whitespace-nowrap center font-medium text-gray-500 p-2 mr-2 text-center">Code appareil: </p>
                                <div class="flex justify-center">
                                    <input type="number" name="number1" class="input-numbers whitespace-nowrap inline-flex max-w-[32px] text-center p-1 mx-1 center border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                    <input type="number" name="number2" class="input-numbers whitespace-nowrap inline-flex max-w-[32px] text-center p-1 mx-1 center border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                    <input type="number" name="number3" class="input-numbers whitespace-nowrap inline-flex max-w-[32px] text-center p-1 mx-1 center border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                    <input type="number" name="number4" class="input-numbers whitespace-nowrap inline-flex max-w-[32px] text-center p-1 mx-1 center border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                    <input type="number" name="number5" class="input-numbers whitespace-nowrap inline-flex max-w-[32px] text-center p-1 mx-1 center border-gray-200 rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
                                </div>
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

const setupInputs = () => {
    const inputs = document.querySelectorAll(".input-numbers");
    for (let i = 0; i < inputs.length; i++) {
        const el = inputs.item(i);
        el.addEventListener("keydown", ev => {
            const char = ev.key.charAt(0);
            if (char < '0' || char > '9') {
                el.value = "";
            } else {
                el.value = char;
                if (i < inputs.length - 1) {
                    inputs.item(i + 1).focus();
                } else el.blur();
            }
            if (ev.key == "Backspace" && i > 0) {
                inputs.item(i - 1).focus();
            }
            ev.preventDefault();
        });
    }
}

export default {
    name: "Easyconnect",
    components: {
        Backbutton
    },
    setup() {
        return {user: JSON.parse(localStorage.getItem('user')??"{}")};
    },
    mounted: [
        setupInputs
    ]
    
};
</script>