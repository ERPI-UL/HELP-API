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
            <div class="flex flex-col grow m-2 min-h-0 overflow-x-hidden overflow-y-scroll">
                <div v-if="window.location.href.split('#')[1] == 'editing'" class="m-4 w-fit h-fit">
                    <RedirectButton href="/machines/create">
                        <component :is="icon.plus" class="flex-shrink-0 h-5 text-white mr-2" aria-hidden="true" />
                        Nouvelle machine
                    </RedirectButton>
                </div>
                <div class="m-2 ml-4 flex grow flex-wrap justify-evenly"> <!-- Scenario -->
                    <MachineCard v-if="window.location.href.split('#')[1] == 'all'" v-for="item in obj.machines.all">
                        <template v-slot:title>{{item.title}}</template>
                        <template v-slot:description>{{item.description}}</template>
                    </MachineCard>
                    <MachineCard v-if="window.location.href.split('#')[1] == 'editing'" v-for="item in obj.machines.editing" id="machine-container">
                        <template v-slot:title>{{item.title}}</template>
                        <template v-slot:description>{{item.description}}</template>
                        <template v-slot:href><RedirectButton :href="item.href">Editer</RedirectButton></template>
                        <template v-slot:remove><DangerousButton v-on:click="removeMachine(item.id, $event.target);">Supprimer</DangerousButton></template>
                    </MachineCard>
                    <ValidatePopup ref="delete-popup"></ValidatePopup>
                </div>
                <div class="flex grow-0 m-2 p-2 justify-center w-full">
                    <OutlineButton v-if="obj.displayMoreBtn" v-on:click="loadNextMachines();">Voir plus</OutlineButton>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Topbar from "../components/Topbar.vue";
import MachineCard from "../components/MachineCard.vue";
import RedirectButton from "../components/RedirectButton.vue";
import OutlineButton from "../components/OutlineButton.vue";
import DangerousButton from "../components/DangerousButton.vue";
import ValidatePopup from "../components/ValidatePopup.vue";
import User from "../script/User";

import {
    PlusIcon
} from "@heroicons/vue/solid";
import API from '../script/API';

let dom = null;
let obj = {
    displayMoreBtn: false,
    machines: {
        all: [
            
        ],
        editing: [
            
        ]
    }
};

let loadNextMachines = () => {return iterator != null && iterator.isNext();};
let iterator = null;

function attachListeners(it) {
    it.promise.then(response => {
        const data = response.data.map(el => {return {
            id: el.id,
            title: el.name,
            description: el.description,
            href: `/machines/edit?idMachine=${el.id}`
        }});
        obj.machines.all = obj.machines.all.concat(data);
        obj.machines.editing = obj.machines.editing.concat(data);
        obj.displayMoreBtn = it.isNext();
        if (dom != null) dom.$forceUpdate();
    }).catch(error => {
        console.error(error);
        obj.displayMoreBtn = false;
        if (dom != null) dom.$forceUpdate();
    });
    loadNextMachines = () => {
        iterator = it.next();
        if (iterator != null) {
            attachListeners(iterator);
            return iterator.isNext();
        } else return false;
    }
}

function removeMachine(id, caller) {
    const el = this.$refs["delete-popup"];
    el.show("Supprimer une machine", "Voulez-vous supprimer "+(obj.machines.all.find(el => el.id == id).title)+" ?", "Annuler", "Supprimer");
    el.setPosition(caller);
    el.setCallback(() => {
        API.execute_logged(API.ROUTE.MACHINES+id, API.METHOD_DELETE, User.currentUser.getCredentials(), {}, API.TYPE_JSON).then(res => {
            let dom = caller;
            while (dom.id != "machine-container") dom = dom.parentElement;
            dom.remove();
        }).catch(console.error);
    });
}

function fetchMachines() {
    iterator = API.iterate(API.ROUTE.MACHINES);
    attachListeners(iterator);
}

export default {
    name: "Machines",
    components: {
        Topbar,
        MachineCard,
        RedirectButton,
        OutlineButton,
        DangerousButton,
        ValidatePopup
    },
    setup() {
        if (window.location.href.split("#").length < 2) window.location.href += "#all";
        return {window, User, icon: {plus: PlusIcon}, obj}
    },
    mounted() {
        dom = this;
        fetchMachines();
    },
    methods: {loadNextMachines, removeMachine}
};
</script>