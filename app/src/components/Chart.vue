<template>
    <!-- Template chart view : Used to display a graph to the user based on informations in the [charInfos] variable -->
    <div v-on:click="toogleFullscreen(this)" class="slide-in bg-white rounded-lg shadow-lg p-2 relative w-[20vw] min-h-[10vh] h-min max-w-full max-h-full m-4 scale-100 hover:shadow-xl hover:scale-105 cursor-pointer">
        <div class="flex flex-col min-h-0">
            <h2 class="text-center font-bold">{{title}}</h2>
            <canvas id="chart-render" class="flex grow-0 bg-white my-auto max-h-full min-h-[10vh]"></canvas>
        </div>
    </div>
</template>

<script>
import Chart from "chart.js/auto";

/**
 * Creates a chart inside the template (using Chart.JS)
 * and attaches the onclick event listener for fullscreen mode
 */
function setChart(el, div, infos) {
    const chart = new Chart(div, infos);
    div.parentNode.addEventListener("click", ev => {
        if (el.attrs.length > 0) ev.stopPropagation();
    })
}

/**
 * Toogle the fullscreen mode of the chart, modifying the chart's css to fit the screen's size for fullscreen mode
 * @param {HTMLElement} el
 */
function toogleFullscreen(el) {
    if (el.attrs.length == 0) {
        el.$el.classList.forEach(attr => el.attrs.push(attr));
        el.attrs.forEach(attr => el.$el.classList.remove(attr));
        el.$el.classList.add("fullscreen-parent");
        el.$el.childNodes[0].classList.add("fullscreen-child");
    } else {
        el.$el.classList.remove("fullscreen-parent");
        el.$el.childNodes[0].classList.remove("fullscreen-child");
        el.attrs.forEach(attr => el.$el.classList.add(attr));
        el.attrs = [];
    }
}

export default {
    name: "Chart",
    props: ["title", "chartInfos"],
    data: () => {return {}},
    components: {},
    mounted: function() {
        this.attrs = [];
        setChart(this, this.$el.childNodes[0].childNodes[1], this.chartInfos);
    },
    methods: {toogleFullscreen}
}
</script>

<style>
.fullscreen-child {
    background-color: white;
    position: absolute;
    top: 10vh;
    left: 15vw;
    width: 70vw;
    height: 80vh;
    cursor: auto;
    box-shadow: 0px 0px 80px #0005;
    border-radius: 1em;
    padding: 1em;
}
.fullscreen-parent {
    z-index: 99;
    animation: spawn-in 800ms ease;
    background-color: #0006;
    position: absolute;
    top: 0px;
    left: 0px;
    width: 100vw;
    height: 100vh;
}
</style>