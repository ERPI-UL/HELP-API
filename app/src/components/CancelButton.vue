<template>
    <!-- Template Cancel Button, same style as the Back Button : An action should be attached to this button (with v-on:click for example) -->
    <button type="button"
       class="h-fit cursor-pointer whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border rounded-md shadow-sm text-base font-medium text-black bg-gray-50 hover:bg-gray-100">
        <slot></slot>
    </button>
</template>

<script>
export default {
    name: "CancelButton",
    props: [],
    components: {},
    setup: () => {}
};
</script>
