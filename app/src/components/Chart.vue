<template>
    <!-- Template chart view : Used to display a graph to the user based on informations in the [charInfos] variable -->
    <div ref="parent" v-on:click="toogleFullscreen(this);" class="slide-in bg-white rounded-lg shadow-lg p-2 relative w-[20vw] min-h-[10vh] h-min max-w-full max-h-full m-4 scale-100 hover:shadow-xl hover:scale-105 cursor-pointer">
        <div ref="child" class="flex flex-col min-h-0">
            <div id="quit-btn" class="hidden flex grow-0 justify-end">
                <button class="bg-red-600 p-0.5 h-fit w-fit flex flex-row shadow rounded">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 m-auto text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
            <h2 class="text-center font-bold">{{title}}</h2>
            <canvas id="chart-render" class="flex grow-0 bg-white my-auto max-h-full min-h-[10vh]" style="transition: none;"></canvas>
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
}

/**
 * Toogle the fullscreen mode of the chart,
 * modifying the chart's css to fit the screen's size for fullscreen mode
 */
function toogleFullscreen(el) {
    if (el.attrs.length == 0) {
        console.log("cas 1")
        el.$refs["child"].querySelector("div#quit-btn").classList.remove("hidden");
        el.$refs["parent"].classList.forEach(attr => el.attrs.push(attr));
        el.attrs.forEach(attr => el.$refs["parent"].classList.remove(attr));
        el.$refs["parent"].classList.add("fullscreen-parent");
        el.$refs["child"].classList.add("fullscreen-child");
    } else {
        console.log("cas 2")
        el.$refs["child"].querySelector("div#quit-btn").classList.add("hidden");
        el.$refs["parent"].classList.remove("fullscreen-parent");
        el.$refs["child"].classList.remove("fullscreen-child");
        el.attrs.forEach(attr => el.$refs["parent"].classList.add(attr));
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
        setChart(this, this.$refs["child"].childNodes[2], this.chartInfos);

        this.$refs["child"].addEventListener("click", ev => {
            if (this.attrs.length > 0) ev.stopPropagation();
        });

        this.$refs["child"].querySelector("#quit-btn").firstElementChild.addEventListener("click", ev => {
            toogleFullscreen(this);
            ev.stopPropagation(); // important to not have the click event triggered on an other div
        });
        
        window.addEventListener("keydown", ev => {
            if (ev.key == "Escape" && this.attrs.length > 0) {
                toogleFullscreen(this);
            }
        });
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