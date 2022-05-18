<template>
    <div class="min-h-screen flex flex-col">
        <div class="p-2">
            <Topbar></Topbar>
        </div>
        <div class="block md:flex grow">
            <div class="m-2 grow-0">
                <div class="bg-white rounded min-w-[12vw] divide-y grow">
                    <h2 class="text-2xl leading-9 font-extrabold text-indigo-600 px-6 py-2 whitespace-nowrap">Scénarios</h2>
                    <div class="md:pt-8 flex md:flex-col md:overflow-x-visible overflow-x-scroll justify-between">
                        <a class="whitespace-nowrap md:min-w-full md:p-4 md:m-4 p-2 m-2 rounded-lg text-base font-semibold text-left text-indigo-800 outline-none hover:border-indigo-300" 
                            :class="(window.location.href.split('#')[1] == 'all')?'bg-indigo-600 text-indigo-50 shadow-lg shadow-indigo-600': ''"
                            href="#all">
                            Tous les scénarios
                        </a>
                        <a v-if="user.canLearner()" class="whitespace-nowrap md:min-w-full md:p-4 md:m-4 p-2 m-2 rounded-lg text-base font-semibold text-left text-indigo-800 outline-none hover:border-indigo-300"
                            :class="(window.location.href.split('#')[1] == 'pending')?'bg-indigo-600 text-indigo-50 shadow-lg shadow-indigo-600': ''"
                            href="#pending">
                            Scénarios en cours
                        </a>
                        <a v-if="user.canTeacher()" class="whitespace-nowrap md:min-w-full md:p-4 md:m-4 p-2 m-2 rounded-lg text-base font-semibold text-left text-indigo-800 outline-none hover:border-indigo-300"
                            :class="(window.location.href.split('#')[1] == 'editing')?'bg-indigo-600 text-indigo-50 shadow-lg shadow-indigo-600': ''"
                            href="#editing">
                            Créer / Modifier
                        </a>
                    </div>
                </div>
            </div>
            <div class="flex flex-col grow m-2 overflow-x-hidden overflow-y-scroll">
                <div v-if="window.location.href.split('#')[1] == 'editing'" class="m-4 w-fit h-fit">
                    <RedirectButton href="/scenarios/create">
                        <component :is="icon.plus" class="flex-shrink-0 h-5 text-white mr-2" aria-hidden="true" />
                        Nouveau scénario
                    </RedirectButton>
                </div>
                <div class="m-2 ml-4 flex grow flex-wrap justify-evenly"> <!-- Scenario -->
                    <Scenario v-if="window.location.href.split('#')[1] == 'all'" v-for="item in scenarios.all">
                        <template v-slot:title>{{item.title}}</template>
                        <template v-slot:machine>{{item.machine}}</template>
                        <template v-slot:description>{{item.description}}</template>
                    </Scenario>
                    <Scenario v-if="window.location.href.split('#')[1] == 'editing'" v-for="item in scenarios.editing">
                        <template v-slot:title>{{item.title}}</template>
                        <template v-slot:machine>{{item.machine}}</template>
                        <template v-slot:description>{{item.description}}</template>
                        <template v-slot:href><RedirectButton :href="item.href">Editer</RedirectButton></template>
                        <template v-slot:remove><DangerousButton v-on:click="removeScenario(item.id, $event.target)">Supprimer</DangerousButton></template>
                    </Scenario>
                    <Scenario v-if="window.location.href.split('#')[1] == 'pending'" v-for="item in scenarios.pending">
                        <template v-slot:title>{{item.title}}</template>
                        <template v-slot:machine>{{item.machine}}</template>
                        <template v-slot:description>{{item.description}}</template>
                    </Scenario>
                    <ValidatePopup ref="delete-popup"></ValidatePopup>
                </div>
                <div class="flex grow-0 m-2 p-2 justify-center w-full">
                    <OutlineButton
                        v-if="(window.location.href.split('#')[1] == 'all' || window.location.href.split('#')[1] == 'editing') && obj.displayMoreAllButton"
                        v-on:click="loadNextAllScenarios();">
                        Voir plus
                    </OutlineButton>
                    <OutlineButton
                        v-if="window.location.href.split('#')[1] == 'pending' && obj.displayMoreAllButton"
                        v-on:click="loadNextOwnScenarios();">
                        Voir plus
                    </OutlineButton>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Topbar from "../components/Topbar.vue";
