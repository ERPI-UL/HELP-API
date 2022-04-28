<template>
  <div>
    <Topbar>
      <template v-slot:left>
        <BackLink to="/explore"></BackLink>
      </template>

      <template v-slot:default>
        <h1 class="font-bold">Ingredient Informations</h1>
      </template>

      <template v-slot:right>
        <div class="pr-4">
          <VTooltip :triggers="['click', 'touch', 'focus']">
            <InformationCircleIcon
              class="h-6 w-6 cursor-pointer"
            ></InformationCircleIcon>
            <template #popper>
              <div>
                <header class="font-semibold top-0 flex">Informations</header>
                <div class="flex-col flex p-2 border-t-2 overflow-y-auto h-[480px]">
                  <div v-for="(item, cle) in descr" :key="item.id">
                    <div ></div>
                    <span class="font-semibold">{{ cle.replace(/_/g," ") }} :</span>
                    <span class="font-light px-5">{{ item }}</span>
                    <span v-if="cle === 'Hlbr' || cle === 'Hlb'">
                      <img src="../../assets/logo.png">
                    </span>
                  </div>
                </div>
              </div>
            </template>
          </VTooltip>
        </div>
      </template>
    </Topbar>

    <main class="p-4">
      <section>
        <Card>
          <h2 class="font-semibold mb-4">
            {{bdd.Class}} : {{ bdd.Inci }}
          </h2>
          <div class="flex flex-col gap-4 border-t-2 border-black">
            <div v-for="(item, cle) in bdd" :key="cle">
              <div v-if="cle != 'Id'">
                <div class="font-semibold">
                  {{ cle.replace(/_/g, ' ') }} :

                  <InformationCircleIcon
                    class="h-6 w-6 inline-block"
                    v-if="Object.keys(descr).indexOf(cle) != -1"
                    v-tooltip="'' + descr[cle]"
                  ></InformationCircleIcon>

                  <InfoSolid
                    class="h-6 w-6 inline-block"
                    v-else
                    v-tooltip="'No description available for ' + cle"
                  ></InfoSolid>

                  <div
                    class="font-normal px-5"
                    v-if="
                      cle === 'qViscosity' ||
                      cle === 'qPolarity' ||
                      cle === 'qSpreading'
                    "
                  >
                    {{ QUALITATIVES[item] }}
                  </div>

                  <div
                    class="font-normal px-5"
                    v-else-if="cle === 'Emulsion_Type'"
                  >
                    {{ EMUL_TYPE[item] }}
                  </div>

                  <div class="font-normal px-5" v-else-if="cle === 'State'">
                    {{ STATES[item] }}
                  </div>

                  <div
                    class="flex flex-wrap justify-left divide-x-2"
                    v-else-if="
                      cle === 'Application' ||
                      cle === 'Iodine_Number' ||
                      cle === 'Saponification_Value' ||
                      cle === 'Concentration_Usage' ||
                      cle === 'Texture'
                    "
                  >
                    <div v-for="(item2, cle2) in item" :key="cle2">
                      <div class="flex-1 px-4 divide-y-2 ">
                        <div class="font-semibold">{{ cle2.replace(/_/g, ' ') }} :</div>
                        <div class="font-normal px-5" v-if="item2 === null">
                          -
                        </div>
                        <div class="font-normal px-5" v-else>
                          {{ item2 }}
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="font-normal px-5" v-else-if="item === null">
                    -
                  </div>
                  <div class="font-normal px-5" v-else>
                    {{ item }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Card>
      </section>
    </main>
  </div>
</template>

<script>
import Topbar from "../../components/Topbar.vue";
import Blank from "../../components/Blank.vue";
import Card from "../../components/Card.vue";
import BackLink from "../../components/BackLink.vue";
import { useRoute } from "vue-router";
import { InformationCircleIcon } from "@heroicons/vue/outline";
import { InformationCircleIcon as InfoSolid } from "@heroicons/vue/solid";

import { onMounted, ref } from "vue";

import axios from "axios";
import descriptions from "../../assets/descriptions.js";

export default {
  name: "ExploreItem",
  components: {
    Topbar,
    Blank,
    Card,
    BackLink,
    InformationCircleIcon,
    InfoSolid,
  },
  setup() {
    const route = useRoute();
    const id = route.params.id;
    const bdd = ref([]);
    const descr = ref([]);
    const QUALITATIVES = [
      "low",
      "medium to low",
      "medium",
      "medium to high",
      "high",
      "very high",
    ];
    const STATES = ["liquid", "liquid paste", "paste", "solid paste", "solid"];
    const EMUL_TYPE = ["ow", "ow and wo", "wo"];

    const getData = async () => {
      descr.value = descriptions[0];
      try {
        bdd.value = await axios
          .get("http://127.0.0.1:5000/" + route.params.type + "/" + id)
          .then((res) => res.data);
      } catch (error) {
        console.log(error);
      }
    }

    onMounted(getData);

    return {
      id,
      bdd,
      descr,
      QUALITATIVES,
      STATES,
      EMUL_TYPE,
    };
  },
  
};
</script>

<style>
</style>
