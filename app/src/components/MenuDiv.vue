<template>
    <div class="flex flex-col m-2 min-w-0 overflow-hidden">
        <h2 class="text-indigo-400 text-xl ml-2">{{title}}</h2>
        <div class="flex md:flex-row flex-col md:space-x-8 md:space-y-0 space-y-4 md:p-4 p-2 border border-2 border-indigo-300 rounded-lg overflow-x-auto min-w-0 max-w-full w-fit">
            <slot></slot>
        </div>
    </div>
</template>

<script>
export default {
    name: "MenuDiv",
    components: {

    },
    props: {
        title: {
            type: String,
            required: true
        }
    }
}
</script>