<template>
    <!-- Template Back Button : Used to go bakc in the website -->
    <button type="button"
       class="h-fit cursor-pointer whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100"
       v-on:click="$router.go(-1)">
        <slot></slot>
    </button>
</template>

<script>
export default {
    name: "BackButton",
    components: {},
    setup: () => {},
    methods: {}
};
</script>
