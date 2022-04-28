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
        <div class="flex gap-2 pr-4">
          <div class="cursor-pointer" v-on:click="toggleFilter()">
            <FilterIcon v-tooltip="'Filter'"></FilterIcon>
          </div>
          <div class="cursor-pointer" v-on:click="downloadData()">
            <CloudDownloadIcon
              v-tooltip="'Download current view'"
            ></CloudDownloadIcon>
          </div>
        </div>
      </template>
    </Topbar>
    <NavbarGraph v-on:valueChange="handleChange"></NavbarGraph>
    <main class="p-4">
      <Panel id="filterPanel" class="translate-x-full">
        <Card>
          <h1 class="font-bold">Filters</h1>
          <div class="flex flex-col gap-2" v-if="fullData.length > 0" id="filters">
            <div v-for="(el, i) in Object.keys(fullData[0])" :key="i">
              <div class="flex flex-col" v-if="['Afterfeel', 'Additional_Information', 'Cas', 'Inci', 'Class', 'Emollience', 'Hlb'].indexOf(el) != -1">
                <label :for="el">{{ beautifyName(el) }}</label>
                <input :id="el" :name="el" class="border rounded-sm" type="text"/>
              </div>
              <div class="flex flex-col" v-if="['qViscosity'].indexOf(el) != -1">
                <label :for="el">{{ el }}</label>
                <select :name="el" :id="el" class="border rounded-sm">
                  <option value=""></option>
                  <option value="5">Very high</option>
                  <option value="4">High</option>
                  <option value="2">Medium</option>
                  <option value="0">Low</option>
                </select>
              </div>
              <div class="flex flex-col" v-if="['qPolarity', 'qSpreading'].indexOf(el) != -1">
                <label :for="el">{{ el }}</label>
                <select :name="el" :id="el" class="border rounded-sm">
                  <option value=""></option>
                  <option value="4">High</option>
                  <option value="3">Medium to high</option>
                  <option value="2">Medium</option>
                  <option value="1">Medium to low</option>
                  <option value="0">Low</option>
                </select>
              </div>
              <div class="flex flex-col" v-if="['State'].indexOf(el) != -1">
                <label :for="el">{{ el }}</label>
                <select :name="el" :id="el" class="border rounded-sm">
                  <option value=""></option>
                  <option value="0">liquid</option>
                  <option value="1">liquid paste</option>
                  <option value="2">paste</option>
                  <option value="3">solid paste</option>
                  <option value="4">solid</option>
                </select>
              </div>
              <div class="flex flex-col" v-if="['Biodegrability'].indexOf(el) != -1">
                <label :for="el">{{ el }}</label>
                <select :name="el" :id="el" class="border rounded-sm">
                  <option value=""></option>
                  <option value="readily biodegradable">
                    readily biodegradable
                  </option>
                  <option value="not biodegradable">not biodegradable</option>
                </select>
              </div>
              <div class="flex flex-col" v-if="['Origin'].indexOf(el) != -1">
                <label :for="el">{{ el }}</label>
                <select :name="el" :id="el" class="border rounded-sm">
                  <option value=""></option>
                  <option value="natural">natural</option>
                  <option value="Nature raw materials (enzymatic)">
                    Nature raw materials (enzymatic)
                  </option>
                  <option value="Nature raw materials">
                    Nature raw materials
                  </option>
                  <option value="Natural and synthetic raw materials">
                    Natural and synthetic raw materials
                  </option>
                  <option value="synthetic">synthetic</option>
                </select>
              </div>
              <div class="flex flex-col" v-if="['Price', 'Hlbr', 'Mw', 'Density', 'Iodine_Number', 'Saponification_Value', 'Refrative_Index', 'Viscosity', 'Concentration_Usage',].indexOf(el) != -1">
                <label :for="el">{{ beautifyName(el) }}</label>
                <div>
                  <input type="number" :name="el" :id="el" class="border rounded-sm w-1/2" value="0"/>
                  <input type="number" :name="el + '__Max'" :id="el + '__Max'" class="border rounded-sm w-1/2" value="9999"/>
                </div>
              </div>
              <div class="flex flex-col" v-if="['Ionic_Class'].indexOf(el) != -1">
                <label :for="el">{{ beautifyName(el) }}</label>
                <select :name="el" :id="el" class="border rounded-sm">
                  <option value=""></option>
                  <option value="ionic">ionic</option>
                  <option value="anionic">anionic</option>
                </select>
              </div>
              <div class="flex flex-col" v-if="['Emulsion_Type'].indexOf(el) != -1">
                <label :for="el">{{ beautifyName(el) }}</label>
                <select :name="el" :id="el" class="border rounded-sm">
                  <option value=""></option>
                  <option value="0">O/W</option>
                  <option value="1">O/W and W/O</option>
                  <option value="2">W/O</option>
                </select>
              </div>
              <div class="flex flex-col" v-if="['Texture'].indexOf(el) != -1">
                <label :for="el">{{ el }}</label>
                <select :name="el" :id="el" class="border rounded-sm">
                  <option value=""></option>
                  <option value="Cream">Cream</option>
                  <option value="Lotion">Lotion</option>
                  <option value="Spray">Spray</option>
                  <option value="Gel">Gel</option>
                  <option value="-">-</option>
                </select>
              </div>
              <div v-if="['Application'].indexOf(el) != -1">
                <h2 class="font-semibold">Application</h2>
                <div class="grid grid-cols-2">
                  <div class="flex items-center gap-2">
                    <input type="checkbox" :name="el + '__Body_Care'" :id="el + '__Body_Care'">
                    <label :for="el + '__Body_Care'">Body Care</label>
                  </div>
                  <div class="flex items-center gap-2">
                    <input type="checkbox" :name="el + '__Face_Care'" :id="el + '__Face_Care'">
                    <label :for="el + '__Face_Care'">Face Care</label>
                  </div>
                  <div class="flex items-center gap-2">
                    <input type="checkbox" :name="el + '__Sun_Care'" :id="el + '__Sun_Care'">
                    <label :for="el + '__Sun_Care'">Sun Care</label>
                  </div>
                  <div class="flex items-center gap-2">
                    <input type="checkbox" :name="el + '__Hair_Care'" :id="el + '__Hair_Care'">
                    <label :for="el + '__Hair_Care'">Hair Care</label>
                  </div>
                  <div class="flex items-center gap-2">
                    <input type="checkbox" :name="el + '__Color'" :id="el + '__Color'">
                    <label :for="el + '__Color'">Color</label>
                  </div>
                  <div class="flex items-center gap-2">
                    <input type="checkbox" :name="el + '__Antiperspirant_Deodorant'" :id="el + '__Antiperspirant_Deodorant'">
                    <label :for="el + '__Antiperspirant_Deodorant'">Antiperspirant Deodorant</label>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="flex justify-end gap-2 mt-2">
            <button class="bg-white border border-blue-500 rounded text-blue-500 py-1 px-2" v-on:click="resetFilter(); toggleFilter();">Reset</button>
            <button class="bg-blue-500 rounded text-white py-1 px-2" v-on:click="setFilter(); toggleFilter();">Filter</button>
          </div>
        </Card>
      </Panel>
      <div id="graph">
        <h1 class="font-bold mb-2">Graph</h1>
        <Card>
          <div id="data-message" class="text-red-500"></div>
          <Vue3ChartJs :ref="chartRef.scatter" v-bind="{ ...chartScatter }" />
          <Vue3ChartJs :ref="chartRef.bubble" v-bind="{ ...chartBubble }" />
          <select name="type" id="type" v-on:change="changeChartType()">
            <option :value="type" v-for="type in chartTypes" :key="type">
              {{ type }}
            </option>
          </select>
          <hr />
          <div class="flex">
            <div class="overflow-hidden grow">
              <h1>X axis</h1>
              <ul v-if="fullData.length > 0">
                <li v-for="(el, i) in Object.keys(fullData[0])" :key="i">
                  <div
                    v-if="
                      [
                        'Application',
                        'Class',
                        'Id',
                        'Inci',
                        'Ionic_Class',
                        'Class',
                        'Origin',
                        'Texture',
                        'Additional_Information',
                        'Afterfeel',
                        'Biodegradability',
                        'Cas',
                        'Emollience',
                        'Iodine_Number',
                        'Saponification_Value',
                      ].indexOf(el) == -1
                    "
                  >
                    <input
                      v-if="el == xAxe"
                      class="mr-1"
                      type="checkbox"
                      :name="el + 'x'"
                      :id="el + 'x'"
                      checked
                      v-on:click="changeAxe('x', el)"
                    />
                    <input
                      v-else
                      class="mr-1"
                      type="checkbox"
                      :name="el + 'x'"
                      :id="el + 'x'"
                      v-on:click="changeAxe('x', el)"
                    />
                    <label :for="el + 'x'">{{ beautifyName(el) }}</label>
                  </div>
                </li>
              </ul>
            </div>
            <div class="overflow-hidden grow">
              <h1>Y axis</h1>
              <ul v-if="fullData.length > 0">
                <li v-for="(el, i) in Object.keys(fullData[0])" :key="i">
                  <div
                    v-if="
                      [
                        'Application',
                        'Class',
                        'Id',
                        'Inci',
                        'Ionic_Class',
                        'Class',
                        'Origin',
                        'Texture',
                        'Additional_Information',
                        'Afterfeel',
                        'Biodegradability',
                        'Cas',
                        'Emollience',
                        'Iodine_Number',
                        'Saponification_Value',
                      ].indexOf(el) == -1
                    "
                  >
                    <input
                      v-if="el == yAxe"
                      class="mr-1"
                      type="checkbox"
                      :name="el + 'y'"
                      :id="el + 'y'"
                      checked
                      v-on:click="changeAxe('y', el)"
                    />
                    <input
                      v-else
                      class="mr-1"
                      type="checkbox"
                      :name="el + 'y'"
                      :id="el + 'y'"
                      v-on:click="changeAxe('y', el)"
                    />
                    <label :for="el + 'y'">{{ beautifyName(el) }}</label>
                  </div>
                </li>
              </ul>
            </div>
            <div class="overflow-hidden grow" v-if="chartType == 'bubble'">
              <h1>R axis</h1>
              <ul v-if="fullData.length > 0">
                <li v-for="(el, i) in Object.keys(fullData[0])" :key="i">
                  <div
                    v-if="
                      [
                        'Application',
                        'Class',
                        'Id',
                        'Inci',
                        'Ionic_Class',
                        'Class',
                        'Origin',
                        'Texture',
                        'Additional_Information',
                        'Afterfeel',
                        'Biodegradability',
                        'Cas',
                        'Emollience',
                        'Iodine_Number',
                        'Saponification_Value',
                      ].indexOf(el) == -1
                    "
                  >
                    <input
                      v-if="el == zAxe"
                      class="mr-1"
                      type="checkbox"
                      :name="el + 'z'"
                      :id="el + 'z'"
                      checked
                      v-on:click="changeAxe('z', el)"
                    />
                    <input
                      v-else
                      class="mr-1"
                      type="checkbox"
                      :name="el + 'z'"
                      :id="el + 'z'"
                      v-on:click="changeAxe('z', el)"
                    />
                    <label :for="el + 'z'">{{ beautifyName(el) }}</label>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </Card>
      </div>
      <div id="table" class="hidden">
        <h1 class="font-bold mb-2">Table</h1>
        <Card>
          <table
            v-if="fullData.length > 0"
            class="
              block
              overflow-auto
              max-h-[40rem]
              border-collapse border border-slate-500
            "
          >
            <thead>
              <tr>
                <td class="border border-slate-600 p-2">Show</td>
                <td
                  class="border border-slate-600 p-2"
                  v-for="(el, i) in fullData[0]"
                  :key="i"
                >
                  {{ beautifyName(i) }}
                </td>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(el, i) in fullData" :key="i">
                <td class="border border-slate-700 p-2">
                  <input
                    type="checkbox"
                    :name="el.inci"
                    :id="el.inci"
                    checked
                    v-on:click="hide_show(el.Inci)"
                  />
                </td>
                <td
                  class="border border-slate-700 p-2"
                  v-for="(v, j) in el"
                  :key="j"
                >
                  <ul v-if="j == 'Application'">
                    <li v-for="(n, k) in v" :key="k">
                      {{ beautifyName(k) }}: {{ n ? n : "NA" }}
                    </li>
                  </ul>
                  <ul v-else-if="j == 'Iodine_Number'">
                    <li v-for="(n, k) in v" :key="k">
                      {{ beautifyName(k) }}: {{ n ? n : "NA" }}
                    </li>
                  </ul>
                  <ul v-else-if="j == 'Saponification_Value'">
                    <li v-for="(n, k) in v" :key="k">
                      {{ beautifyName(k) }}: {{ n ? n : "NA" }}
                    </li>
                  </ul>
                  <ul v-else-if="j == 'Concentration_Usage'">
                    <li v-for="(n, k) in v" :key="k">
                      {{ beautifyName(k) }}: {{ n ? n : "NA" }}
                    </li>
                  </ul>
                  <ul v-else-if="j == 'Texture'">
                    <li v-for="(n, k) in v" :key="k">
                      {{ beautifyName(k) }}: {{ n ? n : "NA" }}
                    </li>
                  </ul>
                  <p v-else>{{ v }}</p>
                </td>
              </tr>
            </tbody>
          </table>
        </Card>
      </div>
      <div id="list" class="hidden">
        <h1 class="font-bold mb-2">List</h1>
        <Card>
          <div v-for="cat in categories" :key="cat">
            <h1 class="font-bold">{{ cat }}</h1>
            <div v-for="el in fullData" :key="el.Id">
              <div
                class="ml-4"
                v-if="
                  el.Class == cat || (cat == 'undefined' && el.Class == null)
                "
              >
                <span>{{ el.Inci }}</span>
              </div>
            </div>
          </div>
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
import Panel from "../../components/Panel.vue";

