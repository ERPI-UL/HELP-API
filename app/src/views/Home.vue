<template>
  <div>
    <Topbar>
      <template v-slot:left>
        <Blank></Blank>
      </template>

      <template v-slot:default>
        <h1 class="font-bold">Home</h1>
      </template>

      <template v-slot:right>
        <div class="pr-4">
          <VTooltip :triggers="['click', 'touch']">
            <InformationCircleIcon
              class="h-6 w-6 cursor-pointer"
            ></InformationCircleIcon>
            <template #popper>
              <div>
                <header class="font-semibold top-0 flex justify-between p-2">
                  About
                </header>
                <div class="flex-col flex gap-4 p-2 border-t-2">
                  Informations sur Formutools
                </div>
              </div>
            </template>
          </VTooltip>
        </div>
      </template>
    </Topbar>

    <main class="p-4">
      <Card>
        <div class="flex flex-col items-center justify-center h-full">
          <img class="rounded-full shadow-lg m-4" src="../assets/logo.png" />
          <div class="font-semibold m-4 text-center">
            Formutools <br />
            Ver. 0.3
          </div>
          <router-link
            class="
              items-center
              rounded-lg
              p-4
              text-center
              font-semibold
              w-64
              shadow-lg
              bg-emerald-300
              m-4
              cursor-pointer
            "
            to="/explore"
            >Explore</router-link
          >
          <router-link
            class="
              items-center
              rounded-lg
              p-4
              text-center
              font-semibold
              w-64
              shadow-lg
              bg-amber-300
              m-4
              cursor-pointer
            "
            to=""
            >Formulate</router-link
          >
        </div>
      </Card>
    </main>
  </div>
</template>

<script>
import Topbar from "../components/Topbar.vue";
import Card from "../components/Card.vue";
import { InformationCircleIcon } from "@heroicons/vue/outline";
import Blank from '../components/Blank.vue';

export default {
  name: "Home",
  components: {
    Topbar,
    Card,
    InformationCircleIcon,
    Blank,
  },
};
</script>


<style>
</style>