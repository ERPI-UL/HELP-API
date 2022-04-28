<template>
    <div>
        <div class="flex items-center justify-between">
            <div class="flex items-center gap-1">
                <span :id="title + '-open'" class="hidden" v-on:click="closeDrawer()">
                    <ChevronDownIcon class="h-5"></ChevronDownIcon>
                </span>
                <span :id="title + '-close'" class="" v-on:click="openDrawer()">
                    <ChevronRightIcon class="h-5"></ChevronRightIcon>
                </span>
                <h2 class="font-semibold">{{ title }}</h2>
            </div>
            <div class="flex gap-1">
                <slot name="right"></slot>
            </div>
        </div>
        <div :id="title + '-items'" class="flex flex-col gap-4 overflow-hidden h-0 transition-all ml-4">
            <slot name="items"></slot>
        </div>
    </div>
</template>

<script>
import { ChevronRightIcon, ChevronDownIcon } from "@heroicons/vue/outline";

export default {
    name: 'Drawer',
    components: {
        ChevronDownIcon,
        ChevronRightIcon
    },
    props: {
        title: String
    },
    setup(props) {
        const openDrawer = () => {
            document.getElementById(props.title + "-open").classList.remove("hidden");
            document.getElementById(props.title + "-close").classList.add("hidden");
            var items = document.getElementById(props.title + "-items");
            items.classList.remove("h-0");
            items.classList.add("mt-3");
        };

        const closeDrawer = () => {
            document.getElementById(props.title + "-open").classList.add("hidden");
            document.getElementById(props.title + "-close").classList.remove("hidden");
            var items = document.getElementById(props.title + "-items");
            items.classList.add("h-0");
            items.classList.remove("mt-3");
        };

        return {
            openDrawer,
            closeDrawer
        }
    }
}
</script>

<style>

</style>