import Vue3ChartJs from "@j-t-mcc/vue3-chartjs";
import BackLink from "../../components/BackLink.vue";
import NavbarGraph from "../../components/NavbarGraph.vue";
import NavbarFill from "../../components/NavbarFill.vue";
import { useRoute } from "vue-router";
import { onMounted, ref } from "vue";
import { FilterIcon, CloudDownloadIcon } from "@heroicons/vue/outline";
import { beautifyName, pluginChartBackground } from "../../utils";

import axios from "axios";

export default {
  name: "ExploreGraph",
  components: {
    Topbar,
    Blank,
    Card,
    Vue3ChartJs,
    BackLink,
    NavbarGraph,
    NavbarFill,
    FilterIcon,
    Panel,
    CloudDownloadIcon,
  },
  setup() {
    const route = useRoute();
    const fullData = ref([]);
    const categories = ref([]);
    var categoriesColor = [];

    var filterOpened = false;

    const chartTypes = ["scatter", "bubble"];

    const chartType = ref("scatter");

    const chartRef = {
      scatter: ref(null),
      bubble: ref(null),
    };

    const hidden = ref([]);
    const selected = ref("");
    const xAxe = ref("x");
    const yAxe = ref("y");
    const zAxe = ref("z");

    const chartScatter = {
      id: "ChartScatter",
      type: "scatter",
      data: {
        datasets: [],
      },
      options: {
        onClick: function (ctx) {
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: function (ctx) {
                let label = [];
                let dtst = ctx.dataset;
                label.push((dtst.label || "") + ": ");
                let data = dtst.data;
                let index = ctx.dataIndex;
                let xx = ctx.parsed.x;
                let yy = ctx.parsed.y;

                label.push(data[index].name);

                label.push("(" + xAxe.value + " : " + xx + ", " + yAxe.value + " : " + yy + ")");
                return label;
              },
            },
          },
        },
      },
      plugins : [pluginChartBackground]
    };

    const chartBubble = {
      id: "ChartBubble",
      type: "bubble",
      data: {
        datasets: [],
      },
      options: {
        onClick: function (ctx) {
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: function (ctx) {
                let label = [];
                let dtst = ctx.dataset;
                label.push((dtst.label || "") + ": ");
                let data = dtst.data;
                let index = ctx.dataIndex;
                let xx = ctx.parsed.x;
                let yy = ctx.parsed.y;

                label.push(data[index].name);

                label.push("(" + xAxe.value + " : " + xx + ", " + yAxe.value + " : " + yy + ")");
                return label;
              },
            },
          },
        },
      },
      plugins : [pluginChartBackground]
    };

    var dataShown = "graph";

    const getRandomNumber = () => {
      const min = 0;
      const max = 256;
      return Math.random() * (max - min) + min;
    };

    const clamp = (min, value, max) => {
      if (value < min) return min;
      if (value > max) return max;
      return value;
    };

    for (let i = 0; i < 15; i++) {
      categoriesColor.push(
        "rgb(" +
          getRandomNumber() +
          ", " +
          getRandomNumber() +
          ", " +
          getRandomNumber() +
          ")"
      );
    }

    const populateData = () => {
      const datasets = [];

      categories.value.forEach((cat, i) => {
        datasets.push({
          label: cat,
          backgroundColor: categoriesColor[i],
          data: [],
        });
      });

      fullData.value.forEach((el) => {
        if (!hidden.value.includes(el.Inci)) {
          if (el[xAxe.value] != null && el[yAxe.value] != null) {
            var value = {
              name: el[inci],
              x: el[xAxe.value],
              y: el[yAxe.value],
            };

            if (chartType.value == "bubble" && el[zAxe.value] != null) {
              value.r = el[zAxe.value];
            }

            datasets[el.Class ? categories.value.indexOf(el.Class) : categories.value.indexOf("undefined")].data.push(value);
          }
        }
      });

      chartScatter.data.datasets = []; // Empty the list of datasets
      chartBubble.data.datasets = []; // Empty the list of datasets

      chartScatter.data.datasets = datasets;
      chartBubble.data.datasets = datasets;
    };

    const handleChange = (value) => {
      const table = document.getElementById("table");
      const list = document.getElementById("list");
      const graph = document.getElementById("graph");

      table.classList.add("hidden");
      list.classList.add("hidden");
      graph.classList.add("hidden");

      if (value == "navbar-graph") {
        graph.classList.remove("hidden");
        dataShown = "graph";
      }

      if (value == "navbar-list") {
        list.classList.remove("hidden");
        dataShown = "list";
      }

      if (value == "navbar-table") {
        table.classList.remove("hidden");
        dataShown = "table";
      }
    };

    const changeAxe = (axe, value) => {
      if (axe == "x") {
        xAxe.value = value;
      }

      if (axe == "y") {
        yAxe.value = value;
      }

      if (axe == "z") {
        zAxe.value = value;
      }

      populateData();
      chartRef[chartType.value].value.update();
    };

    const getData = async () => {
      // Previous Data Store in LocalStorage
      const previousData = localStorage.getItem(
        "formultool." + route.params.type
      );

      try {
        fullData.value = await axios
          .get("http://127.0.0.1:5000/" + route.params.type + previousData)
          .then((res) => res.data);
        categories.value = Array.from(
          new Set(
            fullData.value.map((el) => {
              if (el.Class) {
                return el.Class;
              } else {
                return "undefined";
              }
            })
          )
        );

        if (fullData.value.length == 0) {
          document.getElementById("data-message").textContent =
            "No Data with the current filter.";
        } else {
          document.getElementById("data-message").textContent = "";
        }

        populateData();
        chartRef[chartType.value].value.update();
      } catch (error) {
        console.log(error);
      }
    };

    onMounted(getData);

    const toggleFilter = () => {
      if (filterOpened) {
        // Fermer le panneau
        const panel = document.getElementById("filterPanel");
        panel.classList.add("translate-x-full");
      } else {
        // Ouvrir le panneau
        const panel = document.getElementById("filterPanel");
        panel.classList.remove("translate-x-full");
      }

      filterOpened = !filterOpened;
    };

    const setFilter = () => {
      const root = document.getElementById("filters");
      var filter = "?";
      var tmp_numeric_filter = "";

      if (root) {
        const inputs = Array.from(root.getElementsByTagName("input"));
        inputs.forEach((input) => {
          if (input.value != "") {
            if (
              [
                "Price",
                "Viscosity",
                "Saponification_Value",
                "Mw",
                "Iodine_Number",
                "Hlbr",
                "Density",
                "Concentration_Usage",
              ].indexOf(input.name) != -1
            ) {
              tmp_numeric_filter = input.name + "=" + input.value;
            } else if (
              [
                "Price__Max",
                "Viscosity__Max",
                "Saponification_Value__Max",
                "Mw__Max",
                "Iodine_Number__Max",
                "Hlbr__Max",
                "Density__Max",
                "Concentration_Usage__Max",
              ].indexOf(input.name) != -1
            ) {
              tmp_numeric_filter += "-" + input.value + "&";

              if (!tmp_numeric_filter.endsWith("=0-9999&")) {
                filter += tmp_numeric_filter;
              }
            } else if (
              [
                "Application__Body_Care",
                "Application__Face_Care",
                "Application__Sun_Care",
                "Application__Hair_Care",
                "Application__Color",
                "Application__Antiperspirant_Deodorant"
              ].indexOf(input.name) != -1
            ) {
                if (input.checked) {
                  filter += input.name + "=Recomended&"
                }
            } else {
              filter += input.name + "=" + input.value + "&";
            }
          }
        });
        const selects = Array.from(root.getElementsByTagName("select"));
        selects.forEach((select) => {
          if (select.value != "") {
            filter += select.name + "=" + select.value;
          }
        });
      }

      localStorage.setItem("formultool." + route.params.type, filter);
      getData();
    };

    const resetFilter = () => {
      localStorage.setItem("formultool." + route.params.type, "?");
      getData();
    };

    const downloadData = () => {
      if (dataShown == "graph") {
        // Download Chart as image
        let a = document.createElement("a");
        a.href =
          chartRef[chartType.value].value.chartJSState.chart.toBase64Image();
        a.download = "formultool-graph.png";
        a.click();
        a = null;
      }

      if (dataShown == "table") {
        let dataCSV = "data:text/csv;charset=utf-8,";
        const columnDelimiter = ",";
        const lineDelimiter = "\n";

        const keys = Object.keys(fullData.value[0]);

        // Add columns name
        dataCSV += keys.join(columnDelimiter) + lineDelimiter;

        // Add data
        fullData.value.forEach((el) => {
          let line = [];

          keys.forEach((key) => {
            line.push(el[key]);
          });

          dataCSV += line.join(columnDelimiter) + lineDelimiter;
        });

        let a = document.createElement("a");
        a.href = dataCSV;
        a.download = "formultool-export.csv";
        a.click();
        a = null;
      }
    };

    const hide_show = (name) => {
      var input = document.getElementById(name);

      if (input == null) return;

      if (input.checked) {
        var index = hidden.value.indexOf(name);

        if (index < 0) return;

        hidden.value.splice(index, 1);
      } else {
        hidden.value.push(name);
      }

      populateData();
      chartRef[chartType.value].value.update();
    };

    const changeChartType = () => {
      chartType.value = document.getElementById("type").value;

      document.getElementById("ChartBubble").style.display = "none";
      document.getElementById("ChartScatter").style.display = "none";

      switch (chartType.value) {
        case "bubble":
          document.getElementById("ChartBubble").style.display = "block";
          break;

        case "scatter":
          document.getElementById("ChartScatter").style.display = "block";
          break;

        default:
          break;
      }

      populateData();
      chartRef[chartType.value].value.update();
    };

    onMounted(changeChartType);

    return {
      beautifyName,
      chartType,
      selected,
      handleChange,
      fullData,
      changeAxe,
      xAxe,
      yAxe,
      zAxe,
      categories,
      toggleFilter,
      getData,
      downloadData,
      hide_show,
      chartTypes,
      changeChartType,
      chartBubble,
      chartScatter,
      setFilter,
      chartRef,
      resetFilter,
    };
  },
};
</script>

<style>
</style>