<template>
    <button class="h-fit w-fit whitespace-nowrap inline-flex items-center justify-center px-4 py-2 border border-2 rounded-md shadow-sm text-base font-medium text-indigo-600 border-indigo-600 hover:text-indigo-700 hover:border-indigo-700 hover:bg-indigo-600/[0.1]">
        <slot></slot>
    </button>
</template>

<script>
export default {
    name: "OutlineButton",
    components: {},
    setup: () => {}
};
</script>