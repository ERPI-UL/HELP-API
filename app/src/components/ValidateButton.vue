<template>
    <button type="button"
       class="whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700">
        <slot></slot>
    </button>
</template>

<script>
export default {
    name: "ValidateButton",
    components: {},
    setup: () => {}
};
</script>