<template>
    <div v-on:click="toogleFullscreen" class="slide-in bg-white rounded-lg shadow-lg p-2 relative w-fit h-fit m-4 hover:shadow-xl">
        <h2 class="text-center font-bold">{{title}}</h2>
        <canvas id="chart-render"></canvas>
    </div>
</template>

<script>
import Chart from "chart.js/auto";

function setChart(div, infos) {
    const chart = new Chart(div, infos);
}

export default {
    name: "Chart",
    props: ["title", "chartInfos"],
    data: () => {return {}},
    components: {},
    mounted: function() {
        setChart(this.$el.childNodes[1], this.chartInfos);
    },
    methods: {
        
    }
}
</script>
