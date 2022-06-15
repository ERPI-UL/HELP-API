<template>
    <!-- Home page, with topbar and a little window with some basic introduction text -->
    <div class="flex flex-col h-screen">
        <div class="p-2">
            <Topbar></Topbar>
        </div>
        <div class="flex flex-wrap space-y-6 m-4">
            <div class="flex m-4 p-2 bg-white rounded-lg shadow-lg border border-gray-200 m-auto">
                <img class="max-h-[20vw] md:max-h-[10vh] m-auto" src="../assets/images/icon_full.png" alt="" />
                <p class="text-xl font-semibold text-gray-600 my-auto mx-4">Indico - version 0.1.0</p>
            </div>
            <div class="flex flex-col m-4 p-2 bg-white rounded-lg shadow-lg border border-gray-200 m-auto">
                <img class="w-80 mx-auto" src="../assets/images/grand_est.png" alt="" />
                <p class="text-xl font-semibold text-gray-600 my-auto md:mx-4 mx-0 text-center">Avec le soutien fiancier de la Région Grand Est</p>
            </div>
        </div>
    </div>
</template>

<script>
import API from "../script/API";
import Topbar from "../components/Topbar.vue";

function setup() {
    
}

export default {
    name: "About",
    components: {
        Topbar
    },
    data() {
        return {}
    },
    mounted() {
        setup();
    }
};
</script>


<style>
</style>