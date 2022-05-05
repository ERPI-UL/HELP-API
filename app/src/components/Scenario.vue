<template>
    <div class="scenario-parent bg-white rounded-lg shadow-lg p-4 min-w-fit h-fit max-w-[25vw] m-4 hover:shadow-xl hover:scale-105 cursor-pointer">
        <div class="top">
            <div class="flex justify-between center">
                <h2 class="text-indigo-600 font-bold text-lg">
                    <slot name="title"></slot>
                </h2>
                <h2 class="ml-10 text-indigo-400 font-base text-base">
                    <slot name="machine"></slot>
                </h2>
            </div>
            <p class="text-gray-400 text-base text-sm">
                <slot name="description"></slot>
            </p>
        </div>
        <div class="pt-8 flex justify-between">
            <slot name="progress"></slot>
        </div>
        <div class="pt-8 flex justify-between">
            <div></div>
            <slot name="href"></slot>
        </div>
    </div>
</template>

<script>

export default {
    name: "Scenario",
    components: {
        
    },
    setup: () => {
        return {user: JSON.parse(localStorage.getItem('user')??"{}")}
    }
}
</script>
