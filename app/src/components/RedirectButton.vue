<template>
    <a type="button"
       class="whitespace-nowrap cursor-pointer inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700">
        <slot></slot>
    </a>
</template>

<script>
export default {
    name: "RedirectButton",
    components: {},
    setup: () => {}
};
</script>