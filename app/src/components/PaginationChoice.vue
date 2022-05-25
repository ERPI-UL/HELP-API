<template>
    <div v-show="this.obj.showing" id="pagination-parent" class="flex flex-col justify-center absolute top-0 left-0 w-screen h-screen bg-black/[0.4]">
        <div class="p-1 flex flex-col min-w-[50vw] min-h-[50vh] md:max-w-[70vw] max-w-[98vw] md:max-h-[70vh] max-h-[98vh] bg_white shadow-lg border border-1 border-gray-200 mx-auto bg-white rounded-lg"> <!-- POPUP -->
            <div class="flex flex-col grow min-h-0">
                <div class="flex">
                    <h1 class="text-indigo-600 font-extrabold text-2xl mx-2">{{ title }}</h1>
                    <span class="refresh-btn border border-2 rounded border-indigo-600 bg-indigo-600 my-auto ml-auto md:block hidden cursor-pointer shadow-md">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                    </span>
                </div>
                <div class="flex justify-between my-2"> <!-- CONTROLS -->
                    <div class="w-full disabled:opacity-50" v-on:click="this.obj.prevPage">
                        <svg xmlns="http://www.w3.org/2000/svg" class="shadow h-8 w-8 cursor-pointer text-indigo-600 m-auto border border-1 border-indigo-600 rounded-lg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
                        </svg>
                    </div>
                    <div class="w-full">
                        <p id="pagination-state" class="m-auto w-fit">{{ this.obj.pageNumber }} / {{ this.obj.pageNbr_max }}</p>
                    </div>
                    <div class="w-full disabled:opacity-50" v-on:click="this.obj.nextPage">
                        <svg xmlns="http://www.w3.org/2000/svg" class="shadow h-8 w-8 cursor-pointer text-indigo-600 m-auto border border-1 border-indigo-600 rounded-lg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
                        </svg>
                    </div>
                </div>
                <div class="flex flex-col overflow-x-hidden overflow-y-scroll grow border border-1 border-gray-300 rounded-lg bg-indigo-50 min-h-0">
                    <div v-for="el in this.obj.paginationContent[this.obj.pageNumber]" class="flex px-2 py-1 hover:bg-indigo-200 select-none space-x-2" v-on:click="el.selected = !el.selected">
                        <p class="flex grow text-base">{{ el.label }}</p>
                        <div v-show="el.selected">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                        <div v-show="!el.selected" class="h-6 w-6"></div>
                    </div>
                </div>
            </div>
            <div class="flex grow-0 m-1 justify-between"> <!-- BUTTONS -->
                <CancelButton v-on:click="this.hide();">Annuler</CancelButton>
                <span class="refresh-btn border border-2 rounded border-indigo-600 bg-indigo-600 m-auto md:hidden block shadow-md">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                </span>
                <ValidateButton v-on:click="this.validate();">Valider</ValidateButton>
            </div>
        </div>
    </div>
</template>

<script>
import API from '../script/API';
import User from '../script/User';
import CancelButton from "./CancelButton.vue";
import ValidateButton from "./ValidateButton.vue";

function updatePagination(self, forceRefresh=false)
{
    if (!self.obj.paginationContent[self.obj.pageNumber] || forceRefresh) {
        API.execute_logged(self.route+API.createPagination(self.obj.pageNumber, self.obj.pageLength), API.METHOD_GET, User.currentUser.getCredentials(), undefined, API.TYPE_JSON).then(res => {
            self.obj.paginationContent[self.obj.pageNumber] = [];
            self.obj.pageNbr_min = 1;
            self.obj.pageNumber = res.current_page;
            self.obj.pageNbr_max = res.last_page;
            if (!res.data) return;
            res.data.forEach(el => {
                if (! (self.identifier(el) in self.selectedValues))
                self.obj.paginationContent[self.obj.pageNumber].push({
                    label: self.displayAttribute(el),
                    infos: el,
                    selected: self.identifier(el) in self.selectedValues
                });
            });
        }).catch(err => {
            self.obj.paginationContent[self.obj.pageNumber] = [{label: "Erreur de chargement : "+err.status, infos: null, selected: false}];
        });
    }
}

class PaginationController {
    showing = false;
    paginationContent = [];
    pageNumber = 1;
    pageLength = 10;
    pageNbr_min = 1;
    pageNbr_max = 1;
}

export default {
    name: "PaginationChoice",
    props: ["displayAttribute", "identifier", "selectedValues", "callback", "route", "selectID", "title"],
    data: () => {return {obj: new PaginationController()}},
    components: {
        CancelButton,
        ValidateButton
    },
    mounted: function() {
        window.addEventListener("keydown", ev => {
            if (!this.obj.showing) return;
            if (ev.key == "Enter") this.validate();
        });
        updatePagination(this);

        document.querySelectorAll(".refresh-btn").forEach(el => {
            el.addEventListener('click', ev => {
                if (!ev.target.childNodes[0]) return;
                if (ev.target.childNodes[0].classList.contains("animate-spin")) return; // Prevent multiple refresh
                updatePagination(this, true);
                ev.target.childNodes[0].classList.add("animate-spin");
                setTimeout(() => {
                    ev.target.childNodes[0].classList.remove("animate-spin");
                }, 1010);
            });
        });
    },
    methods: {
        show() {
            this.obj.showing = true;
        },
        hide() {
            this.obj.showing = false;
            const obj = document.querySelector(this.selectID);
            if (obj != null) obj.value = obj.children[0].value;
        },
        validate() {
            let selectedContent = [];
            this.obj.paginationContent.forEach(list => {
                list.forEach(el => {
                    if (el.selected && el.infos != null) selectedContent.push(el.infos);
                });
            });
            this.callback(selectedContent);
            this.hide();
        },
        nextPage() {
            this.obj.pageNumber = Math.min(this.obj.pageNumber + 1, this.obj.pageNbr_max);
            updatePagination(this);
        },
        prevPage() {
            this.obj.pageNumber = Math.max(this.obj.pageNumber - 1, this.obj.pageNbr_min);
            updatePagination(this);
        }
    }
}
</script>