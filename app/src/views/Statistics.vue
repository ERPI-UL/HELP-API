<template>
    <div class="min-h-screen flex flex-col">
        <div class="p-2">
            <Topbar></Topbar>
        </div>
        <div class="block md:flex grow">
            <div class="m-2 grow-0">
                <div class="bg-white rounded min-w-[12vw] divide-y grow">
                    <h2 class="text-2xl leading-9 font-extrabold text-indigo-600 px-6 py-2 whitespace-nowrap">Statistiques</h2>
                    <div class="md:pt-8 flex md:flex-col md:overflow-x-visible overflow-x-scroll justify-between">
                        <a class="whitespace-nowrap md:min-w-full md:p-4 md:m-4 p-2 m-2 rounded-lg text-base font-semibold text-left text-indigo-800 outline-none hover:border-indigo-300" 
                            :class="(window.location.href.split('#')[1] == 'learning')?'bg-indigo-600 text-indigo-50 shadow-lg shadow-indigo-600': ''"
                            href="#learning">
                            Apprentissage
                        </a>
                        <a class="whitespace-nowrap md:min-w-full md:p-4 md:m-4 p-2 m-2 rounded-lg text-base font-semibold text-left text-indigo-800 outline-none hover:border-indigo-300"
                            :class="(window.location.href.split('#')[1] == 'testing')?'bg-indigo-600 text-indigo-50 shadow-lg shadow-indigo-600': ''"
                            href="#testing">
                            Évaluations
                        </a>
                    </div>
                </div>
            </div>
            <div class="m-4 grow">
                <div class="bg-white shadow-lg p-2 rounded-lg w-full h-fit md:flex block">
                    <div class="flex md:mr-6" v-if="user.canTeacher()">
                        <h2 class="m-1 p-1">Utilisateurs: </h2>
                        <select name="username" id="user-select" class="border-none rounded bg-indigo-50 p-1 m-1">
                            <option value="all">Tous</option>
                            <option value="user1">Utilisateur 1</option>
                            <option value="user1">Utilisateur 2</option>
                        </select>
                    </div>
                    <div class="flex">
                        <h2 class="m-1 p-1">Scénarios: </h2>
                        <select name="username" id="user-select" class="border-none rounded bg-indigo-50 p-1 m-1">
                            <option value="all">Tous</option>
                            <option value="user1">Scénario 1</option>
                            <option value="user1">Scénario 2</option>
                        </select>
                    </div>
                </div>
                <div class="m-2 ml-4 flex flex-wrap justify-evenly grow"> <!-- Statistiques -->
                    <div class="center mt-10 overflow-hidden" id="loadzone">
                        <p class="text-center text-4xl text-gray-500">Chargement ...</p>
                        <p class="text-center text-2xl text-gray-400">Chargement des données</p>
                    </div>
                    <Chart v-for="chart in charts" :title="chart.title" :chartInfos="chart.data"></Chart>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Topbar from "../components/Topbar.vue";
import Chart from "../components/Chart.vue";
import User from "../script/User";

const charts = [];
var dom = null;

var counter = 0;
function addElement() {
    const len = Math.round(Math.random()*8)+2;
    fetch("https://random-word-api.herokuapp.com/word?number="+(len+1)).then(text => text.json().then( words => {
        document.getElementById("loadzone").style.display = "none";
        charts.push({
            title: words[0],
            data: {
                type: Math.random() > 0.5 ? "bar" : "line",
                data: {
                    labels: words.splice(1, len),
                    datasets: [{
                        label: "Some data",
                        backgroundColor: '#4F46E5',
                        borderColor: '#4F46E5',
                        data: Array.from({length: len}, () => Math.random()), // two last ones for scale hehe
                        tension: 0.5,
                        fill: Math.random() > 0.5
                    }]
                }
            }
        });
    }));
    if (counter++ < Math.random()*2+4) {
        setTimeout(addElement, 300);
    } else setTimeout(() => {
        if (dom != null) dom.$forceUpdate();
    }, 1000);
    if (dom != null) dom.$forceUpdate();
}

export default {
    name: "Statistics",
    data: () => {
        return {charts, user: User.currentUser}
    },
    components: {
        Topbar,
        Chart
    },
    setup() {
        if (!User.currentUser.canLearner()) window.history.back();
        return {window};
    },
    mounted() {
        dom = this;
        setTimeout(() => {
            addElement();
        }, 600);
    }
};
</script>