<template>
    <div class="min-h-screen flex flex-col">
        <div class="p-2">
            <Topbar></Topbar>
        </div>
        <div class="block md:flex grow">
            <div class="m-2 grow-0">
                <div class="bg-white rounded min-w-[12vw] divide-y grow">
                    <h2 class="text-2xl leading-9 font-extrabold text-indigo-600 px-6 py-2 whitespace-nowrap">Machines</h2>
                    <div class="md:pt-8 flex md:flex-col md:overflow-x-visible overflow-x-scroll justify-between">
                        <a class="whitespace-nowrap md:min-w-full md:p-4 md:m-4 p-2 m-2 rounded-lg text-base font-semibold text-left text-indigo-800 outline-none hover:border-indigo-300" 
                            :class="(window.location.href.split('#')[1] == 'all')?'bg-indigo-600 text-indigo-50 shadow-lg shadow-indigo-600': ''"
                            href="#all">
                            Toutes les machines
                        </a>
                        <a v-if="User.currentUser.canTeacher()" class="whitespace-nowrap md:min-w-full md:p-4 md:m-4 p-2 m-2 rounded-lg text-base font-semibold text-left text-indigo-800 outline-none hover:border-indigo-300"
                            :class="(window.location.href.split('#')[1] == 'editing')?'bg-indigo-600 text-indigo-50 shadow-lg shadow-indigo-600': ''"
                            href="#editing">
                            Créer / Modifier
                        </a>
                    </div>
                </div>
            </div>
            <div class="flex flex-col">
                <div v-if="window.location.href.split('#')[1] == 'editing'" class="m-4 w-fit h-fit">
                    <RedirectButton href="/machines/create">
                        <component :is="icon.plus" class="flex-shrink-0 h-5 text-white mr-2" aria-hidden="true" />
                        Nouvelle machine
                    </RedirectButton>
                </div>
                <div class="m-2 ml-4 flex grow flex-wrap justify-evenly"> <!-- Scenario -->
                    <MachineCard v-if="window.location.href.split('#')[1] == 'all'" v-for="item in machines.all">
                        <template v-slot:title>{{item.title}}</template>
                        <template v-slot:description>{{item.description}}</template>
                    </MachineCard>
                    <MachineCard v-if="window.location.href.split('#')[1] == 'editing'" v-for="item in machines.editing">
                        <template v-slot:title>{{item.title}}</template>
                        <template v-slot:description>{{item.description}}</template>
                        <template v-slot:href><RedirectButton :href="item.href">Editer</RedirectButton></template>
                    </MachineCard>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Topbar from "../components/Topbar.vue";
import MachineCard from "../components/MachineCard.vue";
import RedirectButton from "../components/RedirectButton.vue";
import User from "../script/User";

import {
    PlusIcon
} from "@heroicons/vue/solid";

let dom = null;

const machines = {
    all: [
        {title: "ML-W960", description: "Découpeuse laser ML-W960", href: "/"}
    ],
    editing: [
        {title: "ML-W960", description: "Découpeuse laser ML-W960", href: "/machines/edit?idMachine=1"}
    ]
}

export default {
    name: "Machines",
    components: {
        Topbar,
        MachineCard,
        RedirectButton
    },
    setup() {
        return {window, machines, User, icon: {plus: PlusIcon}}
    },
    mounted() {
        dom = this;
    }
};
</script>