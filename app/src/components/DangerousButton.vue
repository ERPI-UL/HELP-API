<template>
    <!-- Template Dangerous Button : Big red button to indicate critical action such as deletions, etc. -->
    <button class="h-fit w-fit whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-red-600 hover:bg-red-700">
        <slot></slot>
    </button>
</template>

<script>
export default {
    name: "DangerousButton",
    components: {},
    setup: () => {}
};
</script>