import Scenario from "../components/Scenario.vue";
import RedirectButton from "../components/RedirectButton.vue";
import OutlineButton from "../components/OutlineButton.vue";
import DangerousButton from "../components/DangerousButton.vue";
import ValidatePopup from "../components/ValidatePopup.vue";
import User from "../script/User";
import API from '../script/API';
import {
    PlusIcon
} from "@heroicons/vue/solid";

let dom = null;
let Alliterator = null;
let Owniterator = null;
let obj = {
    displayMoreAllButton: false,
    displayMoreOwnButton: false
};

let loadNextAllScenarios = () => {return Alliterator != null && Alliterator.isNext();}
let loadNextOwnScenarios = () => {return Owniterator != null && Owniterator.isNext();}

function attachAllListeners(it) {
    it.promise.then(res => {
        const data = res.data.map(el => {return {
            id: el.id,
            title: el.name,
            description: el.description,
            machine: el.machine.name,
            href: "/scenarios/edit?idScenario="+el.id
        }});
        scenarios.all = scenarios.all.concat(data);
        scenarios.editing = scenarios.editing.concat(data);
        obj.displayMoreAllButton = Alliterator.isNext();
        if (dom != null) dom.$forceUpdate();
    }).catch(err => {
        console.error(err);
        obj.displayMoreAllButton = false;
        if (dom != null) dom.$forceUpdate();
    });
    loadNextAllScenarios = () => {
        iterator = it.next();
        if (iterator != null) {
            attachAllListeners(iterator);
            return iterator.isNext();
        } else return false;
    };
}

function attachOwnListeners(it) {
    it.promise.then(res => {
        scenarios.pending.concat(res.data.map(el => {return {
            title: el.name,
            description: el.description,
            machine: el.machine.name,
            href: "/scenarios/continue?idScenario="+el.id
        }}));
        obj.displayMoreOwnButton = Owniterator.isNext();
        if (dom != null) dom.$forceUpdate();
    }).catch(err => {
        console.error(err);
        obj.displayMoreOwnButton = false;
        if (dom != null) dom.$forceUpdate();
    });
    loadNextOwnScenarios = () => {
        iterator = it.next();
        if (iterator != null) {
            attachOwnListeners(iterator);
            return iterator.isNext();
        } else return false;
    };
}

function fetchAllScenarios() {
    Alliterator = API.iterate(API.ROUTE.SCENARIOS);
    attachAllListeners(Alliterator);
}

function fetchOwnScenarios() {
    Owniterator = API.iterate(API.ROUTE.STATS.USERS+User.currentUser.id+API.ROUTE.STATS.__SESSIONS);
    attachOwnListeners(Owniterator);
}

function removeScenario(id, caller) {
    const el = this.$refs["delete-popup"];
    el.show("Supprimer un scénario", "Voulez-vous supprimer "+(scenarios.editing.find(el => el.id == id).title)+" ?", "Annuler", "Supprimer");
    el.setPosition(caller);
    el.setCallback(() => {
        API.execute_logged(API.ROUTE.SCENARIOS+id, API.METHOD_DELETE, User.currentUser.getCredentials(), {}, API.TYPE_JSON).then(res => {
            let dom = caller;
            while (dom.id != "scenario-parent") dom = dom.parentElement;
            dom.remove();
        }).catch(console.error);
    });
}

const scenarios = {
    all: [
        
    ],
    pending: [
        
    ],
    editing: [
        
    ]
}

export default {
    name: "Scenarios",
    components: {
        Topbar,
        Scenario,
        RedirectButton,
        OutlineButton,
        DangerousButton,
        ValidatePopup
    },
    setup() {
        if (window.location.href.split("#").length < 2) window.location.href += "#all";
        return {window, scenarios, user: User.currentUser, icon: {plus: PlusIcon}, obj}
    },
    mounted() {
        dom = this;
        fetchAllScenarios();
        fetchOwnScenarios();
    },
    methods: {loadNextAllScenarios, loadNextOwnScenarios, removeScenario}
};
</script>