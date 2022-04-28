<template>
  <div>
    <Topbar>
        <template v-slot:left>
            <BackLink to="/explore"></BackLink>
        </template>

        <template v-slot:default>
            <Blank></Blank>
        </template>

        <template v-slot:right>
            <Blank></Blank>
        </template>
    </Topbar>
    <NavbarSelection v-on:valueChange="handleChange"></NavbarSelection>
    <main class="p-4">
        <div id="ahp">
            <div id="ahp-1">
                <h1 class="font-bold mb-2">AHP - Criteria choice</h1>
                <Card>
                    <div class="grid grid-cols-3">
                        <p>Criteria 1</p>
                        <select class="bg-transparent border border-transparent" name="c0" id="c0" v-on:change="testCritera()">
                            <option class="text-black" v-for="col in allCols" :key="col" :value="col">{{ beautifyName(col) }}</option>
                        </select>
                        <select name="c0m" id="c0m">
                            <option value="min">Min</option>
                            <option value="max">Max</option>
                        </select>
                        <p>Criteria 2</p>
                        <select class="bg-transparent border border-transparent" name="c1" id="c1" v-on:change="testCritera()">
                            <option class="text-black" v-for="col in allCols" :key="col" :value="col">{{ beautifyName(col) }}</option>
                        </select>
                        <select name="c1m" id="c1m">
                            <option value="min">Min</option>
                            <option value="max">Max</option>
                        </select>
                        <p>Criteria 3</p>
                        <select class="bg-transparent border border-transparent" name="c2" id="c2" v-on:change="testCritera()">
                            <option class="text-black" v-for="col in allCols" :key="col" :value="col">{{ beautifyName(col) }}</option>
                        </select>
                        <select name="c2m" id="c2m">
                            <option value="min">Min</option>
                            <option value="max">Max</option>
                        </select>
                        <p>Criteria 4</p>
                        <select class="bg-transparent border border-transparent" name="c3" id="c3" v-on:change="testCritera()">
                            <option class="text-black" v-for="col in allCols" :key="col" :value="col">{{ beautifyName(col) }}</option>
                        </select>
                        <select name="c3m" id="c3m">
                            <option value="min">Min</option>
                            <option value="max">Max</option>
                        </select>
                    </div>
                    <div class="flex items-center justify-center">
                        <button class="bg-blue-500 text-white px-2 py-1 rounded" v-on:click="nextAHP()">Next</button>
                    </div>
                </Card>
            </div>
            <div id="ahp-2" class="hidden">
                <h1 class="font-bold mb-2">AHP - Weight choice</h1>
                <Card>
                    <div class="grid grid-cols-3">
                        <!-- Crit 0 / Crit 1 -->
                        <div class="flex justify-between">
                            <span class="crit-0"></span>
                            <span id="v-1-0">1.00</span>
                        </div>
                        <input id="weight-1-0" type="range" value="1" min="-7" max="9" v-on:change="updateMatrix(1, 0)">
                        <div class="flex justify-between">
                            <span id="v-0-1">1.00</span>
                            <span class="crit-1"></span>
                        </div>
                        <!-- Crit 0 / Crit 2 -->
                        <div class="flex justify-between">
                            <span class="crit-0"></span>
                            <span id="v-2-0">1.00</span>
                        </div>
                        <input id="weight-2-0" type="range" value="1" min="-7" max="9" v-on:change="updateMatrix(2, 0)">
                        <div class="flex justify-between">
                            <span id="v-0-2">1.00</span>
                            <span class="crit-2"></span>
                        </div>
                        <!-- Crit 0 / Crit 3 -->
                        <div class="flex justify-between">
                            <span class="crit-0"></span>
                            <span id="v-3-0">1.00</span>
                        </div>
                        <input id="weight-3-0" type="range" value="1" min="-7" max="9" v-on:change="updateMatrix(3, 0)">
                        <div class="flex justify-between">
                            <span id="v-0-3">1.00</span>
                            <span class="crit-3"></span>
                        </div>
                        <!-- Crit 1 / Crit 2 -->
                        <div class="flex justify-between">
                            <span class="crit-1"></span>
                            <span id="v-2-1">1.00</span>
                        </div>
                        <input id="weight-2-1" type="range" value="1" min="-7" max="9" v-on:change="updateMatrix(2, 1)">
                        <div class="flex justify-between">
                            <span id="v-1-2">1.00</span>
                            <span class="crit-2"></span>
                        </div>
                        <!-- Crit 1 / Crit 3 -->
                        <div class="flex justify-between">
                            <span class="crit-1"></span>
                            <span id="v-3-1">1.00</span>
                        </div>
                        <input id="weight-3-1" type="range" value="1" min="-7" max="9" v-on:change="updateMatrix(3, 1)">
                        <div class="flex justify-between">
                            <span id="v-1-3">1.00</span>
                            <span class="crit-3"></span>
                        </div>
                        <!-- Crit 2 / Crit 3 -->
                        <div class="flex justify-between">
                            <span class="crit-2"></span>
                            <span id="v-3-2">1.00</span>
                        </div>
                        <input id="weight-3-2" type="range" value="1" min="-7" max="9" v-on:change="updateMatrix(3, 2)">
                        <div class="flex justify-between">
                            <span id="v-2-3">1.00</span>
                            <span class="crit-3"></span>
                        </div>
                    </div>
                    <div class="flex flex-col items-center justify-center">
                        <div>
                            Consistency:
                            <span id="consistency">0.00</span>
                            %
                        </div>
                        <div id="consistency-message" class="text-red-500"></div>
                        <button class="bg-blue-500 text-white px-2 py-1 rounded" v-on:click="previousAHP()">Previous</button>
                        <button class="bg-blue-500 text-white px-2 py-1 rounded" v-on:click="nextAHP()">Results</button>
                        <button class="bg-blue-500 text-white px-2 py-1 rounded" v-on:click="resetWeight()">Reset</button>
                    </div>
                </Card>
            </div>
            <div id="ahp-3" class="hidden">
                <h1 class="font-bold mb-2">AHP - Results</h1>
                <Card>
                    <div class="flex flex-col">
                        <Vue3ChartJs :ref="chartRef.result" v-bind="{ ...chartResult }" />
                        <div v-for="l in shownData" :key="l.Name" class="flex justify-between">
                            <div class="flex gap-2">
                                <span>
                                    <router-link :to="'/explore/' + type + '/' + l.Id">
                                        {{ l.Name }}
                                    </router-link>
                                </span>
                                <VTooltip v-if="l.MissingData" :triggers="['click', 'touch']">
                                    <InformationCircleIcon class="h-6 w-6 cursor-pointer text-red-500"></InformationCircleIcon>
                                    <template #popper>
                                        <p>Some data where missing when calculating the score for the element.<br>The average of the set was taken for the calcul.</p>
                                    </template>
                                </VTooltip>
                            </div>
                            <span>{{ l.Score }}</span>
                        </div>
                        <div>
                            <button class="bg-blue-500 text-white px-2 py-1 rounded" v-on:click="resetSelection()">Reset</button>
                            <button class="bg-blue-500 text-white px-2 py-1 rounded" v-on:click="showMoreResults()">Show More</button>
                        </div>
                    </div>
                </Card>
            </div>
        </div>
        <div id="custom" class="hidden">
            <h1 class="font-bold mb-2">Custom</h1>
            <Card>
                <table class="border-collapse border">
                    <tr>
                        <th class="border">Column</th>
                        <th class="border" colspan="2">Weight</th>
                    </tr>
                    <tr>
                        <td class="border">
                            <select name="col1" id="col1">
                                <option value="col">Col1</option>
                            </select>
                        </td>
                        <td class="border" colspan="2">
                            <input type="text" value="1">
                        </td>
                    </tr>
                    <tr>
                        <td class="border">
                            <select name="col1" id="col1">
                                <option value="col">Col1</option>
                            </select>
                        </td>
                        <td class="border">
                            <input type="text" value="1">
                        </td>
                        <td class="border">
                            <span>-</span>
                        </td>
                    </tr>
                </table>
            </Card>
        </div>
        <NavbarFill></NavbarFill>
    </main>
  </div>
