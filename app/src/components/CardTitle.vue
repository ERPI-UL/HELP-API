<template>
    <div class="flex min-w-fit">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-indigo-600 my-1 md:block hidden" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <slot name="path"></slot>
        </svg>
        <h2 class="md:text-2xl text-xl font-extrabold text-indigo-600 md:pl-4 pl-0">
            <slot name="title"></slot>
        </h2>
    </div>
</template>

<script>

export default {
    name: "CardTitle",
    components: {

    }
}
</script>
