<template>
    <div class="min-h-screen flex flex-col bg-black">
        <div class="p-2">
            <Topbar class="bg-gray-800"></Topbar>
        </div>
        <div class="flex bg-gray-800 m-4 shadow-lg rounded-lg p-2 grow">
            
        </div>
    </div>
</template>

<script>
import Topbar from "../components/Topbar.vue";
import User from "../script/User";

export default {
    name: "Admin",
    components: {
        Topbar
    },
    setup() {
        return {User}
    },
    mounted() {
        if (!User.currentUser.isAdmin()) window.location.href = "/";
    },
    methods: {}
};
</script>
