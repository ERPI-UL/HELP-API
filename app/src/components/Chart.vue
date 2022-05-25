<template>
    <div v-on:click="toogleFullscreen(this)" class="slide-in bg-white rounded-lg shadow-lg p-2 relative w-[20vw] h-min max-w-full max-h-full m-4 scale-100 hover:shadow-xl hover:scale-105 cursor-pointer">
        <div>
            <h2 class="text-center font-bold">{{title}}</h2>
            <canvas id="chart-render" class="flex grow bg-white"></canvas>
        </div>
    </div>
</template>

<script>
import Chart from "chart.js/auto";

function setChart(el, div, infos) {
    const chart = new Chart(div, infos);
    div.parentNode.addEventListener("click", ev => {
        if (el.attrs.length > 0) ev.stopPropagation();
    })
}

/**
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
    z-index: 99;
    cursor: auto;
    box-shadow: 0px 0px 80px #0005;
    border-radius: 1em;
    padding: 1em;
}
.fullscreen-parent {
    background-color: #0006;
    position: absolute;
    top: 0px;
    left: 0px;
    width: 100vw;
    height: 100vh;
}
</style>