<template>
    <div v-on:click="toogleFullscreen" class="slide-in bg-white rounded-lg shadow-lg p-2 relative w-fit h-fit m-4 hover:shadow-xl hover:scale-105 cursor-pointer">
        <h2 class="text-left font-semibold text-gray-800 text-lg">{{ boxTitle }}</h2>
        <p class="text-center font-bold text-gray-600 text-xl px-8 py-2">{{ boxInfos }}</p>
    </div>
</template>

<script>

export default {
    name: "InfoBox",
    props: ["boxTitle", "boxInfos"],
    data: () => {return {}},
    components: {},
    mounted: function() {
        
    },
    methods: {
        
    }
}
</script>
