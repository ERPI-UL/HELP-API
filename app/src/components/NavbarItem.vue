<template>
    <div class="flex flex-col justify-center items-center h-14 hover:bg-slate-300 w-16 rounded">
        <slot></slot>
    </div>
</template>

<script>
export default {
    name: 'NavbarItem',
}
</script>

<style scopped>
div > svg {
    @apply h-6;
}

.selected {
    @apply text-black;
}

</style>