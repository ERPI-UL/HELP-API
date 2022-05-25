<template>
    <button type="button"
       class="h-fit cursor-pointer whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100"
       v-on:click="redirectHome();">
        <slot></slot>
    </button>
</template>

<script>
import { redirectHome } from '../script/common';

export default {
    name: "BackButton",
    components: {},
    setup: () => {},
    methods: {redirectHome}
};
</script>