</template>

<script>
import Topbar from "../../components/Topbar.vue";
import Blank from "../../components/Blank.vue";
import Card from "../../components/Card.vue";

import BackLink from "../../components/BackLink.vue";
import NavbarSelection from "../../components/NavbarSelection.vue";
import NavbarFill from "../../components/NavbarFill.vue";
import { useRoute, useRouter } from "vue-router";
import { onMounted, ref } from "vue";
import { beautifyName } from "../../utils";
import Vue3ChartJs from "@j-t-mcc/vue3-chartjs";

import { InformationCircleIcon } from "@heroicons/vue/outline";

import axios from "axios";

export default {
    name: "ExploreSelection",
    components: {
        NavbarSelection, NavbarFill,
        Topbar,
        Blank,
        Card,
        BackLink,
        InformationCircleIcon,
        Vue3ChartJs
    },
    setup() {
        const route = useRoute();
        const router = useRouter()
        const cols = ref([])
        const parameter = 4
        const data = ref([])
        const shownData = ref([])
        const allCols = ref([])
        const etapeAHP = ref(1)
        const type = route.params.type
        const numberResult = ref(5)

        var mat = [[1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0]]
        var w = [0, 0, 0, 0]
        var consistency = 0

        const calculConstitency = () => {

            // Calcul somme colonne
            var sommeCol = [0, 0, 0, 0]
            for (let i = 0; i < 4; i++) {
                const row = mat[i];

                for (let j = 0; j < 4; j++) {
                    sommeCol[j] += row[j]
                }
            }

            // Calcul matrix normalized
            var normalizedMatrix = [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
            for (let i = 0; i < 4; i++) {
                for (let j = 0; j < 4; j++) {
                    normalizedMatrix[i][j] = mat[i][j] / sommeCol[j]
                }
            }

            // Calcul weight
            w = [0, 0, 0, 0]
            for (let i = 0; i < 4; i++) {
                for (let j = 0; j < 4; j++) {
                    w[i] += normalizedMatrix[i][j]/4
                }
            }

            // Calcul (A*w)/w
            var Aww = [0, 0, 0, 0]
            for (let i = 0; i < 4; i++) {
                for (let j = 0; j < 4; j++) {
                    Aww[i] += mat[i][j] * w[j]
                }
                Aww[i] /= w[i]
            }

            // Calcul moyenne
            var lambda = 0
            for (let i = 0; i < 4; i++) {
                lambda += Aww[i]/4
            }

            // Consistency Ratio
            consistency = ((lambda - parameter) / (parameter - 1)) / 0.9

            // Update UI
            document.getElementById('consistency').textContent = (consistency * 100).toString().substring(0, 5)

            if (consistency > 0.1) {
                document.getElementById('consistency-message').textContent = "Attention, la consistence est supérieure à 10%. Les résultats peuvent ne pas être cohérents."
            }
            else {
                document.getElementById('consistency-message').textContent = ""
            }
        }

        const handleChange = (value) => {
            const custom = document.getElementById("custom");
            const ahp = document.getElementById("ahp");

            custom.classList.add("hidden");
            ahp.classList.add("hidden");

            if (value == "navbar-ahp") {
                ahp.classList.remove("hidden");
            }

            if (value == "navbar-custom") {
                custom.classList.remove("hidden");
            }
        };

        const ahp = async () => {
            if (consistency == "NaN") return

            if (consistency > 0.1) return

            const order = [document.getElementById('c0m').value, document.getElementById('c1m').value, document.getElementById('c2m').value, document.getElementById('c3m').value]
            const url = "http://127.0.0.1:5000/" + route.params.type + "/ahp?cols=" + cols.value + "&ord=" + order + "&w=" + w

            try {
                data.value = await axios.get(url).then((res) => res.data)
            } catch (error) {
                console.log(error);
            }

            updateShownData()
            populateChart()
        }

        const getData = async () => {
            const url = "http://127.0.0.1:5000/" + route.params.type + "/1"

            var element

            try {
                element = await axios.get(url).then((res) => res.data)
            } catch (error) {
                console.log(error);
            }

            Object.keys(element).forEach((col) => {
                if (['Density', 'Hlbr', 'Iodine_Number', 'Price', 'qPolarity', 'qSpreading', 'qViscosity', 'Saponification_Value', 'State', 'Viscosity', 'Emulsion_Type', "Hlb", "Concentration_Usage"].indexOf(col) != -1) {
                    allCols.value.push(col)
                }
            })
        }

        onMounted(getData)

        const testCritera = () => {
            for (let i = 0; i < 4; i++) {
                const el = document.getElementById('c' + i)
                el.classList.add('border-transparent')
                el.classList.remove('border-red-500')
            }

            var duplicate = false

            for (let i = 0; i < 4; i++) {
                for (let j = 0; j < 4; j++) {
                    if (i != j) {
                        const el1 = document.getElementById('c' + i);
                        const el2 = document.getElementById('c' + j);

                        if (el1.value == el2.value) {
                            duplicate = true
                            el1.classList.remove('border-transparent')
                            el1.classList.add('border-red-500')

                            el2.classList.remove('border-transparent')
                            el2.classList.add('border-red-500')
                        }

                    }
                }
            }

            return !duplicate
        }

        const nextAHP = () => {
            switch (etapeAHP.value) {
                case 1:
                    // Get values
                    for (let i = 0; i < 4; i++) {
                        cols.value.push(document.getElementById('c' + i).value)
                    }

                    // Test for non duplicate columns
                    if (!testCritera()) {
                        cols.value = []
                        return
                    }

                    // Fill the next card with the name of criteras
                    for (let i = 0; i < 4; i++) {
                        const critera = document.getElementById('c' + i).value
                        const elements = document.getElementsByClassName('crit-' + i)

                        Array.from(elements).forEach(el => {
                            el.textContent = beautifyName(critera)
                        });
                    }

                    // Hide the card and show the next one
                    document.getElementById("ahp-1").classList.add('hidden')
                    document.getElementById("ahp-2").classList.remove('hidden')

                    etapeAHP.value = 2
                    break;

                case 2:
                    // Verify Consistency
                    calculConstitency()

                    // Get résultat
                    ahp()

                    // Hide the card and show the next one
                    document.getElementById("ahp-2").classList.add('hidden')
                    document.getElementById("ahp-3").classList.remove('hidden')
                    etapeAHP.value = 3
                    break
            
                default:
                    break;
            }
        }

        const previousAHP = () => {
            switch (etapeAHP.value) {
                case 2:
                    resetWeight()

                    cols.value = []

                    // Hide the card and show the next one
                    document.getElementById("ahp-2").classList.add('hidden')
                    document.getElementById("ahp-1").classList.remove('hidden')
                    etapeAHP.value = 1
                    break;

                case 3:
                    // Hide the card and show the next one
                    document.getElementById("ahp-3").classList.add('hidden')
                    document.getElementById("ahp-2").classList.remove('hidden')
                    etapeAHP.value = 2
                    break
            
                default:
                    break;
            }
        }

        const updateMatrix = (i, j) => {
            const valLeft = document.getElementById('v-' + i + '-' + j)
            const valRight = document.getElementById('v-' + j + '-' + i)

            var val = document.getElementById('weight-' + i + '-' + j).value
            val = val < 1 ? 1/(-val + 2) :  +(val)

            valRight.textContent = (val).toFixed(2)
            mat[i][j] = val
            valLeft.textContent = (1/val).toFixed(2)
            mat[j][i] = 1/val

            calculConstitency()
        }

        const resetWeight = () => {
            for (let i = 0; i < 4; i++) {
                for (let j = 0; j < 4; j++) {
                    var range = document.getElementById('weight-' + i + '-' + j)
                    
                    if (range) {
                        range.value = 1.0
                        updateMatrix(i, j)
                    }

                }
            }
        }

        const resetSelection = () => {
            router.go()
        }

        const chartRef = {
            result: ref(null),
        }

        const chartResult = {
            id: "ChartResult",
            type: "bar",
            data: {
                labels : [],
                datasets: [{
                    axis: 'y',
                    label: "Score",
                    backgroundColor: 'rgb(255, 99, 132)',
                    data: [],
                }],
            },
            options: {
                indexAxis: 'y',
            }
        }

        const updateShownData = () => {
            shownData.value = data.value.slice(0, numberResult.value)
        }

        const populateChart = () => {
            chartResult.data.labels = []
            chartResult.data.datasets[0].data = []

            shownData.value.forEach(el => {
                chartResult.data.labels.push(el.Name)
                chartResult.data.datasets[0].data.push(el.Score)
            });

            chartRef.result.value.update()
        }

        const showMoreResults = () => {
            numberResult.value += 5

            updateShownData()
            populateChart()
        }

        return {
            beautifyName,
            handleChange,
            ahp,
            allCols,
            testCritera,
            updateMatrix,
            nextAHP,
            previousAHP,
            data,
            type,
            resetSelection,
            resetWeight,
            chartResult,
            chartRef,
            shownData,
            showMoreResults
        }
    }
}
</script>

<style>

</style>