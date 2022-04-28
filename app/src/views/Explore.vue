<template>
  <div>
    <Topbar>
      <template v-slot:left>
        <BackLink to="/"></BackLink>
      </template>

      <template v-slot:default>
        <h1 class="font-bold">Ingredients list</h1>
      </template>

      <template v-slot:right>
        <Blank></Blank>
      </template>
    </Topbar>
    <main class="p-4">
      <section>
        <Card>
          <Drawer title="Emollients">
            <template v-slot:right>
              <router-link to="/explore/graph/emollients">
                <ChartPieIcon class="h-6" v-tooltip="'Graph'"></ChartPieIcon>
              </router-link>
              <router-link to="/explore/selection/emollients">
                <BeakerIcon class="h-6" v-tooltip="'Selection'"></BeakerIcon>
              </router-link>
            </template>
            <template v-slot:items>
              <Drawer v-for="c in emollientsClass" :key="c" :title="c">
                <template v-slot:items>
                  <div v-for="e in emollientsFromClass(c)" :key="e">
                    <router-link :to="'/explore/emollients/' + e.Id">
                      {{ e.Inci }}
                    </router-link>
                  </div>
                </template>
              </Drawer>
            </template>
          </Drawer>
        </Card>
      </section>
      <section class="mt-4">
        <Card>
          <Drawer title="Surfactants">
            <template v-slot:right>
              <router-link to="/explore/graph/surfactants">
                <ChartPieIcon class="h-6" v-tooltip="'Graph'"></ChartPieIcon>
              </router-link>
              <router-link to="/explore/selection/surfactants">
                <BeakerIcon class="h-6" v-tooltip="'Selection'"></BeakerIcon>
              </router-link>
            </template>
            <template v-slot:items>
              <Drawer v-for="c in surfactantsClass" :key="c" :title="c">
                <template v-slot:items>
                  <div v-for="s in surfactantsFromClass(c)" :key="s">
                    <router-link :to="'/explore/surfactants/' + s.Id">
                      {{ s.Inci }}
                    </router-link>
                  </div>
                </template>
              </Drawer>
            </template>
          </Drawer>
        </Card>
      </section>
    </main>
  </div>
</template>

<script>
import Topbar from "../components/Topbar.vue";
import Blank from "../components/Blank.vue";
import Card from "../components/Card.vue";
import BackLink from "../components/BackLink.vue";
import Drawer from "../components/Drawer.vue";
import {
  ChartPieIcon,
  BeakerIcon,
} from "@heroicons/vue/outline";

import axios from "axios";
import { onMounted } from "@vue/runtime-core";
import { ref } from "vue";

export default {
  name: "Explore",
  components: {
    Topbar,
    Blank,
    Card,
    BackLink,
    ChartPieIcon,
    BeakerIcon,
    Drawer
  },
  setup() {
    const emollients = ref([]);
    const surfactants = ref([]);
    const emollientsClass = ref([])
    const surfactantsClass = ref([])

    const getEmollients = async () => {
      try {
        emollients.value = await axios.get("http://127.0.0.1:5000/emollients").then((res) => res.data)
        emollientsClass.value = Array.from(new Set(emollients.value.map((emo) => { return emo.Class ? emo.Class : 'undefined' })))

      } catch (error) {
        console.log(error);
      }
    };

    const getSurfactants = async () => {
      try {
        surfactants.value = await axios.get("http://127.0.0.1:5000/surfactants").then((res) => res.data)
        surfactantsClass.value = Array.from(new Set(surfactants.value.map((sur) => { return sur.Class ? sur.Class : 'undefined' })))
      } catch (error) {
        console.log(error);
      }
    };

    onMounted(getEmollients);
    onMounted(getSurfactants);

    const emollientsFromClass = (className) => {
      return emollients.value.filter((el) => {
        if (el.Class == className) return el
        if (className == 'undefined' && el.Class == null) return el
      })
    }

    const surfactantsFromClass = (className) => {
      return surfactants.value.filter((el) => {
        if (el.Class == className) return el
        if (className == 'undefined' && el.Class == null) return el
      })
    }

    return {
      emollients,
      emollientsClass,
      emollientsFromClass,
      surfactants,
      surfactantsClass,
      surfactantsFromClass,
    };
  },
};
</script>

<style>
</style>