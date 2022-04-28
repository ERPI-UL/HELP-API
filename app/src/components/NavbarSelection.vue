<template>
    <div class="fixed bottom-0 w-screen bg-white h-14 flex justify-center gap-6 text-slate-500">
        <NavbarItem id="navbar-ahp" class="selected" v-on:click="updateSelected('navbar-ahp')">
            <span>AHP</span>
            <ChartPieIcon></ChartPieIcon>
        </NavbarItem>
        <!-- <NavbarItem id="navbar-custom" v-on:click="updateSelected('navbar-custom')">
            <span>Custom</span>
            <TableIcon></TableIcon>
        </NavbarItem> -->
    </div>
</template>

<script>
import NavbarItem from "./NavbarItem.vue"
import { ref, watch } from 'vue'
import { ChartPieIcon, ViewListIcon, TableIcon } from "@heroicons/vue/outline"

export default {
    name: 'NavbarGraph',
    components: {
        NavbarItem,
        ChartPieIcon, ViewListIcon, TableIcon,
    },
    setup(props, context) {
        const selected = ref('navbar-ahp')

        const updateSelected = (value) => {
            selected.value = value
        }

        watch(selected, (newValue, oldValue) => {
            document.getElementById(oldValue).classList.remove('selected')
            document.getElementById(newValue).classList.add('selected')

            context.emit("valueChange", newValue)
        })

        return {
            updateSelected
        }
    }
}
</script>

<style>

</style>